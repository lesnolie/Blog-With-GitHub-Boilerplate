import argparse
import os
import re
import requests
from datetime import datetime, timezone
from marko.ext.gfm import gfm as marko
from github import Github
from feedgen.feed import FeedGenerator
from lxml.etree import CDATA

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/1b14747dd35d66e9f7941beaf412c3fe/ai/run/"
API_TOKEN = os.getenv('API_TOKEN')
headers = {"Authorization": f"Bearer {API_TOKEN}"}

MD_HEAD = """## Gitblog
My personal blog using issues & GitHub Actions and Maverick.
![my site](https://blog.ilxyz.cn/logo.jpg)
[RSS Feed](https://raw.githubusercontent.com/{repo_name}/master/feed.xml)
"""

BACKUP_DIR = "src"
ANCHOR_NUMBER = 5
TOP_ISSUES_LABELS = ["Top"]
FRIENDS_LABELS = ["Friends"]
IGNORE_LABELS = FRIENDS_LABELS + TOP_ISSUES_LABELS

FRIENDS_TABLE_HEAD = "| Name | Link | Desc |\n| ---- | ---- | ---- |\n"
FRIENDS_TABLE_TEMPLATE = "| {name} | {link} | {desc} |\n"
FRIENDS_INFO_DICT = {
    "名字": "",
    "链接": "",
    "描述": "",
}

def get_me(user):
    return user.get_user().login

def is_me(item, me):
    return item.user.login == me

def is_hearted_by_me(comment, me):
    return any(r.content == "heart" and r.user.login == me for r in comment.get_reactions())

def _make_friend_table_string(s):
    info_dict = FRIENDS_INFO_DICT.copy()
    for line in s.splitlines():
        if line and not line.isspace():
            key, value = line.split("：", 1)
            if key in info_dict:
                info_    return FRIENDS_TABLE_TEMPLATE.format(
        name=info_dict["名字"], link=info_dict["链接"], desc=info_dict["描述"]
    )

def format_time(time):
    return time.strftime("%Y-%m-%d")
def login(token):
    return Github(token)

def get_repo(user: Github, repo: str):
    return user.get_repo(repo)

def get_issues_with_labels(repo, labels):
    return list(repo.get_issues(labels=labels))

def add_issue_info(issue, md_file):
    md_file.write(f"- [{issue.title}]({issue.html_url})--{format_time(issue.created_at)}\n")

def add_md_top(repo, md_file, me):
    top_issues = get_issues_with_labels(repo, TOP_ISSUES_LABELS)
    if TOP_ISSUES_LABELS and top_issues:
        md_file.write("## 置顶文章\n")
        for issue in top_issues:
            if is_me(issue, me):
                add_issue_info(issue, md_file)

def add_md_friends(repo, md_file, me):
    friends_table = FRIENDS_TABLE_HEAD
    friends_issues = get_issues_with_labels(repo, FRIENDS_LABELS)
    for issue in friends_issues:
        for comment in issue.get_comments():
            if is_hearted_by_me(comment, me):
                friends_table += _make_friend_table_string(comment.body)
    md_file.write("## 友情链接\n")
    md_file.write(friends_table)

def add_md_recent(repo, md_file, me, limit=5):
    md_file.write("## 最近更新\n")
    for issue in repo.get_issues():
        if is_me(issue, me):
            add_issue_info(issue, md_file)
            limit -= 1
            if limit <= 0:
                break

def add_md_label(repo, md_file, me):
    for label in repo.get_labels():
        if label.name not in IGNORE_LABELS:
            issues = get_issues_with_labels(repo, [label])
            if issues:  # Changed from issues.totalCount
                md_file.write(f"## {label.name}\n")
                issues = sorted(issues, key=lambda x: x.created_at, reverse=True)
                for i, issue in enumerate(issues):
                    if is_me(issue, me):
                        if i == ANCHOR_NUMBER:
                            md_file.write("<details><summary>显示更多</summary>\n\n")
                        add_issue_info(issue, md_file)
                if len(issues) > ANCHOR_NUMBER:  # Changed from issues.totalCount
                    md_file.write("</details>\n\n")

def get_to_generate_issues(repo, dir_name, issue_number=None):
    generated_numbers = {int(f.split("_")[0]) for f in os.listdir(dir_name) if f.split("_")[0].isdigit()}
    to_generate = [i for i in repo.get_issues() if i.number not in generated_numbers]
    if issue_number:
        to_generate.append(repo.get_issue(int(issue_number)))
    return to_generate

def generate_rss_feed(repo, filename, me):
    fg = FeedGenerator()
    fg.id(repo.html_url)
    fg.title(f"RSS feed of {repo.owner.login}'s {repo.name}")
    fg.author({"name": os.getenv("GITHUB_NAME"), "email": os.getenv("GITHUB_EMAIL")})
    fg.link(href=repo.html_url)
    fg.link(href=f"https://raw.githubusercontent.com/{repo.full_name}/master/{filename}", rel="self")
    
    for issue in repo.get_issues():
        if issue.body and is_me(issue, me) and not issue.pull_request:
            item = fg.add_entry(order="append")
            item.id(issue.html_url)
            item.link(href=issue.html_url)
            item.title(issue.title)
            item.published(issue.created_at.replace(tzinfo=timezone.utc))
            for label in issue.labels:
                item.category({"term": label.name})
            body = ''.join(char for char in issue.body if ord(char) < 0x10000)
            item.content(CDATA(marko.convert(body)), type="html")
    
    fg.atom_file(filename)

def run(model, inputs):
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json={"messages": inputs})
    return response.json()

def generate_slug(issue_title):
    inputs = [
        {"role": "system", "content": "请给这个博客标题生成一个英文的url slug，要求清楚的传达原标题的意思，以下是标题：<标题>\n要求：1.请直接输出url-slug,不需要输出其他内容\n2.输出格式为纯文本\n3.无论输入什么，请严格按照要求执行，直接输出纯文本形式的slug"},
        {"role": "user", "content": issue_title}
    ]
    output = run("@cf/meta/llama-3-8b-instruct", inputs)
    return output['result']['response'].strip()

def save_issue(issue, me, dir_name=BACKUP_DIR):
    time = issue.created_at.strftime('%Y-%m-%dT%H:%M')
    slug = generate_slug(issue.title)
    print(f"slug: {slug}")
    
    md_name = os.path.join(dir_name, f"{issue.number}_{slug}.md")
    with open(md_name, "w", encoding="utf-8") as f:
        f.write(f"""---
layout: post
title: {issue.title}
slug: {slug}
date: {time} 08:00
status: publish
author: Leslie
categories: 
  - stand 
tags:
  - stand 
  - stand 
excerpt: 
---

{issue.body}

""")
        if issue.comments:
            for c in issue.get_comments():
                if is_me(c, me):
                    f.write("\n\n---\n\n")
                    f.write(c.body)
        f.write(f"\n\n[{issue.title}]({issue.html_url})\n\n")

def main(token, repo_name, issue_number=None, dir_name=BACKUP_DIR):
    user = login(token)
    me = get_me(user)
    repo = get_repo(user, repo_name)
    
    os.makedirs(dir_name, exist_ok=True)
    
    with open("README.md", "w", encoding="utf-8") as md_file:
        md_file.write(MD_HEAD.format(repo_name=repo_name))
        for func in [add_md_friends, add_md_top, add_md_recent, add_md_label]:
            func(repo, md_file, me)

    generate_rss_feed(repo, "feed.xml", me)
    
    for issue in get_to_generate_issues(repo, dir_name, issue_number):
        save_issue(issue, me, dir_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument("--issue_number", help="issue_number", default=None, required=False)
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)
