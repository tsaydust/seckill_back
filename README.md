# 秒杀系统 - 用户与地址管理模块

基于 **gRPC** 和 **SQLAlchemy** 实现的用户管理及地址管理模块，适用于高并发秒杀场景的微服务架构。提供轻量级、高性能的接口服务。

---

## 📖 功能特性

- **用户管理**  
  - 用户注册、查询、更新、删除  
  - 支持基础信息（用户名、邮箱等）管理  

- **地址管理**  
  - 地址的增删改查  
  - 地址与用户的关联绑定  

- **技术亮点**  
  - **gRPC**：基于 HTTP/2 的高性能远程调用协议  
  - **SQLAlchemy ORM**：灵活安全的数据库操作抽象层  
  - **微服务架构**：模块解耦，易于扩展  

---

## 🛠️ 技术栈

- **核心框架**: Python 3.12+  
- **通信协议**: gRPC / Protocol Buffers  
- **数据库**: SQLAlchemy (支持 SQLite/MySQL/PostgreSQL)  
- **工具链**: `grpcio`, `grpcio-tools`, `sqlalchemy`  

---

## 🚀 快速开始

### 环境准备

1. 克隆仓库：
   ```bash
   git clone https://github.com/tsaydust/seckill_back.git
