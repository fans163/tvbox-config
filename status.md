# 源检测状态

最近更新：2026-11-14 06:08 UTC

| 仓 | 状态 | 保留 | 删除 | 已测快源 | 解析器源（未测） |
|---|---|---|---|---|---|
| `qist-jsm` | ✅ 家庭电视版（无直播·推荐） | 159 | 3 | 32 | 105 |
| `lightconer` | ✅ 聚合大仓（片源最多） | 480 | 37 | 15 | 368 |
| `qist-js` | ✅ 大合集 | 294 | 2 | 223 | 63 |
| `niubihu1` | ✅ 牛虎 | 173 | 1 | 11 | 131 |
| `hd9211` | ✅ 采集站合集 | 116 | 28 | 28 | 0 |
| `qist-dianshi` | ✅ 电视自用 | 160 | 3 | 33 | 105 |
| `qist-0825` | ✅ 小而精 | 130 | 4 | 24 | 97 |
| `qist-9918` | ✅ 极简 | 55 | 4 | 15 | 22 |

## 筛选口径

- **域名连通性**：每个源提取主域名，解析失败或 80/443 都连不上的直接删除（共测 262 个域名）
- **接口测速**：直连 HTTP API 的源实测响应时间，超过 10 秒删除（共测 264 个接口）
- **排序**：实测快的排最前；jar/js/py 解析器源无法在服务端模拟播放链路，居中标注「未测」
- **国外源**：YouTube、googlevideo、github.io、netlify、vercel、telegram 等命中即删
- 播放中卡顿只能在电视上实测：遇到就往 `blocklist.txt` 加一行源名，第二天自动剔除

## 电视上填这个地址

```
https://gh-proxy.com/https://raw.githubusercontent.com/hesanyue50-lang/tvbox-config/main/tvbox.json
```

主代理不通时把开头的 `gh-proxy.com` 换成 `ghproxy.net`。
`gh-proxy` 是 GitHub 国内加速镜像，不是 VPN，国内直连即可。
