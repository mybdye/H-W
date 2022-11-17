## [![H](https://github.com/mybdye/H-W-SeleniumBase/actions/workflows/H.yml/badge.svg)](https://github.com/mybdye/H-W-SeleniumBase/actions/workflows/H.yml) [![W](https://github.com/mybdye/H-W-SeleniumBase/actions/workflows/W.yml/badge.svg)](https://github.com/mybdye/H-W-SeleniumBase/actions/workflows/W.yml)
Project for SeleniumBase study.

#### ⏱️ TODO
- None

#### ✏️ NOTE
- 11.17
  - 修复 sb.open() 概率卡死
  - 修复 bark push url编码问题
- 11.16
  - renew 尝试次数 10 改到 15，全程 2~6 分钟
  - yml 配置超时 10 分钟自动取消 action
- 11.04
  - ~~helium/selenium/Playwright~~ >> SeleniumBase
  - ~~MacOS/Windows~~ >> Ubuntu

#### 🌟️ SUGGESTION
```diff
!自定义schedule
.github/workflows/H.yml
.github/workflows/W.yml

例如：
schedule:
    # UTC (国内 UTC+8)
    - cron: '03 02 */2 * *'   
    # 每2天 10:03am 执行
    
!规则参考
  * * * * *
  | | | | |
  | | | | +----- day of week (0 - 7) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
  | | | +------- month (1 - 12) OR jan,feb,mar,apr ...
  | | +--------- day of month (1 - 31)
  | +----------- hour (0 - 23)
  +------------- minute (0 - 59)
```

#### ㊙️ SECRET
  |YOU SECRET NAME|YOU SECRET VALUE|
  |-----|--|
  |`URL_BASE_H` or `URL_BASE_W`|网址，至少写一个，不要带有`https://` 和 `/` |
  |`USERNAME`|你的用户名|
  |`PASSWORD`|你的密码|
  |`BARK_TOKEN`|(可选) api.day.app/`BARK_TOKEN`/ 详见 https://github.com/Finb/Bark|
  |`TG_BOT_TOKEN`|(可选) `xxxxxx:xxxxxxxxxxxxx`|
  |`TG_USER_ID`|(可选) 给 bot `@userinfobot` 发送 `/start`|

#### 📚 THANKS
- [SeleniumBase](https://github.com/seleniumbase)
- [Python](https://www.python.org/)
- [PyCharm CE](https://www.jetbrains.com/pycharm/)
