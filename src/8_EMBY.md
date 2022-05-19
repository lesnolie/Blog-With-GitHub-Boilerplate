---
layout: post
title: EMBY
slug: EMBY
date: 2022-05-19 08:00
status: publish
author: Leslie
categories: 
  - stand 
tags:
  - stand 
  - stand 
excerpt: 
---

最近做了几件事，第一件事是搭建了一个EMBY，并用了两个服务器进行反代二次加速。目前来看观看不卡。我的腾讯机也不会放着不用了。  
第二件事就是想弄一个全自动化的追剧，目前发现的工具有“NAS-TOOLS”、“MOVIE-ROBOT”、以及一个”懒人追剧体验，全自动顶级追剧“。  
没错，依照我的性格，我不能允许这种东西我不会，那就放手一搏吧。  

东西很简单，用到的软件有：  
jackket 用来搜索  
Snoarr用来管理电视剧  
Radarr用来管理电影  
Qbittorrent & NZB 用来下载电影。  
整体都用DOCKER运行，NASTOOLS和MOVIE-ROBOT是两个DOCKER将几个DOCKER 串联起来。总之就是让几个DOCKER 通过硬链接实现搜索点击想看的剧，自动下载并整理命名，就可以在EMBY上观看了。  

那，毫无意外，整体过程又是及其耗费时间的，遇到的问题有：nginx、VPS的性能不行，WSL无法systemctl，service不会用，WSL2无法使用代理。  
等等等等等等等等。  

最终我明白一个道理，我目前还是先赚钱，等有了NAS系统（或者PS5）以后，再来搞这个吧。  

[EMBY](https://github.com/lesnolie/Marverick/issues/8)

