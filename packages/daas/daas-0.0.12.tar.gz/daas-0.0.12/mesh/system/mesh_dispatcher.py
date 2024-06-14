#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from typing import Any, Dict, Type

from mesh.macro import spi, T
from mesh.prsim import Dispatcher


@spi("mesh")
class MeshDispatcher(Dispatcher):

    async def reference(self, mpi: Type[T]) -> T:
        pass

    async def invoke(self, urn: str, param: Dict[str, Any]) -> Any:
        pass

    async def invoke_generic(self, urn: str, param: Any) -> Any:
        pass
