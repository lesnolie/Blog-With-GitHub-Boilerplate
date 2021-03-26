# -*- coding: utf-8 -*-
"""博客构建配置文件
"""

# For Maverick
site_prefix = "/Blog-With-GitHub-Boilerplate/"
source_dir = "../src/"
build_dir = "../dist/"
index_page_size = 10
archives_page_size = 20
template = {
    "name": "Galileo",
    "type": "local",
    "path": "../Galileo"
}
enable_jsdelivr = {
    "enabled": False,
    "repo": ""
}

# 站点设置
site_name = "我喜欢猫，和你"
site_logo = "${static_prefix}logo.png"
site_build_date = "2019-12-18T16:51+08:00"
author = "LESLIE"
email = "lesliezhang08@gmail.com"
author_homepage = "https://blog.leslie.cn"
description = "但故事的最后你好像还是说了拜"
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
