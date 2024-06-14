/*
 * Copyright (c) 2023, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <fcntl.h>
#include <linux/fs.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/types.h>

#include <data_readers/data_reader.hpp>
#include <data_readers/multi_hot/async_data_reader.hpp>
#include <pybind/model.hpp>

namespace HugeCTR {

Input get_input_from_json(const nlohmann::json& j_input) {
  auto type_name = get_value_from_json<std::string>(j_input, "type");
  if (type_name.compare("Data") != 0) {
    HCTR_OWN_THROW(Error_t::WrongInput, "the first layer is not Data layer:" + type_name);
  }
  auto j_label = get_json(j_input, "label");

  auto label_name = get_json(j_label, "top");
  auto label_dim = get_json(j_label, "label_dim");
  std::vector<std::string> label_name_vec;
  std::vector<int> label_dim_vec;

  if (label_name.is_array()) {
    if (label_name.size() != label_dim.size()) {
      HCTR_OWN_THROW(Error_t::WrongInput,
                     "the number of label names does not match number of label dimensions");
    }
    for (int label_id = 0; label_id < label_name.size(); label_id++) {
      label_name_vec.push_back(label_name[label_id].get<std::string>());
      label_dim_vec.push_back(label_dim[label_id].get<int>());
    }
  } else {
    label_name_vec.push_back(label_name.get<std::string>());
    label_dim_vec.push_back(label_dim.get<int>());
  }

  auto j_dense = get_json(j_input, "dense");
  auto dense_name = get_value_from_json<std::string>(j_dense, "top");
  auto dense_dim = get_value_from_json<int>(j_dense, "dense_dim");

  std::vector<DataReaderSparseParam> data_reader_sparse_param_array;
  auto j_sparse = get_json(j_input, "sparse");
  for (unsigned int i = 0; i < j_sparse.size(); i++) {
    const nlohmann::json& js = j_sparse[i];
    const auto sparse_name = get_value_from_json<std::string>(js, "top");
    bool is_fixed_length = get_value_from_json<int>(js, "is_fixed_length");
    int slot_num = get_value_from_json<int>(js, "slot_num");
    auto nnz_per_slot = get_json(js, "nnz_per_slot");
    std::vector<int> nnz_per_slot_vec;

    if (nnz_per_slot.is_array()) {
      if (nnz_per_slot.size() != static_cast<size_t>(slot_num)) {
        HCTR_OWN_THROW(Error_t::WrongInput, "nnz_per_slot.size() != slot_num");
      }
      for (int slot_id = 0; slot_id < slot_num; ++slot_id) {
        nnz_per_slot_vec.push_back(nnz_per_slot[slot_id].get<int>());
      }
    } else {
      // max nnz for each slot is the same
      int max_nnz = nnz_per_slot.get<int>();
      for (int slot_id = 0; slot_id < slot_num; ++slot_id) {
        nnz_per_slot_vec.push_back(max_nnz);
      }
    }
    DataReaderSparseParam param{sparse_name, nnz_per_slot_vec, is_fixed_length, slot_num};

    data_reader_sparse_param_array.push_back(param);
  }
  Input input =
      Input(label_dim_vec, label_name_vec, dense_dim, dense_name, data_reader_sparse_param_array);
  return input;
}

static int get_logical_sector_size(std::string file) {
  int fd = open(file.c_str(), O_RDONLY);
  int logical_sector_size = 0;
  if (ioctl(fd, BLKSSZGET, &logical_sector_size) < 0) {
    HCTR_LOG_C(WARNING, WORLD, "Can't get logical sector size of ", file,
               ". Returning default 4096\n");
    logical_sector_size = 4096;
  }
  close(fd);
  return logical_sector_size;
}
template <typename TypeKey>
void add_input(Input& input, DataReaderParams& reader_params,
               std::map<std::string, SparseInput<TypeKey>>& sparse_input_map,
               std::vector<std::vector<TensorEntity>>& train_tensor_entries_list,
               std::vector<std::vector<TensorEntity>>& evaluate_tensor_entries_list,
               std::shared_ptr<IDataReader>& train_data_reader,
               std::shared_ptr<IDataReader>& evaluate_data_reader, size_t batch_size,
               size_t batch_size_eval, bool use_mixed_precision, bool repeat_dataset,
               bool train_intra_iteration_overlap, size_t num_iterations_statistics,
               const std::shared_ptr<ResourceManager> resource_manager) {
  DataReaderType_t format = reader_params.data_reader_type;
  // Check_t check_type = reader_params.check_type;
  std::string source_data = reader_params.source[0];
  std::string eval_source = reader_params.eval_source;
  // TODO - changes structures to support multiple labels
  std::string top_strs_dense = input.dense_name;
  int dense_dim = input.dense_dim;

  std::string top_strs_label = input.labels_.begin()->first;
  int total_label_dim = std::accumulate(
      std::begin(input.labels_), std::end(input.labels_), 0,
      [](const int previous, const std::pair<std::string, int>& p) { return previous + p.second; });

  int total_max_sparse_dim = 0;
  bool sample_len_fixed = true;
  if (input.labels_.size() > 1) {
    top_strs_label = "combined_multi_label";
  }

  for (unsigned int i = 0; i < input.data_reader_sparse_param_array.size(); i++) {
    DataReaderSparseParam param = input.data_reader_sparse_param_array[i];
    std::string sparse_name = param.top_name;
    total_max_sparse_dim += param.max_nnz * param.slot_num;
    sample_len_fixed &= param.is_fixed_length;
    SparseInput<TypeKey> sparse_input(param.slot_num, param.max_feature_num);
    sparse_input_map.emplace(sparse_name, sparse_input);
  }
  if (format == DataReaderType_t::Norm) {
    HCTR_OWN_THROW(Error_t::Deprecated, "Norm is deprecated");
  }
  if (format == DataReaderType_t::Raw) {
    HCTR_OWN_THROW(Error_t::Deprecated, "Raw is deprecated");
  }
  if ((format == DataReaderType_t::RawAsync)) {
    if (reader_params.async_param.multi_hot_reader) {
      bool is_float_dense = reader_params.async_param.is_dense_float;
      int num_threads = reader_params.async_param.num_threads;
      int num_batches_per_thread = reader_params.async_param.num_batches_per_thread;
      bool shuffle = reader_params.async_param.shuffle;
      int cache_eval_data = reader_params.cache_eval_data;
      bool schedule_h2d = false;

      // If we want to cache eval, make sure we have enough buffers
      auto eval_num_batches_per_thread = num_batches_per_thread;
      if (cache_eval_data > num_threads * num_batches_per_thread) {
        eval_num_batches_per_thread = (cache_eval_data + num_threads - 1) / num_threads;
        HCTR_LOG_S(INFO, ROOT)
            << "Multi-Hot AsyncDataReader: eval reader increased batches per thread to "
            << eval_num_batches_per_thread << " to accommodate for the caching" << std::endl;
      }

      HCTR_LOG_S(INFO, ROOT) << "Multi-Hot AsyncDataReader: num_threads = " << num_threads
                             << std::endl;
      HCTR_LOG_S(INFO, ROOT) << "Multi-Hot AsyncDataReader: num_batches_per_thread = "
                             << num_batches_per_thread << std::endl;
      HCTR_LOG_S(INFO, ROOT) << "Multi-Hot AsyncDataReader: shuffle = " << (shuffle ? "ON" : "OFF")
                             << std::endl;
      HCTR_LOG_S(INFO, ROOT) << "Multi-Hot AsyncDataReader: schedule_h2d = "
                             << (schedule_h2d ? "ON" : "OFF") << std::endl;

      MultiHot::FileSource file_source;
      file_source.name = source_data;
      file_source.slot_id = 0;

      train_data_reader.reset(new MultiHot::AsyncDataReader<TypeKey>(
          {file_source}, resource_manager, batch_size, num_threads, num_batches_per_thread,
          input.data_reader_sparse_param_array, total_label_dim, dense_dim, use_mixed_precision,
          shuffle, schedule_h2d, is_float_dense));

      file_source.name = eval_source;
      evaluate_data_reader.reset(new MultiHot::AsyncDataReader<TypeKey>(
          {file_source}, resource_manager, batch_size_eval, num_threads,
          eval_num_batches_per_thread, input.data_reader_sparse_param_array, total_label_dim,
          dense_dim, use_mixed_precision, false, schedule_h2d, is_float_dense));

    } else {
      HCTR_OWN_THROW(Error_t::WrongInput, "Only multi-hot async datareader is supported.");
    }

    auto schedulable_train_reader =
        std::dynamic_pointer_cast<SchedulableDataReader>(train_data_reader);
    auto schedulable_eval_reader =
        std::dynamic_pointer_cast<SchedulableDataReader>(evaluate_data_reader);

    for (size_t i = 0; i < resource_manager->get_local_gpu_count(); i++) {
      train_tensor_entries_list[i].push_back(
          {top_strs_label, schedulable_train_reader->get_label_tensor23s()[i]});
      evaluate_tensor_entries_list[i].push_back(
          {top_strs_label, schedulable_eval_reader->get_label_tensor23s()[i]});

      train_tensor_entries_list[i].push_back(
          {top_strs_dense, schedulable_train_reader->get_dense_tensor23s()[i]});
      evaluate_tensor_entries_list[i].push_back(
          {top_strs_dense, schedulable_eval_reader->get_dense_tensor23s()[i]});
    }

    return;

  } else {
    int num_workers_train = reader_params.num_workers;
    int num_workers_eval = reader_params.num_workers;
#ifndef DISABLE_CUDF
    long long parquet_source_max_row_group_size = 0;
    long long parquet_eval_max_row_group_size = 0;
    size_t parquet_label_cols = 0;
    size_t parquet_dense_cols = 0;
    // size_t parquet_cat_cols = 0;
    int local_gpu_count = resource_manager->get_local_gpu_count();
    std::vector<int> variable_slots_id;
    std::shared_ptr<Metadata> parquet_meta = std::make_shared<Metadata>();
    auto get_meta_path = [&](std::string one_parquet_file_path) -> std::string {
      std::size_t found = one_parquet_file_path.find_last_of("/\\");
      std::string metadata_path = one_parquet_file_path.substr(0, found);
      metadata_path.append("/_metadata.json");
      return metadata_path;
    };
    if (format == DataReaderType_t::Parquet) {
      // if parallelism granularity is file, num_files should be greater than num of workers
      std::string first_file_name, buff;
      std::ifstream read_stream(eval_source, std::ifstream::in);
      if (!read_stream.is_open()) {
        HCTR_OWN_THROW(Error_t::FileCannotOpen, "file list open failed: " + eval_source);
      }
      std::getline(read_stream, buff);
      int num_of_files = std::stoi(buff);
      std::string metadata_path;
      if (num_of_files) {
        std::getline(read_stream, first_file_name);
        metadata_path = get_meta_path(first_file_name);
        parquet_meta->reset_metadata(metadata_path);
        parquet_eval_max_row_group_size = parquet_meta->get_max_row_group();
        HCTR_LOG(INFO, ROOT, "eval source %s max_row_group_size %lld\n", eval_source.c_str(),
                 parquet_eval_max_row_group_size);
      }
      parquet_label_cols = parquet_meta->get_label_names().size();
      parquet_dense_cols = parquet_meta->get_cont_names().size();

      read_stream.close();
      std::vector<std::string> train_sources = reader_params.source;
      for (const auto& file_list_name : train_sources) {
        std::string first_file_name, buff;
        std::ifstream read_stream(file_list_name, std::ifstream::in);
        if (!read_stream.is_open()) {
          HCTR_OWN_THROW(Error_t::FileCannotOpen, "file list open failed: " + eval_source);
        }
        std::getline(read_stream, buff);
        int num_of_files = std::stoi(buff);
        std::string metadata_path;
        if (num_of_files) {
          std::getline(read_stream, first_file_name);
          metadata_path = get_meta_path(first_file_name);
          parquet_meta->reset_metadata(metadata_path);
          parquet_source_max_row_group_size =
              std::max(parquet_meta->get_max_row_group(), parquet_source_max_row_group_size);
          HCTR_LOG(INFO, ROOT, "train source %s max_row_group_size %lld\n", file_list_name.c_str(),
                   parquet_source_max_row_group_size);
        }
      }

      if (!reader_params.read_file_sequentially) {
        // std::ifstream read_stream(eval_source, std::ifstream::in);
        num_workers_eval = std::min(num_workers_eval, num_of_files);

        std::vector<std::string> train_sources = reader_params.source;
        int min_num_files = 0;
        // there may exist multiple training sources
        for (const auto& file_list_name : train_sources) {
          std::ifstream read_stream(file_list_name, std::ifstream::in);
          if (!read_stream.is_open()) {
            HCTR_OWN_THROW(Error_t::FileCannotOpen, "file list open failed: " + file_list_name);
          }

          std::string buff;
          std::getline(read_stream, buff);
          int num_of_files = std::stoi(buff);
          if (!min_num_files || num_of_files < min_num_files) min_num_files = num_of_files;
          read_stream.close();
        }
        num_workers_train = std::min(num_workers_train, min_num_files);
      }
      num_workers_train = std::min(local_gpu_count, num_workers_train);
      num_workers_eval = std::min(local_gpu_count, num_workers_eval);
    }
#endif

    HCTR_LOG_S(INFO, ROOT) << "num of DataReader workers for train: " << num_workers_train
                           << std::endl;
    HCTR_LOG_S(INFO, ROOT) << "num of DataReader workers for eval: " << num_workers_eval
                           << std::endl;

    DataReader<TypeKey>* data_reader_tk = new DataReader<TypeKey>(
        batch_size, total_label_dim, dense_dim, input.data_reader_sparse_param_array,
        resource_manager, repeat_dataset, num_workers_train, use_mixed_precision,
        reader_params.data_source_params);
    train_data_reader.reset(data_reader_tk);
    DataReader<TypeKey>* data_reader_eval_tk = new DataReader<TypeKey>(
        batch_size_eval, total_label_dim, dense_dim, input.data_reader_sparse_param_array,
        resource_manager, repeat_dataset, num_workers_eval, use_mixed_precision,
        reader_params.data_source_params);
    evaluate_data_reader.reset(data_reader_eval_tk);

    long long slot_sum = 0;
    std::vector<long long> slot_offset;
    for (auto slot_size : reader_params.slot_size_array) {
      slot_offset.push_back(slot_sum);
      slot_sum += slot_size;
    }
    switch (format) {
      case DataReaderType_t::Norm: {
        HCTR_OWN_THROW(Error_t::Deprecated, "Norm is deprecated");
        break;
      }
      case DataReaderType_t::Raw: {
        HCTR_OWN_THROW(Error_t::Deprecated, "Raw is deprecated");
        break;
      }
      case DataReaderType_t::Parquet: {
#ifdef DISABLE_CUDF
        HCTR_OWN_THROW(Error_t::WrongInput, "Parquet is not supported under DISABLE_CUDF");
#else
        train_data_reader->create_drwg_parquet(
            source_data, reader_params.read_file_sequentially, slot_offset, repeat_dataset,
            parquet_source_max_row_group_size, parquet_dense_cols + parquet_label_cols,
            dense_dim + total_label_dim);
        evaluate_data_reader->create_drwg_parquet(
            eval_source, reader_params.read_file_sequentially, slot_offset, repeat_dataset,
            parquet_eval_max_row_group_size, parquet_dense_cols + parquet_label_cols,
            dense_dim + total_label_dim);
#endif
        break;
      }
      default: {
        assert(!"Error: no such option && should never get here!");
      }
    }

    for (size_t i = 0; i < resource_manager->get_local_gpu_count(); i++) {
      train_tensor_entries_list[i].push_back(
          {top_strs_label, data_reader_tk->get_label_tensor23s()[i]});
      evaluate_tensor_entries_list[i].push_back(
          {top_strs_label, data_reader_eval_tk->get_label_tensor23s()[i]});

      train_tensor_entries_list[i].push_back(
          {top_strs_dense, data_reader_tk->get_dense_tensor23s()[i]});
      evaluate_tensor_entries_list[i].push_back(
          {top_strs_dense, data_reader_eval_tk->get_dense_tensor23s()[i]});
    }

    for (unsigned int i = 0; i < input.data_reader_sparse_param_array.size(); i++) {
      auto& top_name = input.data_reader_sparse_param_array[i].top_name;
      const auto& sparse_input = sparse_input_map.find(top_name);

      sparse_input->second.train_sparse_tensors = data_reader_tk->get_sparse_tensor23s(top_name);
      sparse_input->second.evaluate_sparse_tensors =
          data_reader_eval_tk->get_sparse_tensor23s(top_name);
    }
  }  // end of else. not AsynRaw Reader
}

template void add_input<long long>(Input&, DataReaderParams&,
                                   std::map<std::string, SparseInput<long long>>&,
                                   std::vector<std::vector<TensorEntity>>&,
                                   std::vector<std::vector<TensorEntity>>&,
                                   std::shared_ptr<IDataReader>&, std::shared_ptr<IDataReader>&,
                                   size_t, size_t, bool, bool, bool, size_t,
                                   const std::shared_ptr<ResourceManager>);
template void add_input<unsigned int>(Input&, DataReaderParams&,
                                      std::map<std::string, SparseInput<unsigned int>>&,
                                      std::vector<std::vector<TensorEntity>>&,
                                      std::vector<std::vector<TensorEntity>>&,
                                      std::shared_ptr<IDataReader>&, std::shared_ptr<IDataReader>&,
                                      size_t, size_t, bool, bool, bool, size_t,
                                      const std::shared_ptr<ResourceManager>);
}  // namespace HugeCTR
