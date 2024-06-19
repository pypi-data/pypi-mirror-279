#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ContainerStoppedMetadata:
    stopped_at: str
    stop_code: str
    stopped_reason: str
