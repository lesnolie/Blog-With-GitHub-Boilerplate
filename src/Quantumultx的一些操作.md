---
layout: post
title: Quantumultx 的一些操作
slug: Quanx
date: 2021-05-22 10:00
status: publish
author: leslie
categories: 
  - IOS
tags: 
  - IOS
  - iPhone
  - Quantumult x
excerpt: Quantumult X从零到1
---

[notice]接触Quantumult X已有3日，从0到1慢慢摸索出一些经验[/notice]

# Quantumult X

## 界面操作

- 主要按钮，右下角小风车。
- PROXY：节点
- 自定义策略：分流，国内走国内，国外走国外，app走app，可自己设置。
- 重写：rewrite，放脚本的地方。
- 工具分析：定时任务



## 操作

懒人直接倒入配置即可，即点开小风车，在配置文件处选择下载，倒入配置文件链接。

也可将配置文件导入手机，直接点击即可。



## 配置文件

配置文件可以编辑，只要编辑配置文件，就是编辑整个软件。

- general 分流策略
- Dns dns
- Policy 策略，分流策略
- server_remote 节点
- filter_remote  远程策略，规则，分流，去广告
- rewrite_remote 远程脚本
- server_local 本地脚本
- Filter_local 本地策略
- rewrite_local 本地脚本
- task_local 定时任务
- mitm 证书和一些host

## 翻墙

导入节点即可

## 脚本

远程和本地导入脚本即可，野可以直接修改相关配置。

 ## 定时任务

能用docker就用docker，不然太费手机。

目前主要是京东相关。

以及天气等。



## boxjs

远程管理，将定时任务的相关配置导入后即可远程出发定时任务。
