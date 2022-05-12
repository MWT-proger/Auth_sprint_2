from typing import Optional

import grpc
from core import config
from grpc_client import AuthService_pb2_grpc

channel = grpc.aio.insecure_channel(f"{config.GRPC_HOST}:{config.GRPC_PORT}")
stub: Optional[AuthService_pb2_grpc.AuthStub] = None


async def get_stub() -> AuthService_pb2_grpc.AuthStub:
    return stub
