/* Copyright 2015 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_CORE_LIB_IO_INPUTBUFFER_H_
#define TENSORFLOW_CORE_LIB_IO_INPUTBUFFER_H_

#include "tensorflow/core/platform/coding.h"
#include "tensorflow/core/platform/env.h"
#include "tensorflow/core/platform/macros.h"
#include "tensorflow/core/platform/status.h"
#include "tensorflow/core/platform/types.h"
#include "tsl/lib/io/inputbuffer.h"

namespace tensorflow {
namespace io {
using tsl::io::InputBuffer;  // NOLINT(misc-unused-using-decls)
}
}

#endif  // TENSORFLOW_CORE_LIB_IO_INPUTBUFFER_H_
