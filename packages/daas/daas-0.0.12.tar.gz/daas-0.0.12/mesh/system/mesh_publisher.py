#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from typing import List

from mesh.kinds import Event
from mesh.macro import spi
from mesh.mpc import ServiceProxy
from mesh.prsim import Publisher


@spi("mesh")
class MeshPublisher(Publisher):

    def __init__(self):
        self.proxy = ServiceProxy.default_proxy(Publisher)

    async def publish(self, events: List[Event]) -> List[str]:
        return await self.proxy.publish(events)

    async def broadcast(self, events: List[Event]) -> List[str]:
        return await self.proxy.broadcast(events)
