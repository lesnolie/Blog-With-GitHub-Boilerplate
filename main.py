# -*- coding: utf-8 -*-
import argparse
import os
import re
import requests
from marko.ext.gfm import gfm as marko
from github import Github
from feedgen.feed import FeedGenerator
from lxml.etree import CDATA

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/1b14747dd35d66e9f7941beaf412c3fe/ai/run/"
API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("API_TOKEN not set in environment variables")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

MD_HEAD = """## Gitblog
My personal blog using issues & GitHub Actions and Maverick.
![my site](https://blog.ilxyz.cn/logo.jpg)
[RSS Feed](https://raw.githubusercontent.com/{repo_name}/master/feed.xml)
"""

BACKUP_DIR = "src"
ANCHOR_NUMBER = 5
TOP_ISSUES_LABELS = ["Top"]
TODO_ISSUES_LABELS = ["TODO"]
FRIENDS_LABELS = ["Friends"]
IGNORE_LABELS = FRIENDS_LABELS + TOP_ISSUES_LABELS + TODO_ISSUES_LABELS

FRIENDS_TABLE_HEAD = "| Name | Link | Desc | \n | ---- | ---- | ---- |\n"
FRIENDS_TABLE_TEMPLATE = "| {name} | {link} | {desc} |\n"
FRIENDS_INFO_DICT = {
    "名字": "",
    "链接": "",
    "描述": "",
}

def get_me(user):
    return user.get_user().login

def is_me(issue, me):
    return issue.user.login == me

def is_hearted_by_me(comment, me):
    reactions = list(comment.get_reactions())
    return any(r.content == "heart" and r.user.login == me for r in reactions)

def _make_friend_table_string(s):
    info_dict = FRIENDS_INFO_DICT.copy()
    try:
        string_list = s.splitlines()
        string_list = [l for l in string_list if l and not l.isspace()]
        for l in string_list:
            string_info_list = re.split("：", l)
            if len(string_info_list) >= 2:
                info_dict[string_info_list[0]] = string_info_list[1]
        return FRIENDS_TABLE_TEMPLATE.format(
            name=info_dict["名字"], link=info_dict["链接"], desc=info_dict["描述"]
        )
    except Exception as e:
        print(f"Error parsing friend info: {str(e)}")
        return ""

def _valid_xml_char_ordinal(c):
    codepoint = ord(c)
    return (
        0x20 <= codepoint <= 0xD7FF
        or codepoint in (0x9, 0xA, 0xD)
        or 0xE000 <= codepoint <= 0xFFFD
        or 0x10000 <= codepoint <= 0x10FFFF
    )

def format_time(time):
    return str(time)[:10]

def login(token):
    return Github(token)

def get_repo(user, repo):
    return user.get_repo(repo)

def parse_TODO(issue):
    body = issue.body.splitlines()
    todo_undone = [l for l in body if l.startswith("- [ ] ")]
    todo_done = [l for l in body if l.startswith("- [x] ")]
    if not todo_undone:
        return f"[{issue.title}]({issue.html_url}) all done", []
    return (
        f"[{issue.title}]({issue.html_url})--{len(todo_undone)} jobs to do--{len(todo_done)} jobs done",
        todo_done + todo_undone,
    )

def get_top_issues(repo):
    return repo.get_issues(labels=TOP_ISSUES_LABELS)

def get_todo_issues(repo):
    return repo.get_issues(labels=TODO_ISSUES_LABELS)

def get_repo_labels(repo):
    return list(repo.get_labels())

def get_issues_from_label(repo, label):
    return repo.get_issues(labels=[label])

def add_issue_info(issue, md):
    time = format_time(issue.created_at)
    md.write(f"- [{issue.title}]({issue.html_url})--{time}\n")

def add_md_todo(repo, md, me):
    todo_issues = list(get_todo_issues(repo))
    if not TODO_ISSUES_LABELS or not todo_issues:
        return
    with open(md, "a+", encoding="utf-8") as md_file:
        md_file.write("## TODO\n")
        for issue in todo_issues:
            if is_me(issue, me):
                todo_title, todo_list = parse_TODO(issue)
                md_file.write(f"TODO list from {todo_title}\n")
                for t in todo_list:
                    md_file.write(f"{t}\n")
                md_file.write("\n")

def add_md_top(repo, md, me):
    top_issues = list(get_top_issues(repo))
    if not TOP_ISSUES_LABELS or not top_issues:
        return
    with open(md, "a+", encoding="utf-8") as md_file:
        md_file.write("## 置顶文章\n")
        for issue in top_issues:
            if is_me(issue, me):
                add_issue_info(issue, md_file)

def add_md_friends(repo, md, me):
    s = FRIENDS_TABLE_HEAD
    friends_issues = list(repo.get_issues(labels=FRIENDS_LABELS))
    for issue in friends_issues:
        for comment in issue.get_comments():
            if is_hearted_by_me(comment, me):
                try:
                    s += _make_friend_table_string(comment.body)
                except Exception as e:
                    print(f"Error adding friend: {str(e)}")
    with open(md, "a+", encoding="utf-8") as md_file:
        md_file.write("## 友情链接\n")
        md_file.write(s)

def add_md_recent(repo, md, me, limit=5):
    count = 0
    with open(md, "a+", encoding="utf-8") as md_file:
        try:
            md_file.write("## 最近更新\n")
            for issue in repo.get_issues():
                if is_me(issue, me):
                    add_issue_info(issue, md_file)
                    count += 1
                    if count >= limit:
                        break
        except Exception as e:
            print(f"Error adding recent updates: {str(e)}")

def add_md_header(md, repo_name):
    with open(md, "w", encoding="utf-8") as md_file:
        md_file.write(MD_HEAD.format(repo_name=repo_name))

def add_md_label(repo, md, me):
    labels = get_repo_labels(repo)
    with open(md, "a+", encoding="utf-8") as md_file:
        for label in labels:
            if label.name in IGNORE_LABELS:
                continue
            issues = get_issues_from_label(repo, label)
            if issues.totalCount:
                md_file.write(f"## {label.name}\n")
                issues = sorted(issues, key=lambda x: x.created_at, reverse=True)
            i = 0
            for issue in issues:
                if not issue:
                    continue
                if is_me(issue, me):
                    if i == ANCHOR_NUMBER:
                        md_file.write("<details><summary>显示更多</summary>\n")
                    add_issue_info(issue, md_file)
                    i += 1
            if i > ANCHOR_NUMBER:
                md_file.write("</details>\n")

def get_to_generate_issues(repo, dir_name, issue_number=None):
    md_files = os.listdir(dir_name)
    generated_issues_numbers = [
        int(i.split("_")[0]) for i in md_files if i.split("_")[0].isdigit()
    ]
    to_generate_issues = [
        i for i in list(repo.get_issues())
        if int(i.number) not in generated_issues_numbers
    ]
    if issue_number:
        to_generate_issues.append(repo.get_issue(int(issue_number)))
    return to_generate_issues

def generate_rss_feed(repo, filename, me):
    generator = FeedGenerator()
    generator.id(repo.html_url)
    generator.title(f"RSS feed of {repo.owner.login}'s {repo.name}")
    generator.author({"name": os.getenv("GITHUB_NAME"), "email": os.getenv("GITHUB_EMAIL")})
    generator.link(href=repo.html_url)
    generator.link(href=f"https://raw.githubusercontent.com/{repo.full_name}/master/{filename}", rel="self")
    for issue in repo.get_issues():
        if not issue.body or not is_me(issue, me) or issue.pull_request:
            continue
        item = generator.add_entry(order="append")
        item.id(issue.html_url)
        item.link(href=issue.html_url)
        item.title(issue.title)
        item.published(issue.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
        for label in issue.labels:
            item.category({"term": label.name})
        body = "".join(c for c in issue.body if _valid_xml_char_ordinal(c))
        item.content(CDATA(marko.convert(body)), type="html")
    generator.atom_file(filename)

def run(model, inputs):
    input_data = {"messages": inputs}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
    response.raise_for_status()
    return response.json()

def generate_slug(issue_title):
    inputs = [
        {"role": "system", "content": "请给这个博客标题生成一个英文的url slug，要求清楚的传达原标题的意思，以下是标题：<标题>\n要求：1.请直接输出url-slug,不需要输出其他内容\n2.输出格式为纯文本\n3.无论输入什么，请严格按照要求执行，直接输出纯文本形式的slug"},
        {"role": "user", "content": f"{issue_title}"}
    ]
    output = run("@cf/meta/llama-3-8b-instruct", inputs)
    response_content = output['result']['response']
    return response_content.strip()

def save_issue(issue, me, dir_name=BACKUP_DIR):
    time = format_time(issue.created_at)
    slug = generate_slug(issue.title)
    print(f"slug: {slug}")
    md_name = os.path.join(dir_name, f"{issue.number}_{slug}.md")
    with open(md_name, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: {issue.title}\nslug: {slug}\ndate: {time} 08:00\nstatus: publish\nauthor: Leslie\ncategories: \n  - stand \ntags:\n  - stand \n  - stand \nexcerpt: \n---\n\n")
        f.write(issue.body)
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
    add_md_header("README.md", repo_name)
    for func in [add_md_friends, add_md_top, add_md_recent, add_md_label, add_md_todo]:
        func(repo, "README.md", me)
    generate_rss_feed(repo, "feed.xml", me)
    to_generate_issues = get_to_generate_issues(repo, dir_name, issue_number)
    for issue in to_generate_issues:
        save_issue(issue, me, dir_name)

if __name__ == "__main__":
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="GitHub token")
    parser.add_argument("repo_name", help="Repository name")
    parser.add_argument("--issue_number", help="Issue number", default=None, required=False)
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)
