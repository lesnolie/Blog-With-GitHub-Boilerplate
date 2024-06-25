---
layout: post
title: 搭建Hysteria2版本gost实现高速中转
slug: build-hysteria2-gost-high-speed-proxy
date: 2024-06-08 08:00
status: publish
author: Leslie
categories: 
  - stand 
tags:
  - stand 
  - stand 
excerpt: 
---

GOST可以中转流量，无论是直接转发还是加密隧道转发，都是一个非常好的工具，能够解决我们日常某些节点无法访问的情况。但是GOST由于加密解密以及协议，速度不甚理想，已知hysteria基于UDP，速度非常的快。那么是否可以两者相结合？

[happyharryh/gost][]该项目就解决了这个问题。  

---

## 使用方法
### [Connector/Transporter] WireGuard  

**用法**
```
./gost -L :8080 -F wg://?c=proxy.conf
```
- 仅支持作为WireGuard客户端，且只能作为代理链的第一级。
- proxy.conf配置请参考 [wireproxy][]。

### [Listener/Transporter] Hysteria-QUIC
**使用Apernet魔改的quic-go加快QUIC传输速度**  
其他参数

- send_mbps: 数据发送速率，等于0则使用BBR(默认)，大于0则使用Brutal
- recv_window_conn: 流接收窗口大小
- recv_window: 连接接收窗口大小
- max_conn_client (仅服务端): 单客户端最大活跃连接数
- cipher: 考虑到QUIC本身自带TLS加密，这里将原版gost的cipher算法简化，提升性能

### [Handler/Connector] Zero

> 极简化连接逻辑，实现0-RTT连接  

**用法**
服务端
```
./gost -L zero://:1234
```
客户端
```
./gost -L :8080 -F zero://server_ip:1234
```
其他参数

 - mitm (仅客户端): 使用中间人(MITM)协助握手的地址列表，可缩减端到端TLS握手产生的RTT，格式同路由控制
 - mitm_caroot (仅客户端): 根证书路径，默认为~/.mitmproxy，需要将该目录下的mitmproxy-ca-cert.cer添加为受信任的根证书颁发机构证书
 - mitm_insecure (仅客户端): 是否跳过网站证书验证

**[其他]**
- 添加 -R 命令行参数，用于指定重试次数

- 添加 LOGFLAGS 环境变量，用于自定义日志输出格式

- 修复单独使用 0.0.0.0 或 [::] 时会同时监听两者的问题

- Bypass 添加 resolve 选项，用于使IP/CIDR规则匹配解析后的域名

克隆说明
本 Fork 包含 git 子仓库，克隆时需要增加 --recursive 选项

```
git clone --recursive https://github.com/happyharryh/gost.git
```
在 Windows 平台克隆后，还需要手动重建一次软链接

```
cd gost
git -c core.symlinks=true checkout .
```
## 实例：本地软路由和国外静态IP互通
我自己将本地软路由和国外静态IP通过gost互通，使用如下指令：

本地命令：
```
nohup ./gost -L=socks5://:6666 -F='quic://xxxx:port?send_mbps=50&keepalive=true' > gost_client.log 2>&1 &
```
将本地和日本服务器连接到一起。

日本服务器命令：

```
/root/gost_hy/gost/gost -L=quic://:port?send_mbps=100 -F socks5://156.xxxx:port
```
通过以上配置，能够实现高速稳定的中转，解决某些节点无法访问的问题，同时利用Hysteria-QUIC的大幅提升传输速度。

[happyharryh/gost]:https://github.com/happyharryh/gost
[wireproxy]:https://github.com/pufferffish/wireproxy/blob/master/README.md

[搭建Hysteria2版本gost实现高速中转](https://github.com/lesnolie/Marverick/issues/41)

