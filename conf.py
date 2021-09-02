# -*- coding: utf-8 -*-
"""博客构建配置文件
"""

# For Maverick
site_prefix = "Marverick/"
source_dir = "../src/"
build_dir = "../dist/"
index_page_size = 10
archives_page_size = 30
template ={
    "name": "Galileo",
    "type": "local",
    "path": "../MyTheme/Galileo/" # could also use relatetive path to Maverick
}
enable_jsdelivr = {
    "enabled": False,
    "repo": "lesnolie/Marverick@gh-pages"
}

# 站点设置
site_name = "LESLIE's WIKI"
site_logo = "${static_prefix}logo.png"
site_build_date = "2021-03-29T16:51+08:00"
author = "LESLIE"
email = "lesliezhang08@gmail.com"
author_homepage = "https://blog.lesliemm.xyz"
description = "我喜欢猫，和你"
key_words = ['Maverick', 'LESLIE', 'YOUNG FATHER', 'blog']
language = 'zh-CN'
external_links = [
    {
        "name": "",
        "url": "",
        "brief": ""
    },
    {
        "name": "",
        "url": "",
        "brief": ""
    }
]
nav = [
    {
        "name": "",
        "url": "${site_prefix}",
        "target": "_self"
    },
    {
        "name": "",
        "url": "${site_prefix}archives/",
        "target": "_self"
    },
   ]
social_links = [
    {
        "name": "",
        "url": "",
        "icon": ""
    },
    {
        "name": "",
        "url": "",
        "icon": ""
    }
]

head_addon = r'''
<meta http-equiv="x-dns-prefetch-control" content="on">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net" />
'''

footer_addon = ''

body_addon = ''
