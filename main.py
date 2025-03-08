import grpc
from services.user import UserServicer
from services.address import AddressService
from protos import user_pb2_grpc, address_pb2_grpc
import asyncio
from services.interceptors import UserInterceptors
from utils.custom_consul import CustomConsul


# interceptors = [UserInterceptors()]

async def main():
    server = grpc.aio.server(interceptors=[UserInterceptors()])
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    address_pb2_grpc.add_AddressServicer_to_server(AddressService(), server)
    async with CustomConsul() as service:
        port = service.get_port()
        server.add_insecure_port(f"0.0.0.0:{port}")
        print(port)
        await server.start()
        service.register()
        await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(main())
