# tvbox-config

TVBox / OK影视 的配置聚合，每周自动检测上游源，输出一个多仓地址。

## 来源

本仓库 fork 自 [hesanyue50-lang/tvbox-config](https://github.com/hesanyue50-lang/tvbox-config)，
在其基础上改为自动识别当前仓库、只保留可用的定时更新流程。

片源配置均来自公开分享的上游作者（见下方「上游」），本仓库只做可用性检测与聚合，不托管任何片源。

## 电视上填这个

```
https://gh-proxy.com/https://raw.githubusercontent.com/fans163/tvbox-config/main/tvbox.json
```

不通就把开头的 `gh-proxy.com` 换成 `ghproxy.net`。

## 它做什么

每周一北京时间 04:00 跑一次：

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

## 私有仓 + 公开输出仓

本仓库只负责检测和聚合，公开仓 `fans163/6` 里只放一个文件 `tvbox.json`（单仓配置，自包含），电视端只需填这一个链接：

```
https://gh-proxy.com/https://raw.githubusercontent.com/fans163/6/main/tvbox.json
```

如需更换发布目标，在 **Settings → Secrets and variables → Actions** 里设置：

- Variables：`PUBLISH_REPO`（可选，默认 `fans163/6`）
- Secrets：`PUBLISH_TOKEN`（必填，一个对目标公开仓有 **Contents: Read and write** 权限的 fine-grained PAT）

配置完成后本仓库可以设为私有，定时任务仍会正常把结果推送到公开仓。

## 本地手动跑

```bash
python3 update.py
```

无第三方依赖，只用标准库。

## 免责声明

- 本仓库仅供本人个人学习、技术研究与自用，不对外提供任何服务，也不构成任何推荐、引导或分发。
- 请勿将本仓库及其生成内容用于出售、倒卖、付费引流、商业推广等任何营利或变相营利行为。
- 请勿将本仓库用于任何违反所在地法律法规的用途；因使用、传播或依赖本仓库内容产生的一切后果，由使用者自行承担。
- 配置文件内容均来自公开分享的上游作者，本仓库只做可用性检测与聚合，不托管、不存储、不制作任何片源。
- 若相关权利人认为内容侵犯其合法权益，请联系删除，本仓库将及时处理。
