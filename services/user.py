import grpc
import sqlalchemy.exc
from sqlalchemy import select, update
from protos import user_pb2, user_pb2_grpc
from models import AsyncSessionFactory
from models.user import User
from google.protobuf import empty_pb2
from utils.pwdutil import hash_pwd, verify_pwd
from loguru import logger

class UserServicer(user_pb2_grpc.UserServicer):
    async def CreateUser(self, request: user_pb2.CreateUserRequest, context, session):
        mobile = request.mobile
        try:
            async with session.begin():
                user = User(mobile=mobile)
                session.add(user)
            response = user_pb2.UserInfoResponse(user=user.to_dict())
            return response
        except sqlalchemy.exc.IntegrityError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('该错误已经存在')

    async def GetUserById(self, request: user_pb2.GetUserByIdRequest, context, session):
        try:
            async with session.begin():
                user_id = request.id
                query = await session.execute(select(User).where(User.id == user_id))
                user = query.scalar()
                if not user:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('用户不存在')
                else:
                    response = user_pb2.UserInfoResponse(user=user.to_dict())
                    return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('服务器错误')

    async def GetUserByMobile(self, request: user_pb2.GetUserByMobileRequest, context, session):
        try:
            async with session.begin():
                mobile = request.mobile
                query = await session.execute(select(User).where(User.mobile == mobile))
                user = query.scalar()
                if not user:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('用户不存在')
                else:
                    response = user_pb2.UserInfoResponse(user=user.to_dict())
                    return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('服务器错误')

    async def UpdateAvatar(self, request: user_pb2.UpdateAvatarRequest, context, session):
        user_id = request.id
        avatar = request.avatar
        try:
            async with session.begin():
                stmt = update(User).where(User.id == user_id).values(avatar=avatar)
                query = await session.execute(stmt)
                rowcount = query.rowcount
                if rowcount == 0:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'ID{user_id}不存在！')
                else:
                    return empty_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('服务器错误')

    async def UpdateUsername(self, request: user_pb2.UpdateAvatarRequest, context, session):
        user_id = request.id
        username = request.username
        try:
            async with session.begin():
                stmt = update(User).where(User.id == user_id).values(username=username)
                query = await session.execute(stmt)
                rowcount = query.rowcount
                if rowcount == 0:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'ID{user_id}不存在！')
                else:
                    return empty_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('服务器错误')

    async def UpdatePassword(self, request: user_pb2.UpdatePasswordRequest, context, session):
        user_id = request.id
        password = request.password
        hashed_password = hash_pwd(password)
        try:
            async with session.begin():
                stmt = update(User).where(User.id == user_id).values(password=hashed_password)
                query = await session.execute(stmt)
                rowcount = query.rowcount
                if rowcount == 0:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'ID{user_id}不存在！')
                else:
                    return empty_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('服务器错误')

    async def VerifyUser(self, request: user_pb2.VerifyUserRequest, context, session):
        mobile = request.mobile
        password = request.password
        async with session.begin():
            query = await session.execute(select(User).where(User.mobile == mobile))
            user = query.scalar()
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'用户不存在！')
            if not verify_pwd(password, user.password):
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('密码错误！')
            response = user_pb2.UserInfoResponse(user=user.to_dict())
            return response

    async def GetUserList(self, request: user_pb2.GetUserPageRequest, context, session):
        page = request.page
        size = request.size
        offset = (page - 1) * size
        async with session.begin():
            query = await session.execute(select(User).limit(size).offset(offset))
            results = query.scalars().fetchall()
            users = []
            for user in results:
                users.append(user.to_dict())
            response = user_pb2.UserListResponse(users=users)
            return response


    async def GetOrCreateUserByMobile(self, request: user_pb2.GetUserByMobileRequest, context, session):
        async with session.begin():
            mobile = request.mobile
            query = await session.execute(select(User).where(User.mobile == mobile))
            user = query.scalar()
            if not user:
                user = User(mobile=mobile)
                session.add(user)
        response = user_pb2.UserInfoResponse(user=user.to_dict())
        logger.info('收到！')
        return response
