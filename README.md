# tvbox-config

TVBox / OK影视 的配置聚合，每天自动检测上游源，输出一个多仓地址。

## 电视上填这个

```
https://gh-proxy.com/https://raw.githubusercontent.com/fans163/tvbox-config/main/tvbox.json
```

不通就把开头的 `gh-proxy.com` 换成 `ghproxy.net`。

## 它做什么

每天北京时间 04:00 跑一次：

1. 逐个拉取上游配置，JSON 能解析、片源数 ≥ 3 才算活着
2. 活着的上游聚合成多仓配置 `tvbox.json`
3. 检测结果写进 [status.md](status.md)

上游挂掉一个，电视上换一个仓就行，配置地址不用改。

## 上游

| 仓 | 来源 |
|---|---|
| qist 家庭电视版 | [qist/tvbox](https://github.com/qist/tvbox) `jsm.json`，无直播 |
| qist 大而全 | 同上 `0821.json` |
| qist 小而精 | 同上 `0826.json` |
| 香雅情源 | 同上 `XYQ.json` |

## 本地手动跑

```bash
python3 update.py
```

无第三方依赖，只用标准库。

## 说明

配置文件内容来自公开分享的上游作者，本仓库只做可用性检测与聚合，不托管任何片源。
仅供技术研究，请遵守所在地法律法规。
