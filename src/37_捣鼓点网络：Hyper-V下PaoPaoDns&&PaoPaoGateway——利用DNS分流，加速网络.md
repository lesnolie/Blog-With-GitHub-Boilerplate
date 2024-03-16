---
layout: post
title: 捣鼓点网络：Hyper-V下PaoPaoDns&&PaoPaoGateway——利用DNS分流，加速网络
slug: 捣鼓点网络：Hyper-V下PaoPaoDns&&PaoPaoGateway——利用DNS分流，加速网络
date: 2024-03-16 08:00
status: publish
author: Leslie
categories: 
  - stand 
tags:
  - stand 
  - stand 
excerpt: 
---

为什么我喜欢捣鼓网络呢？一则网络确实是日常所需，最常接触；二是我能接触到的网络技术也确实简单：理解了网络拓扑，流量走向，安装相应的软件，网上还都有教程；三则事后反馈也是即时的，成就感颇高。     

最近觉得openwrt的Homeproxy不好用。我都学会了写sing-box的配置文件，却对Homeproxy束手无策。Onedrive和canva竟然都访问不了，dns还时常出岔子。于是在网上冲浪的过程中邂逅了一篇文章，文章本身介绍利用singbox和mosdns进行分流，mosdns发现国内dns就直接直连，国外dns则通过singbox的fakeip模式进行代理。效果很好，速度很快。本人搭建成功以后，谷歌网盘的下载速度能达到40/ms。  


不过我一直记得作者说的一句话：
> “因为家里只有一台openwrt设备，无法使用PaoPaoDns&&PaoPaoGateway所以才这么做”。

---

**本文主讲基于Hyper-V虚拟机下，旁路由模式进行PaoPaoDns&&PaoPaoGateway的安装设置。**

## 网络拓扑&原理

![paopaodns&&paopaogateway官方示例][1]

**优势：**
- 直连直接走主路由，只有代理才走网关。也就是说，即使paopaodns&&paopaogateway都坏了，旁路由崩溃了，因为有备用DNS的存在，你整个家庭网络系统仍然可以正常运行。
- PaoPaoGateway 不需要硬盘


![本人理解的拓扑——direct][2]


![本人理解的拓扑——prxoy][3]


而普通的openwrt，无论直连和代理，都需要走一遍openwrt，所以，速度不言而喻。

![其他拓扑解析][4]


## 安装PaoPaoDns

***基于Apline-linux安装，因为他小巧易用。***

### 一、安装 Alpine Linux
1.1. 前往 [Alpine 官网][]下载安装镜像，这里选用 Virtual 镜像（只有小小的30M+），安装完系统空间占用大概 132MB 左右；
1.2. 使用上述镜像创建一台 Hyper-V 二代虚拟机（记得关闭安全启动），并启动；
1.3. 因为Alpine刚装完是只读状态，一定要进行设置，否则重启就还原。（我在这里纠结了一下午）
**_示例设置流程_**
```
# 使用 root 超级用户直接登录
localhost login: root
# 运行 setup-alpine 安装程序
localhost:~# setup-alpine
# 询问键盘布局设置，直接输入 cn ，并回车
Select keyboard layout [none]: cn
# 询问字符集设置，直接输入 cn ，并回车
Select variant []: cn
# 询问主机名设置，如无特殊需要直接回车即可（仅能由小写英文字母及英文横杠组成）
Enter system hostname (short form, e.g. 'foo') [localhost]: 
# 选择将用于外网连接的网卡，如无特殊需，求直接回车使用默认的 eth0 即可
Which one do you want to initialize? (or '?' or 'done') [eth0]
# 询问主机 IP 获取方式，如无特殊需求，直接回车使用默认的 DHCP 获取方式即可
Ip address for eth0? (or 'dhcp', 'none', '?') [dhcp] 
# 询问是否需要手动配置其它特殊的网络设置，无特殊需求直接回车，默认“否”即可
Do you want to do any manual network configuration? [no]
# 设置 root 超级用户密码（需重复一遍，不能是弱密码，位数要求高于六位，为了安全设置时不显示任何字符）
Changing password for root
New password: 
Retype password: 
# 询问时区设置，直接输入 Asia/Shanghai 并回车即可
Which timezone are you in? ('?' for list) [UTC] Asia/Shanghai
# 询问是否设置 HTTP/FTP 代理，无特殊需求直接回车不配置即可
HTTP/FTP proxy URL? (e.g. 'http://proxy:8080', or 'none') [none]
# 询问软件包镜像源配置，国内的推荐选择域名后缀为 edu.cn 的其中一个，根据自己的网络来选
Enter mirror number (1-44) or URL to add (or r/f/e/done) [f]: 23
# 询问使用哪个 SSH server 程序，无特殊需求直接回车使用默认的 openssh 即可
Which SSH server? ('openssh', 'dropbear' or 'none') [openssh] 
# 询问使用哪个 NTP client 时间同步校对客户端，无特殊需求直接回车使用默认的 chrony 即可
Which NTP client to run? ('busybox', 'openntpd', 'chrony' or 'none') [chrony] 
# 询问将哪块硬盘用于配置 Alpine Linux 环境，根据自己需求输入对应硬盘并回车即可
Which disk(s) would you like to use? (or '?' for help or 'none') [none] sda
# 询问上面选择的硬盘用途，直接输入 sys 并回车用于安装 Alpine Linux 系统即可
How would you like to use it? ('sys', 'data', 'lvm' or '?' for help) [?] sys
# 告知将格式化整块磁盘，询问是否继续，输入 y 并回车选择“是”继续即可
WARNING: Erase the above disk(s) and continue? [y/N]: y

# 之后就是等待安装完成提示重启即可（记得提前弹出CD-ROM/DVD）
reboot
```
注：弹出CD-ROM/DVD需要在HYPER-V，Alpine的设置处弹出，这里不再进行截图，请自行寻找。
 
1.4. 设置网络：setup-interfaces，设置IP，这个IP就是以后你的DNS的IP。**比如我设置的是192.168.50.2**

### 二、安装docker

有一个[Alpine的脚本][]，但是这个脚本我直接运行总是没效果，所以我就把脚本里面的所有命令手打了一遍，效果拔群，你们也可以试试。

### 三、安装PaoPaoDns
***如果你的网络环境访问Dokcer镜像有困难，可以尝试使用[上海交大][]的镜像。***   
官方建议使用docker-compose进行安装，方便更新以及更新配置：
#修改 192.168.50.3 为你自己的网关(你准备设置的PaoPaoGateway)地址，其他无需修改
```
version: "3"

services:
  paopaodns:
    image: sliamb/paopaodns:latest
    container_name: PaoPaoDNS
    restart: always
    volumes:
      - /home/paopaodns:/data
    environment:
      - TZ=Asia/Shanghai
      - UPDATE=weekly
      - DNS_SERVERNAME=PaoPaoDNS,blog.03k.org
      - DNSPORT=53
      - CNAUTO=yes
      - CNFALL=yes
      - CN_TRACKER=yes
      - USE_HOSTS=no
      - IPV6=no
      - SOCKS5=192.168.50.3:1080
      - SERVER_IP=10.10.10.8
      - CUSTOM_FORWARD=192.168.50.3:53
      - AUTO_FORWARD=yes
      - AUTO_FORWARD_CHECK=yes
      - USE_MARK_DATA=yes
      - HTTP_FILE=yes
    ports:
      - "53:53/udp"
      - "53:53/tcp"
      - "5304:5304/udp"
      - "5304:5304/tcp"
      - "7889:7889/tcp"
```

当然，你也可以直接使用docker进行安装（我就是这样）
```
#拉取最新的docker镜像
docker pull sliamb/paopaodns:latest
#设置环境变量
#修改 192.168.50.3 为你自己的网关(你准备设置的PaoPaoGateway)地址，其他无需修改
docker run -d \
--name paopaodns \
-v /home/mydata:/data \
-e UPDATE=weekly \
-e CNAUTO=yes \
-e CNFALL=yes \
-e CN_TRACKER=yes \
-e IPV6=no \
-e CUSTOM_FORWARD=192.168.50.3:53  \
-e  AUTO_FORWARD=yes   \
-e  AUTO_FORWARD_CHECK=yes \
-e  USE_MARK_DATA=yes \
-e  CN_TRACKER=yes \
-e  ADDINFO=yes \
-e  SHUFFLE=yes \
-e  RULES_TTL=604800 \
-e  TZ=Asia/Shanghai \
--restart unless-stopped \
-p 53:53/tcp -p 53:53/udp \
-p 5304:5304/tcp -p 5304:5304/udp \
sliamb/paopaodns
```
### 四、安装备用DNS
你可以再安装一个PaoPaodns作为备用dns，当其中一个崩溃时另一个仍能运行。
并且听说ikuai必须设置两个dns。
不知道能不能在远程运行一个PaoPaoDns作为备用Dns服务器，你可以试试，我觉得可行。....

### 五、安装PaoPaoGateway
随便找一个能运行docker的机器，刚才Alpine就可以。

创建目录
```
mkdir iso
```
进入目录
```
cd iso
```
5.1.1 network.ini配置
```
ip=192.168.50.3
mask=255.255.255.0
gw=192.168.50.1
dns1=192.168.50.2
dns2=备用DNS
```
参数解释：
> ip：PaoPaoGateWay的IP要和PaoPaoDNS的-e CUSTOM_FORWARD=192.168.50.3:53一致。
   gw：主路由的IP.
   dns1:PaoPaoDNS（主）的IP
   dns2:PaoPaoDNS（备）的IP

5.1.2 ppgw.ini配置
下面参数根据实际修改。

主要参数：
> clash_web_password="password" # 管理面板的密码password
   dns_ip=192.168.50.2 # PaoDNS（主）
   ex_dns="192.168.50.2:53" # PaoDNS（主）
   model建议使用yaml，因为clash的proxies比较容易写。


配置如下
```
#paopao-gateway

# mode=socks5|ovpn|yaml|suburl|free
# default: socks5
mode=yaml

# Set fakeip's CIDR here
# default: fake_cidr=7.0.0.0/8
fake_cidr=11.0.0.0/8

# Set your trusted DNS here
# default: dns_ip=1.0.0.1
# 使用PaoPaoDNS这里就设置PaoDNS的地址
dns_ip=192.168.50.2
# default: dns_port=53
# If used with PaoPaoDNS, you can set the 5304 port
dns_port=5304

# Clash's web dashboard
clash_web_port="80"
# Clash's 面板密码
clash_web_password="password"

# default:openport=no
# socks+http mixed 1080
openport=yes

# default: udp_enable=no
udp_enable=no

# default:30
sleeptime=30

# socks5 mode settting
# default: socks5_ip=gatewayIP
socks5_ip="192.168.8.1"
# default: socks5_port="7890"
socks5_port="7890"

# ovpn mode settting
# The ovpn file in the same directory as the ppgw.ini.
# default: ovpnfile=custom.ovpn
ovpnfile="custom.ovpn"
ovpn_username=""
ovpn_password=""

# yaml mode settting
# The yaml file in the same directory as the ppgw.ini.
# default: yamlfile=custom.yaml
yamlfile="custom.yaml"

# suburl mode settting
suburl=""
subtime=1d

# fast_node=check/yes/no
fast_node=yes
test_node_url="https://cp.cloudflare.com"
ext_node="Traffic|Expire| GB|Days|Date"
cpudelay="3000"

# dns burn setting
# depand on fast_node=yes & mode=suburl/yaml
dns_burn=yes
# If used with PaoPaoDNS, you can set the PaoPaoDNS:53
ex_dns="192.168.50.2:53"
```

5.1.3 custom.yaml配置(CLASH)
直接把你节点的proxies部分复制进来就行，但是注意复制后的格式哈。
下面是一个配置例子。
```
proxies:
- name: "hysteria2"
  type: hysteria2
  server: server.com
  port: 443
  # ports: 10000-20000/443
  #  up和down均不写或为0则使用BBR流控
  # up: "30 Mbps" # 若不写单位，默认为 Mbps
  # down: "200 Mbps" # 若不写单位，默认为 Mbps
  password: yourpassword
  # obfs: salamander # 默认为空，如果填写则开启obfs，目前仅支持salamander
  # obfs-password: yourpassword
  # sni: server.com
  # skip-cert-verify: false
  # fingerprint: xxxx
  # alpn:
  #   - h3
  # ca: "./my.ca"
  # ca-str: "xyz"

```
5.2 网关的编译

替换clash/mihomo核心
你可以把你的amd64的clash/mihomo(就是clash-meta)二进制文件重命名为clash放到当前目录即可。通过替换clash核心，你可以支持更多的协议和规则功能，比如替换为[mihomo][]。

最终你的iso文件夹会是这个样子的:

![iso文件夹][5]

在iso文件夹下执行这个命令
```
docker run --rm -v .:/data sliamb/ppgwiso
```
等待执行完成，你的PaoPaoGateWay就会出现在文件夹下了。
下载。

### 六、创建PaoPaoGateway虚拟机

#### 运行要求和配置下发
类型|要求
-|-
虚拟机CPU|x86-64
内存|最低128MB，推荐256MB
硬盘|不需要
网卡|1
光驱|1  

*注意：如果节点数量很多或者连接数很多或者你的配置文件比较复杂的话，建议适当增加内存和CPU核心数*

在hyper-新建虚拟机，**选择第一代**（重点），最后一步无需使用磁盘，完成后虚拟机设置加载刚才打包的 ISO镜像，直接光驱启动即可。

登录面板，地址为：网关IP地址/ui

![登录面板][6]


### 附我的hyper-v截图

![hyper-v截图][7]

### 七、主路由设置
需要设置一下内容：我的主路由是梅林固件，你按照你的配置

7.1 LAN-DHCP
![LAN-DHCP][8]

7.2 静态路由设置

![静态路由设置][9]

---

### 结语
看起来麻烦，实际特别简单
- 安装Alpine
- Alpine安装docker
- 安装PaoPaodns
- 编译PaoPaoGateway
- 启用PaoPaoGateway

[1]: https://github.com/lesnolie/Marverick/assets/81410185/9bd72574-0a42-445e-aa06-8e6c61c7970f
[2]: https://github.com/lesnolie/Marverick/assets/81410185/81736437-1f01-4558-a875-6bae920c31f1
[3]: https://github.com/lesnolie/Marverick/assets/81410185/3164a5d3-35e8-48fc-8740-71cad1df6310
[4]: https://github.com/lesnolie/Marverick/assets/81410185/34e73d52-d1e7-4201-b3e0-93a068bfde9e
[5]: https://github.com/lesnolie/Marverick/assets/81410185/5d39771c-87f1-4968-9d43-d4cf966441a9
[6]: https://github.com/lesnolie/Marverick/assets/81410185/78126142-0d89-48bb-936a-79e41fec2a3e
[7]: https://github.com/lesnolie/Marverick/assets/81410185/52ee282b-d10b-4c89-8ab4-b12227c15fa9
[8]: https://github.com/lesnolie/Marverick/assets/81410185/01806c1a-5cd1-4c35-9b7d-0a4587461ef1
[9]: https://github.com/lesnolie/Marverick/assets/81410185/23ee96ec-61e7-4cf2-94ef-346275b40556
[mihomo]:https://github.com/MetaCubeX/mihomo/releases
[Alpine 官网]:https://www.alpinelinux.org/downloads/
[Alpine的脚本]:https://gist.github.com/rupertbenbrook/99a02725934f91a280d154800d541634
[上海交大]:https://mirror.sjtu.edu.cn/docs/docker-registry

[捣鼓点网络：Hyper-V下PaoPaoDns&&PaoPaoGateway——利用DNS分流，加速网络](https://github.com/lesnolie/Marverick/issues/37)

