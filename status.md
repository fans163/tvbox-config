# 源检测状态

最近更新：2026-11-14 05:38 UTC

| 仓 | 状态 | 保留 | 删除 | 已测快源 | 解析器源（未测） |
|---|---|---|---|---|---|
| `qist-jsm` | ✅ 家庭电视版（无直播） | 160 | 2 | 33 | 113 |
| `qist-dianshi` | ✅ 电视自用 | 161 | 2 | 34 | 113 |
| `qist-0825` | ✅ 小而精 | 132 | 2 | 24 | 105 |
| `qist-9918` | ✅ 极简 | 59 | 0 | 15 | 23 |

## 测速口径

- 只对「直连 HTTP API」类型的源做真实测速（接口响应 ≤ 10 秒）
- 域名解析失败的源直接删除；接口超时的删除；连不上但域名正常的降到队尾
- 走 jar / js / python 解析器的源无法在服务端模拟播放链路，标注「未测」，按原顺序保留
- 播放中卡顿只能在电视上实测：遇到卡的就往 `blocklist.txt` 加一行源名，第二天自动剔除

## 电视上填这个地址

```
https://gh-proxy.com/https://raw.githubusercontent.com/hesanyue50-lang/tvbox-config/main/tvbox.json
```

主代理不通时把开头的 `gh-proxy.com` 换成 `ghproxy.net`。
`gh-proxy` 是 GitHub 国内加速镜像，不是 VPN，国内直连即可。
