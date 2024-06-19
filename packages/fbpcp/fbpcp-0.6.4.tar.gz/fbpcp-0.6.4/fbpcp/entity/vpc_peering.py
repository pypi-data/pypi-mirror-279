#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


class VpcPeeringState(Enum):
    PENDING_ACCEPTANCE = "PENDING_ACCEPTANCE"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PROVISIONING = "PROVISIONING"
    INITIATING = "INITIATING"


class VpcPeeringRole(Enum):
    REQUESTER = "REQUESTER"
    ACCEPTER = "ACCEPTER"


@dataclass
class VpcPeering:
    id: str
    status: VpcPeeringState
    role: VpcPeeringRole
    requester_vpc_id: str
    accepter_vpc_id: str
    requester_vpc_cidr: Optional[str] = None
    accepter_vpc_cidr: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
