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

#include <hps/message.hpp>

namespace HugeCTR {

template <typename Key>
void MessageSinkBase<Key>::post(const std::string& tag, const size_t num_pairs,
                                const Key* const keys, const char* const values,
                                const uint32_t value_size) {
  num_posts_++;
  num_pairs_posted_ += num_pairs;
}

template <typename Key>
void MessageSinkBase<Key>::flush() {
  num_flushes_++;
}

template class MessageSinkBase<unsigned int>;
template class MessageSinkBase<long long>;

}  // namespace HugeCTR