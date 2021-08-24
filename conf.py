# -*- coding: utf-8 -*-
"""博客构建配置文件
"""

# For Maverick
site_prefix = "/"
source_dir = "../src/"
build_dir = "../dist/"
index_page_size = 10
archives_page_size = 30
template = {
    "name": "Galileo",
    "type": "local",
    "path": "/MyTheme/" # could also use relatetive path to Maverick
}

enable_jsdelivr = {
    "enabled": True,
    "repo": "lesnolie/Marverick@gh-pages"
}

# 站点设置
site_name = "LESLIE's WIKI"
site_logo = "${static_prefix}logo.png"
site_build_date = "2021-03-29T16:51+08:00"
author = "LESLIE"
email = "lesliezhang08@gmail.com"
author_homepage = "https://blog.leslie.cn"
description = "我喜欢猫，和你"
key_words = ['Maverick', 'LESLIE', 'YOUNG FATHER', 'blog']
language = 'zh-CN'
external_links = [
    {
        "name": "BLOG",
        "url": "https://lesnolie.github.io",
        "brief": "🏄‍ Go My Own Way."
    },
    {
        "name": "dirve",
        "url": "https://drive.lesliemm.xyz",
        "brief": "LIFE Storage"
    }
]
nav = [
    {
        "name": "Home",
        "url": "${site_prefix}",
        "target": "_self"
    },
    {
        "name": "Archives",
        "url": "${site_prefix}archives/",
        "target": "_self"
    },
   ]
social_links = [
    {
        "name": "GitHub",
        "url": "https://github.com/lesnolie",
        "icon": "gi gi-github"
    },
    {
        "name": "Weibo",
        "url": "https://weibo.com/2185506670/",
        "icon": "gi gi-weibo"
    }
]

head_addon = r'''
<meta http-equiv="x-dns-prefetch-control" content="on">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net" />
'''

footer_addon = ''

body_addon = ''
