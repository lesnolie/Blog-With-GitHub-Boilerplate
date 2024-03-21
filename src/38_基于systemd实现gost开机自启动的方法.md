---
layout: post
title: 基于systemd实现gost开机自启动的方法
slug: 基于systemd实现gost开机自启动的方法
date: 2024-03-21 08:00
status: publish
author: Leslie
categories: 
  - stand 
tags:
  - stand 
  - stand 
excerpt: 
---

**由于adspower可以使用sock5代理，所以在两个vps上使用gost创建socks5代理。**

## 打开[Gost仓库][],使用脚本安装gost
```
# 安装最新版本 [https://github.com/go-gost/gost/releases](https://github.com/go-gost/gost/releases)
bash <(curl -fsSL https://github.com/go-gost/gost/raw/master/install.sh) --install
```
> [!NOTE] 
> 如果你是国内服务器，可以自己复制install.sh里面的代码到机器，然后添加自己的github加速地址
> ![image][1]


## 利用systemd讲gost开机启动
**添加service文件**
```
nano /etc/systemd/system/gost.service
```
**内容如下**
```
[Unit]
Description=GOSTv3-Server of GO simple tunnel
Documentation=https://gost.run/
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/gost -L socks5://username:password@:port_num  #修改为自己要使用的gost模式，这里我使用的是socks5
Restart=always
[Install]
WantedBy=multi-user.target
```
**重现加载文件**
```
systemctl daemon-reload
```
**设置开机启动**
```
systemctl enable gost.service 
```
**启动**
```
systemctl start gost.service
```
**查看状态**
```
systemctl status gost.service
```
**使用systemctl管理gost服务的完整用例如下：**
```
# 开机启动
systemctl enable gost.service
# 关闭开机启动
systemctl disable gost.service
# 启动服务
systemctl start gost.service
# 停止服务
systemctl stop gost.service
# 重启服务
systemctl restart gost.service
# 查看服务状态
systemctl status gost.service
systemctl is-active gost.service
# 结束服务进程(服务无法停止时)
systemctl kill gost.service
```

[Gost仓库]: https://github.com/go-gost/gost
[1]:  https://github.com/lesnolie/Marverick/assets/81410185/113c7666-e133-471c-9b93-732b8b7b41fc

[基于systemd实现gost开机自启动的方法](https://github.com/lesnolie/Marverick/issues/38)

