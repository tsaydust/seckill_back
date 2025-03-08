import grpc

from protos import user_pb2_grpc, user_pb2, address_pb2, address_pb2_grpc


def test_create_user(stub):
    try:
        request = user_pb2.CreateUserRequest()
        request.mobile = "18899990000"
        response = stub.CreateUser(request)
        print(response)
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())


def test_get_user_by_id(stub):
    request = user_pb2.GetUserByIdRequest(id=1876290090435608576)
    # request.id = 1876290090435608576
    response = stub.GetUserById(request)
    print(response)


def test_get_user_by_mobile(stub):
    request = user_pb2.GetUserByMobileRequest(mobile="18569815207")
    # request.id = 1876290090435608576
    response = stub.GetUserByMobile(request)
    print(response)


def test_update_avatar(stub):
    request = user_pb2.UpdateAvatarRequest(id=1876290090435608576, avatar="!234423")
    response = stub.UpdateAvatar(request)
    print(response)


def test_update_username(stub):
    request = user_pb2.UpdateUsernameRequest(id=1876290090435608576, username="蔡沲尘")
    response = stub.UpdateUsername(request)
    print(response)


def test_update_password(stub):
    request = user_pb2.UpdatePasswordRequest()
    request.id = 1876290090435608576
    request.password = '111111'
    response = stub.UpdatePassword(request)
    print(response)


def test_verify_user(stub):
    request = user_pb2.VerifyUserRequest()
    request.mobile = '18569815207'
    request.password = '111111'
    response = stub.VerifyUser(request)
    print(response)


def test_get_user_list(stub):
    request = user_pb2.GetUserPageRequest()
    request.page = 2
    request.size = 5
    response = stub.GetUserList(request)
    print(response)


def test_get_or_create_user(stub):
    request = user_pb2.GetUserByMobileRequest()
    request.mobile = '18899990002'
    response = stub.GetOrCreateUserByMobile(request)
    print(response.user.id)


# def test_create_address(stub):
#     request = address_pb2.CreateAddressRequest()
#     request.user_id = 1875875733700608000
#     request.realname = "蔡沲尘"
#     request.mobile = "18569815207"
#     request.region = '北京市朝阳区',
#     request.detail = '白家庄东里',
#     response = stub.CreateAddress(request)
#     print(response.address)

def test_create_address(stub):
    request = address_pb2.CreateAddressRequest(
        user_id=1875875733700608000,
        realname='孙悟空',
        mobile='18569815207',
        region='北京市朝阳区',
        detail='白家庄东里',
    )
    response = stub.CreateAddress(request)
    print(response.address)


def test_update_address(stub):
    request = address_pb2.UpdateAddressRequest()
    request.id = "8f07ea2f7fcf443baf2b1c50ae9a24ac"
    request.realname = "蔡沲尘"
    request.mobile = "18569815207"
    request.region = '河南省信阳市'
    request.detail = '白家庄东里'
    request.user_id = 1875875733700608000
    response = stub.UpdateAddress(request)
    print(response)


def test_delete_address(stub):
    request = address_pb2.DeleteAddressRequest(
        id="8f07ea2f7fcf443baf2b1c50ae9a24ac",
        user_id=1875875733700608000
    )
    stub.DeleteAddress(request)


def test_get_address(stub):
    request = address_pb2.AddressIdRequest(id="5ff10019b7774f6b83d065b10b784cf1", user_id=1875875733700608000)
    response = stub.GetAddressById(request)
    print(response)

def test_get_list_address(stub):
    requset = address_pb2.AddressListRequest(user_id=1875875733700608000, page=5, size=2)
    response = stub.GetAddressList(requset)
    print(response)


def main():
    with grpc.insecure_channel("127.0.0.1:5001") as channel:
        # stub = user_pb2_grpc.UserStub(channel)
        # test_create_user(stub)
        # test_get_user_by_id(stub)
        # test_get_user_by_mobile(stub)
        # test_update_avatar(stub)
        # test_update_username(stub)
        # test_update_password(stub)
        # test_verify_user(stub)
        # test_get_user_list(stub)
        # test_get_or_create_user(stub)

        stub = address_pb2_grpc.AddressStub(channel)
        # test_create_address(stub)
        # test_update_address(stub)
        # test_delete_address(stub)
        # test_get_address(stub)
        test_get_list_address(stub)


if __name__ == '__main__':
    main()
