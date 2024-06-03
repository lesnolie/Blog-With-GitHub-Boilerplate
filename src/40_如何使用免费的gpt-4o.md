---
layout: post
title: 如何使用免费的gpt-4o
slug: 如何使用免费的gpt-4o
date: 2024-06-03 08:00
status: publish
author: Leslie
categories: 
  - stand 
tags:
  - stand 
  - stand 
excerpt: 
---

## 非API
coze 可以免费使用。

## API
需要部署以下几个工具。

### 必须
- [chat2api](https://github.com/lanqian528/chat2api)
- [one-api](https://github.com/MartialBE/one-api)
- 注册 [Burn.hair](https://burn.hair/)

### 非必需
- 部署 [cloudflare_temp_email](https://github.com/berstend/CFTempEmail)（用于注册chatgpt）

### 客户端
- 推荐 [Chatbox](https://github.com/Bin-Huang/chatbox)，你也可以使用其他的客户端。

## chat2api部署步骤

### Docker Compose 部署
1. 创建一个新的目录，例如 `chat2api`，并进入该目录：
```sh
   mkdir chat2api
   cd chat2api
```
2. 在此目录中下载库中的 docker-compose.yml 文件：
```sh
   wget https://raw.githubusercontent.com/LanQian528/chat2api/main/docker-compose.yml
```
修改 docker-compose.yml 文件中的环境变量，保存后：
```
docker-compose up -d
```
使用
在网页使用，直接访问以下地址:

```
http://127.0.0.1:5005
```
使用 API，支持传入 AccessToken 或 RefreshToken，可用 GPT-4, GPT-4o, GPTs：

```
curl --location 'http://127.0.0.1:5005/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{OpenAI APIKEY}}' \
--data '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "stream": true
   }'
```
将你账号的 AccessToken 或 RefreshToken 当作 OpenAI APIKEY 传入。
如果设置了 AUTHORIZATION 环境变量，可以将设置的值当作 OpenAI APIKEY 传入进行多 Tokens 轮询。
AccessToken 获取: chatgpt 登录后，再打开 [session API](https://chatgpt.com/api/auth/session) 获取 accessToken 值。
免登录 gpt-3.5 无需传入 Token。

## 使用cloudflare_temp_email

由于chatgpt-4o非plus用户只能3小时10条，所以使用临时邮箱注册4个账号，达到3消失40条。

## 部署 open-api
使用 Docker Compose 进行部署
注意：虽然启动方式有所不同，但参数设置保持不变。具体的参数设置请参考基于 Docker 部署部分。

在你本机创建一个目录用于存放数据，例如 /home/ubuntu/data/one-api，注意：以下操作都是基于你处于 /home/ubuntu/data/one-api 目录下进行的。如果你的目录不是 /home/ubuntu/data/one-api，请自行进入到你的目录。

```<SH>
mkdir -p ./data/mysql
mkdir -p ./data/one-api
```
下载 docker-compose.yml 文件到你的本地目录（上面的列子是：/home/ubuntu/data/one-api）。

修改 docker-compose.yml 文件，将你需要的环境变量填入。如果你想使用配置文件，可以下载配置文件，并重命名为 config.yaml 放入 ./data/one-api 目录中。

启动服务：

```<SH>
docker-compose up -d
```
启动服务后，你可以通过运行以下命令来查看部署状态：

```<SH>
docker-compose ps
```
请确保所有的服务都已经成功启动，并且状态为 'Up'。 

## 使用
将 burn.hair 和导入 one-api

## 客户端使用
使用 One-api 的地址和令牌即可。
   

[如何使用免费的gpt-4o](https://github.com/lesnolie/Marverick/issues/40)

