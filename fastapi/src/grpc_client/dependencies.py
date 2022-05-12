from http import HTTPStatus
from typing import Optional

import grpc
from grpc_client import AuthService_pb2, AuthService_pb2_grpc
from grpc_client.client import get_stub

from fastapi import Depends, Header, HTTPException


def get_auth_token(authorization: Optional[str] = Header(None)):
    if authorization and "Bearer" in authorization:
        return authorization.split(" ")[-1]
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="token not found")


async def get_role(token: str = Depends(get_auth_token), stub: AuthService_pb2_grpc.AuthStub = Depends(get_stub)):
    try:
        response = await stub.GetUserRole(AuthService_pb2.AuthRequest(access_key=token))
        return response.user_role
    except grpc.RpcError as error:
        if error.code() == grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="token has expired")

        if error.code() == grpc.StatusCode.FAILED_PRECONDITION:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="token is not valid")
