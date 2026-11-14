#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TVBox / OK影视 配置聚合器（国内净化版）

每天：
  1. 拉取上游配置，校验 JSON 与片源数量
  2. 剔除需要翻墙的站点（YouTube / googlevideo / github.io / netlify / vercel 等）
  3. 把 spider 的相对路径（./jar/xxx.jar）改写为绝对地址，保证镜像后还能用
  4. 净化后的配置存到 sources/<slug>.json，多仓地址指向本仓库
  5. 写 status.md

设计要点：
  - 上游配置里 spider 是 "./jar/spider.jar;md5;..."，直接镜像会让 jar 路径断掉，
    所以必须把相对路径改成「代理 + 上游目录 + 文件名」的绝对地址。
  - 国外站点在国内直连不通，用户也不上 VPN，过滤掉可减少点了没反应的死链。
"""

import json
import os
import re
import ssl
import sys
import urllib.request
import datetime

PROXY = "https://gh-proxy.com/"
PROXY_ALT = "https://ghproxy.net/"
TIMEOUT = 25
OUT_DIR = "sources"

# (slug, raw url, 显示名)
SOURCES = [
    ("qist-jsm", "https://raw.githubusercontent.com/qist/tvbox/master/jsm.json",
     "家庭电视版（无直播）"),
    ("qist-dianshi", "https://raw.githubusercontent.com/qist/tvbox/master/dianshi.json",
     "电视自用"),
    ("qist-0825", "https://raw.githubusercontent.com/qist/tvbox/master/0825.json",
     "小而精"),
    ("qist-9918", "https://raw.githubusercontent.com/qist/tvbox/master/9918.json",
     "极简"),
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# 需要翻墙的域名特征
BAD = re.compile(
    r"youtube|youtu\.be|googlevideo|ytimg|ggpht|gstatic|"
    r"github\.io|netlify\.app|vercel\.app|herokuapp|glitch\.me|"
    r"telegram|t\.me|discord|twitter|x\.com",
    re.I,
)


def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
        return r.read()


def load(raw_url):
    """先直连，失败走代理"""
    last = ""
    for u in (raw_url, PROXY + raw_url):
        try:
            return json.loads(fetch(u).decode("utf-8", "ignore"))
        except Exception as e:  # noqa: BLE001
            last = "%s: %s" % (type(e).__name__, str(e)[:50])
    raise RuntimeError(last)


def fix_rel(obj, base):
    """把配置里所有 "./xxx" 相对路径改写成上游绝对地址（走代理）。

    上游大量用 "./json/xxx.json"、"./js/xxx.js"、"./jar/spider.jar;md5;..."
    这种相对引用；一旦把配置镜像到本仓库，这些文件就不存在了，
    必须指回上游原地址，否则对应站点全部失效。
    """
    if isinstance(obj, dict):
        return {k: fix_rel(v, base) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fix_rel(v, base) for v in obj]
    if isinstance(obj, str) and obj.startswith("./"):
        return PROXY + base + obj[2:]
    return obj


def clean(d, raw_url):
    """过滤国外站点 + 修所有相对路径。返回 (新字典, 剔除了多少)"""
    base = raw_url.rsplit("/", 1)[0] + "/"

    removed = 0
    for key in ("sites", "lives", "parses"):
        items = d.get(key)
        if not isinstance(items, list):
            continue
        keep = []
        for it in items:
            if BAD.search(json.dumps(it, ensure_ascii=False)):
                removed += 1
            else:
                keep.append(it)
        d[key] = keep

    d = fix_rel(d, base)
    return d, removed


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows, urls = [], []

    for slug, raw_url, name in SOURCES:
        try:
            d = load(raw_url)
        except Exception as e:  # noqa: BLE001
            rows.append((slug, name, False, 0, 0, str(e)[:50]))
            print("%-14s DEAD %s" % (slug, e))
            continue

        n_before = len(d.get("sites") or [])
        if n_before < 3:
            rows.append((slug, name, False, n_before, 0, "片源太少"))
            print("%-14s DEAD sites=%d" % (slug, n_before))
            continue

        d, removed = clean(d, raw_url)
        n = len(d.get("sites") or [])
        path = os.path.join(OUT_DIR, slug + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
        rows.append((slug, name, True, n, removed, "ok"))
        urls.append({
            "name": name,
            "url": PROXY + "https://raw.githubusercontent.com/hesanyue50-lang/tvbox-config/main/" + path,
        })
        print("%-14s OK sites=%d 剔除国外=%d" % (slug, n, removed))

    if not urls:
        print("!! 全部上游不可用，保留旧文件", file=sys.stderr)
        return 1

    with open("tvbox.json", "w", encoding="utf-8") as f:
        json.dump({"urls": urls}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# 源检测状态",
        "",
        "最近更新：%s" % now,
        "",
        "| 仓 | 名称 | 状态 | 国内可用源 | 剔除的国外源 |",
        "|---|---|---|---|---|",
    ]
    for slug, name, ok, n, removed, note in rows:
        lines.append("| `%s` | %s | %s | %d | %d |" % (
            slug, name, "✅" if ok else "❌ " + note, n, removed))
    lines += [
        "",
        "> 已自动剔除 YouTube、github.io、netlify、telegram 等国内直连不通的站点，"
        "不需要任何 VPN 或代理工具。",
        "",
        "## 电视上填这个地址",
        "",
        "```",
        PROXY + "https://raw.githubusercontent.com/hesanyue50-lang/tvbox-config/main/tvbox.json",
        "```",
        "",
        "主代理不通时把开头的 `gh-proxy.com` 换成 `ghproxy.net`。",
        "",
        "说明：`gh-proxy` 是 GitHub 的国内加速镜像，不是 VPN，国内直连即可。",
        "",
    ]
    with open("status.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("生成 %d 个仓" % len(urls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
