import grpc
from sqlalchemy.testing import rowset

from protos import address_pb2, address_pb2_grpc
from sqlalchemy import delete, select, update
from models.address import Address
from google.protobuf import empty_pb2


class AddressService(address_pb2_grpc.AddressServicer):
    async def CreateAddress(self, request: address_pb2.CreateAddressRequest, context, session):
        user_id = request.user_id
        realname = request.realname
        mobile = request.mobile
        region = request.region
        detail = request.detail
        try:
            async with session.begin():
                address = Address(
                    realname=realname,
                    mobile=mobile,
                    region=region,
                    detail=detail,
                    user_id=user_id
                )
                session.add(address)
            response = address_pb2.AddressResponse(address=address.to_dict())
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('用户不存在！')

    async def DeleteAddress(self, request: address_pb2.DeleteAddressRequest, context, session):
        id = request.id
        user_id = request.user_id
        async with session.begin():
            stmt = delete(Address).where(Address.id == id, Address.user_id == user_id)
            query = await session.execute(stmt)
            if query.rowcount == 0:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('地址不存在！')
            return empty_pb2.Empty()

    async def UpdateAddress(self, request: address_pb2.UpdateAddressRequest, context, session):
        id = request.id
        realname = request.realname
        mobile = request.mobile
        region = request.region
        detail = request.detail
        user_id = request.user_id
        async with session.begin():
            stmt = update(Address).where(Address.id == id, Address.user_id == user_id).values(
                id=id,
                realname=realname,
                mobile=mobile,
                region=region,
                detail=detail
            )
            query = await session.execute(stmt)
            if query.rowcount == 0:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("地址异常！")
            return empty_pb2.Empty()

    async def GetAddressById(self, request: address_pb2.AddressIdRequest, context, session):
        id = request.id
        user_id = request.user_id
        async with session.begin():
            stmt = select(Address).where(Address.id == id, Address.user_id == user_id)
            query = await session.execute(stmt)
            address = query.scalar()
            return address_pb2.AddressResponse(address=address.to_dict())

    async def GetAddressList(self, request: address_pb2.AddressListRequest, context, session):
        user_id = request.user_id
        size = request.size
        page = request.page
        offset = (page - 1) * size
        async with session.begin():
            stmt = select(Address).where(Address.user_id == user_id).offset(offset).limit(size)
            query = await session.execute(stmt)
            rows = query.scalars()
            addresses = []
            for row in rows:
                addresses.append(row.to_dict())
        return address_pb2.AddressListResponse(addresses=addresses)
