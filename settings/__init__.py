MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DB = 'sec_kill_user_db'

# aiomysql
# pip install aiomysql
# asyncmy：在保存64位的整形时，有bug：Unexpected <class 'OverflowError'>: Python int too large to convert to C unsigned long
DB_URI = f"mysql+asyncmy://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

# 这个地方是写死的，后续如果部署到服务器上，可以使用读取环境变量的形式
DATACENTER_ID = 0
WORKER_ID = 0