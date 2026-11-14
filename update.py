#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TVBox / OK影视 配置聚合器

每天：
  1. 逐个检测上游配置是否活着（JSON 可解析 + sites 数量达标）
  2. 把活着的上游聚合成一个「多仓」配置 tvbox.json
  3. 生成 status.md 记录检测结果

为什么用多仓：单个上游挂掉时，电视上换一个仓即可，不用改地址。
为什么 url 加 gh-proxy：电视在国内，raw.githubusercontent.com 直连不通。
"""

import json
import sys
import ssl
import urllib.request
import datetime

PROXY = "https://gh-proxy.com/"          # 主代理（国内可访问）
PROXY_ALT = "https://ghproxy.net/"       # 备用，仅写进说明，不在文件里用
TIMEOUT = 25

# (slug, raw url, 显示名)
SOURCES = [
    ("qist-jsm", "https://raw.githubusercontent.com/qist/tvbox/master/jsm.json",
     "qist 家庭电视版（无直播·推荐）"),
    ("qist-dianshi", "https://raw.githubusercontent.com/qist/tvbox/master/dianshi.json",
     "qist 电视自用"),
    ("qist-0825", "https://raw.githubusercontent.com/qist/tvbox/master/0825.json",
     "qist 小而精"),
    ("qist-js", "https://raw.githubusercontent.com/qist/tvbox/master/js.json",
     "qist 大合集（源最多·含YouTube）"),
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"


def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
        return r.read()


def probe(raw_url):
    """先直连（GitHub Actions 在国外），失败再走代理。返回 (ok, sites, note)"""
    last = ""
    for u in (raw_url, PROXY + raw_url):
        try:
            data = fetch(u)
            d = json.loads(data.decode("utf-8", "ignore"))
            n = len(d.get("sites") or [])
            if n >= 3:
                return True, n, "ok"
            last = "sites=%d 太少" % n
        except Exception as e:  # noqa: BLE001
            last = "%s: %s" % (type(e).__name__, str(e)[:60])
    return False, 0, last


def main():
    got, rows = [], []
    for slug, url, name in SOURCES:
        ok, n, note = probe(url)
        rows.append((slug, name, ok, n, note))
        print("%-10s %-28s %s sites=%d %s" % (slug, name, "OK " if ok else "DEAD", n, note))
        if ok:
            got.append({"name": name, "url": PROXY + url})

    if not got:
        print("!! 所有上游都不可用，保留旧文件不动", file=sys.stderr)
        return 1

    cfg = {"urls": got}
    with open("tvbox.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")

    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# 源检测状态",
        "",
        "最近更新：%s" % today,
        "",
        "| 仓 | 名称 | 状态 | 源数量 | 备注 |",
        "|---|---|---|---|---|",
    ]
    for slug, name, ok, n, note in rows:
        lines.append("| `%s` | %s | %s | %d | %s |" % (
            slug, name, "✅ 可用" if ok else "❌ 失效", n, note))
    lines += [
        "",
        "## 电视上填这个地址",
        "",
        "```",
        PROXY + "https://raw.githubusercontent.com/hesanyue50-lang/tvbox-config/main/tvbox.json",
        "```",
        "",
        "主代理不通时把开头的 `gh-proxy.com` 换成 `ghproxy.net`。",
        "",
    ]
    with open("status.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("生成 %d 个仓" % len(got))
    return 0


if __name__ == "__main__":
    sys.exit(main())
