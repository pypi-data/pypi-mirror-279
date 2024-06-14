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

#include <common.hpp>
#include <functional>

namespace HugeCTR {

struct MessageSinkParams {};

/**
 * Each instance represents an emitter link to a theoretically infinitely sized message queue..
 *
 * @tparam Key Data-type to be used for keys in this message queue.
 */
template <typename Key>
class MessageSinkBase {
 public:
  HCTR_DISALLOW_COPY_AND_MOVE(MessageSinkBase);

  MessageSinkBase() = default;

  virtual ~MessageSinkBase() = default;

  /**
   * Emit one or more key/value pairs to the queue.
   *
   * @param tag A tag under which the key/value pairs should be filed.
   * @param num_pairs The number of \p keys and \p values .
   * @param keys Pointer to the keys.
   * @param values Pointer to the values.
   * @param value_size The size of each value in bytes.
   */
  virtual void post(const std::string& tag, size_t num_pairs, const Key* keys, const char* values,
                    uint32_t value_size);

  /**
   * Blocks the caller until all previously posted messages have been sent.
   */
  virtual void flush();

  size_t num_posts() const { return num_posts_; }
  size_t num_pairs_posted() const { return num_pairs_posted_; }
  size_t num_flushes() const { return num_flushes_; }

 private:
  size_t num_posts_ = 0;
  size_t num_pairs_posted_ = 0;
  size_t num_flushes_ = 0;
};

template <typename Key, typename Params>
class MessageSink : public MessageSinkBase<Key> {
 public:
  using Base = MessageSinkBase<Key>;

  HCTR_DISALLOW_COPY_AND_MOVE(MessageSink);

  MessageSink() = delete;

  MessageSink(const Params& params) : params_{params} {}

  virtual ~MessageSink() = default;

 protected:
  const Params params_;
};

/**
 * Each instance represents an consumer link to a theoretically infinitely sized message queue..
 *
 * @tparam Key Data-type to be used for keys in this message queue.
 */
template <typename Key>
class MessageSource {
 public:
  using Callback = void(const std::string&, const size_t, const Key*, const char*, const size_t);

  HCTR_DISALLOW_COPY_AND_MOVE(MessageSource);

  MessageSource() = default;

  virtual ~MessageSource() = default;

  /**
   * Start listening to the message queue and invoke function for each message received.
   *
   * @param callback Callback function be invoked for each received message.
   */
  virtual void engage(std::function<Callback> callback) = 0;
};

}  // namespace HugeCTR