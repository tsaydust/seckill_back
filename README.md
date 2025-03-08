# 秒杀系统 - 用户与地址管理微服务

基于 **gRPC** 的分布式用户管理微服务，采用 **雪花算法** 生成唯一用户ID，通过 **Consul** 实现服务治理，结合 **SQLAlchemy ORM** 与 **Redis 缓存**，为秒杀系统提供高可用、易扩展的基础服务支撑。

---

## 📖 功能特性

- **用户管理**  
  - 用户注册、查询、更新、删除  
  - 支持基础信息（用户名、邮箱等）管理  

- **地址管理**  
  - 地址的增删改查  
  - 地址与用户的关联绑定  

## 🌟 核心升级

### 分布式架构增强
- **雪花算法**：生成全局唯一用户ID，解决分库分表场景ID冲突问题
- **Consul 集成**：服务自动注册与健康检查，支持动态服务发现

### 性能优化
- **gRPC 流式处理**：高效处理批量用户数据操作
- **Redis 二级缓存**：用户信息缓存加速查询效率


---

## 🛠️ 技术架构

| 组件                | 说明                                                                 |
|---------------------|--------------------------------------------------------------------|
| **通信协议**        | gRPC (HTTP/2 + Protocol Buffers)                                  |
| **服务治理**        | Consul 实现服务注册/发现/健康检查                                 |
| **分布式ID**        | 雪花算法（可配置 worker_id/datacenter_id）                        |
| **数据库**          | SQLAlchemy ORM 支持 MySQL/PostgreSQL                             |
| **缓存**            | Redis 6.2+ (用户信息缓存/分布式锁)                               |
| **安全**            | JWT 鉴权                                           |

---

