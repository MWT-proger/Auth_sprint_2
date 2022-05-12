from concurrent import futures

import AuthService_pb2
import AuthService_pb2_grpc
import grpc

from flask_jwt_extended import decode_token
from main import app
from jwt import ExpiredSignatureError
from redis_db import redis_conn
from services.role import role_service


class Auth(AuthService_pb2_grpc.AuthServicer):

    def __init__(self, app):
        self.flask_app = app

    def GetUserRole(self, request, context):
        with self.flask_app.app_context():
            token = self.validate_token(context, request.access_key)

            roles = [role.get("name") for role in role_service.get_user_role(token.get("sub"))]
            return AuthService_pb2.AuthResponse(user_role=roles)

    def validate_token(self, context, token):
        try:
            token_info = decode_token(token)
            if redis_conn.exists(f"revoked_token_{token_info['jti']}"):
                self.error(context, grpc.StatusCode.FAILED_PRECONDITION, "token is not valid")

            return token_info

        except ExpiredSignatureError as e:
            self.error(context, grpc.StatusCode.INVALID_ARGUMENT, str(e))

    def error(self, context, status, detail):
        context.set_code(status)
        context.set_details(detail)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    AuthService_pb2_grpc.add_AuthServicer_to_server(Auth(app), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
