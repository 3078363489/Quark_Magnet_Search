# V1.0.1版本
解决移动端内容出格问题，采集文章标题重复问题

# Quark_Magnet_Search - 磁力链接搜索引擎

一个强大的磁力链接搜索引擎，集成采集API、夸克网盘智能转存与缓存管理。专为高效资源检索与分发而构建。

## 功能特性

- 🔍 **强大的搜索引擎** - 快速检索磁力链接资源
    
- 📱 **响应式设计** - 移动端直接跳转/PC端生成下载二维码
    
- 🤖 **采集API集成** - 支持火车头及自制采集工具
    
- ☁️ **夸克网盘智能转存** - 自动转存与缓存管理（支持自动清理）
    
- 📊 **数据统计** - 下载次数统计与资源热度分析
    
- 🔎 **SEO优化** - 搜索引擎友好，支持站点地图

## 用户名 admin 密码admin123456

## 技术栈

- Python 3.8.10
    
- Django框架
    
- MySQL 8.0
    
- 支持宝塔面板、1Panel部署
    

## 项目预览

[https://github.com/user-attachments/assets/4a24b5b1-b9b8-4a29-9964-8b1e1df66d0e](https://github.com/user-attachments/assets/4a24b5b1-b9b8-4a29-9964-8b1e1df66d0e)  
_PC端界面 - 直接跳转功能_

[https://github.com/user-attachments/assets/52e1b914-89f1-418f-80ad-f7d4c24f94f9](https://github.com/user-attachments/assets/52e1b914-89f1-418f-80ad-f7d4c24f94f9)  
_PC端界面 - 生成下载二维码_

[https://github.com/user-attachments/assets/a4d79d12-a5fb-45ae-ba1d-bf51d9fe1a3b](https://github.com/user-attachments/assets/a4d79d12-a5fb-45ae-ba1d-bf51d9fe1a3b)  
_资源详情页面_

## 后台管理

[https://github.com/user-attachments/assets/acdf2bb0-3560-4d3d-8b32-2964ade634b1](https://github.com/user-attachments/assets/acdf2bb0-3560-4d3d-8b32-2964ade634b1)  
_后台管理界面 - 数据概览_

[https://github.com/user-attachments/assets/b2b3a5d2-e85b-4464-ab08-e19703ea9e30](https://github.com/user-attachments/assets/b2b3a5d2-e85b-4464-ab08-e19703ea9e30)  
_后台管理界面 - 资源管理_

## 安装部署

### 环境要求

- Python 3.8.10
    
- MySQL 8.0
    
- Django框架
    

### 数据库配置

在 `Magnet_Search/settings.py` 中配置数据库连接：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'magnet_Search',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '12345678'
    }
}

```
### 域名配置

使用前请修改 `Magnet_Search/settings.py` 中的CSRF信任源：

```python

CSRF_TRUSTED_ORIGINS = [
    'http://quark.marketingw.cn',  # 改为自己的域名
]

```
## API接口

### 定时清理任务

```text

https://域名/quark/qurak_Cache/定时删除夸克转存文件

默认1小时清理一次（可在 `./quark/views.py` 中配置）
timezone.now() - timedelta(hours=1)中的1表示1小时
```

### 采集接口

```text

https://域名/API/article_create/

采集接口的密钥在后台Keys中设置

[https://github.com/user-attachments/assets/8c736666-4dc4-4b4f-acb6-09f2f535159b](https://github.com/user-attachments/assets/8c736666-4dc4-4b4f-acb6-09f2f535159b)  
_火车头采集器配置示例_
```

## 资源文件

当前目录下提供：

- 火车头发布模块
    
- 采集规则模板
    

## 项目结构

```text
Quark_Magnet_Search/
├── Magnet_Search/
│   ├── settings.py      # 项目配置
│   └── ...
├── quark/
│   ├── views.py         # 视图函数
│   └── ...
├── API/                 # API接口
└── ...                  # 其他模块
```

## 有问题微信联系
![ccb16e1d1953b60151eb9070641d7e6f](https://github.com/user-attachments/assets/c4c68362-3fc6-4e02-9bc4-1b1b709d1215)


## 演示网站:http://quark.marketingw.cn/
