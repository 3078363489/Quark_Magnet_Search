-- 先创建数据库（确保你要导入数据的数据库存在）
CREATE DATABASE IF NOT EXISTS Magnet_Search CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户并授权（与docker-compose.yml环境变量保持一致）
GRANT ALL PRIVILEGES ON Magnet_Search.* TO 'Magnet_Search'@'%' IDENTIFIED BY '12345678';
FLUSH PRIVILEGES;