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

#pragma once

#include <core23/allocator.hpp>
#include <core23/buffer_requirements.hpp>
#include <core23/device.hpp>
#include <map>
#include <memory>

namespace HugeCTR {

namespace core23 {

class BufferClient;
class OffsettedBuffer;

class Buffer : public std::enable_shared_from_this<Buffer> {
 private:
  class AccessKey {
    friend class OffsettedBuffer;

   private:
    AccessKey() {}
    AccessKey(const AccessKey&) = default;
  };

 public:
  Buffer(const Device& device, std::unique_ptr<Allocator> allocator)
      : device_(device), allocator_(std::move(allocator)) {}
  virtual ~Buffer();

  void subscribe(BufferClient* client, BufferRequirements requirements);
  void allocate();

  bool subscribable() const { return allocator_ && subscribable_impl(); }
  bool allocatable() const {
    return allocator_ && !new_client_requirements_.empty() && allocatable_impl();
  }

  inline void* data(int64_t offset, AccessKey) const { return data_impl(offset); }

  virtual std::pair<void*, int64_t> decay() const { return std::make_pair(nullptr, 0LL); }
  size_t reserved_size() { return do_get_reserved_size(allocator_, new_client_requirements_); };

 protected:
  using ClientOffsets = std::map<BufferClient*, int64_t>;
  using ClientRequirements = std::map<BufferClient*, BufferRequirements>;

  const std::unique_ptr<Allocator>& allocator() const { return allocator_; }
  virtual size_t do_get_reserved_size(const std::unique_ptr<Allocator>& allocator,
                                      const ClientRequirements& client_requirements) {
    return 0;
  };

 private:
  void unsubscribe(BufferClient* client);

  virtual void* data_impl(int64_t offset) const = 0;
  virtual ClientOffsets do_allocate(const std::unique_ptr<Allocator>& allocator,
                                    const ClientRequirements& client_requirements) = 0;

  virtual bool subscribable_impl() const { return true; }
  virtual bool allocatable_impl() const { return true; }

  virtual void post_subscribe(const BufferClient* client, BufferRequirements requirements) {}
  virtual void post_unsubscribe(const BufferClient* client, const BufferRequirements& requirements,
                                int64_t offset) {}

  ClientRequirements served_client_requirements_;
  ClientRequirements new_client_requirements_;
  ClientOffsets client_offsets_;

  Device device_;
  std::unique_ptr<Allocator> allocator_;
};

}  // namespace core23

}  // namespace HugeCTR
