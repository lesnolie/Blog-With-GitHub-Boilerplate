---
layout: post
title: 我的媒体播放库 libdrive
slug: my-media-library-libdrive
date: 2021-06-24 09:00
status: publish
author: LESLIE
categories: 
   - wiki
tags:
   - libdrive
   - movie
   - tv-shows
excerpt:
---



![](./images/libdrive-1.png)

Look at this beautiful website!

It's my [media library](http://35.221.246.119:8000)!

## 什么是Libdrive

***一个可以从[TMDb](https://www.themoviedb.org)自动识别电影、电视剧、漫画，并且产生海报、简单介绍的谷歌硬盘文件可视管理器***

You can build the catalog like the Movies or TV-Shows & Animes, Whatever you like.

I get this amazing tool from [libdrive](https://github.com/libDrive/libDrive).Thanks for the author **Elias Benbourenane**.

## 我是如何创建自己的Libdrive的

就像每一段代码旅程一样，我在创建自己的Libdrive时也遇到了不少麻烦。

 You can find [setup](https://github.com/libDrive/libDrive/wiki/Setup) here by author.

And you can follow me too.

<br/>

**Prerequisites**

---

- A  [Google Developers Console](https://console.developers.google.com/) API lient credentials:  

  > search `console.clould.google` in google then open it.
  >
  > Click `Api & Severice`, then `click credentials`.
  >
  > Then click the `Enable the Drive API` button
  >
  > Name the project anything you want, then click `Next`
  >
  > Wait for the page titled `Configure your OAuth client` to show
  >
  > From the dropdown menu, select `Web Server`
  >
  > Then under the `Authorized redirect URIs` field, put the following URL: `https://config.libdrive.tk`
  >
  > Keep note of the `client_id` and `client_secret`

- A [TMDB API](https://www.themoviedb.org/settings/api) key

- [Python 3](https://www.python.org/)

- OPTIONAL: Cloudflare worker.

- A server.

**Setup**

---

- build locally:

  > 1. Clone the libDrive server repository with `git clone https://github.com/libDrive/server.git`
  >
  > 2. Clone the libDrive web repository with `git clone https://github.com/libDrive/web.git`
  >
  > 3. Open a terminal in the cloned `web` folder
  >
  > 4. Run the following:
  >
  > - `yarn install`
  > - `yarn run build`
  >
  > 5. Copy the generated `/build` folder into the root of the cloned `server` folder
  > 6. Done!

- go to [https://config.libdrive.tk](https://config.libdrive.tk/) and go through the sections, filling in the empty fields

- Save the config into a file named `config.json` in the directory of the libDrive server

- run `python3 -m pip install -r requirements.txt` in the server's directory

- Now your server is ready, to start it run `python3 main.py` from the directory of the libDrive server

the server is now up and run, but it's running only on your machine, the address is `127.0.0.1:8000`.if you wanna share your server publicly, follow this setups:

- run the flowing in terminal `nohup gunicorn -w 4 -b 0.0.0.0:8000 main:app`

**Structure**

---

Movies

>ROOT_DIRECTORY
>
>- MOVIE_1.mp4
>
>- MOVIE_2.mp4
>- MOVIE_3.mp4
>- MOVIE_4.mp4

or

>- ROOT_DIRECTORY
>- MOVIE_1.mp4
>- SUB_FOLDER_1
>  - MOVIE_2.mp4
>- SUB_FOLDER_2
>  - SUB_SUB_FOLDER_1
>    - MOVIE_3.mp4
>    - MOVIE_4.mp4



TV-Shows

>- ROOT_DIRECTORY
>- SHOW_1
>  - SEASON_1
>    - EPISODE_1.mp4
>    - EPISODE_2.mp4
>    - EPISODE_3.mp4
>  - SEASON_2
>    - EPISODE_1.mp4
>    - EPISODE_2.mp4
>    - EPISODE_3.mp4
>- SHOW_2
>  - SEASON_1
>    - EPISODE_1.mp4
>    - EPISODE_2.mp4
>    - EPISODE_3.mp4
>  - SEASON_2
>    - EPISODE_1.mp4
>    - EPISODE_2.mp4
>    - EPISODE_3.mp4

**Some tips**

---

- If there nothing show on your website, pls check the googledrive api allowed.
- there must a `SEASON` folder in TV-shows.

<br/>

Down! Have fun!





