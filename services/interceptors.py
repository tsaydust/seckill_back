from grpc_interceptor.exceptions import GrpcException
from grpc_interceptor import AsyncServerInterceptor
from typing import Any, Callable
import grpc
from models import AsyncSessionFactory

class UserInterceptors(AsyncServerInterceptor):
    async def intercept(
            self,
            method: Callable,
            request_or_iterator: Any,
            context: grpc.ServicerContext,
            method_name: str,
    ) -> Any:
        session = AsyncSessionFactory()
        try:
            response = await method(request_or_iterator, context, session)
            return response
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
        finally:
            await session.close()