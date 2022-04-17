# NJU Health Checkin

> NJU daily health checkin, with fake locations and tgbot info, forked from [forewing/nju-health-checkin](https://github.com/forewing/nju-health-checkin).

## Requirements

```
python3 -m pip install -r requirements.txt
```

## Github Actions

1. Set `NJU_USER` and `NJU_PASS` in settings/secrets.

2. (Optional) Set `TELEGRAM_TOKEN` and `TELEGRAM_TO` secrets. [(appleboy/telegram-action)](https://github.com/appleboy/telegram-action#secrets)

- The job will be automatically executed at 9:00 am UTC+8 (may be delayed up to 1 hour due to GitHub's issues with cron actions).

## Run with Crontab

This script provides features of sending checkin info using telegram-bot, and manually specifying fake location. You can feel free to use all of these two features or neither of them.

`crontab -e` and write:

```crontab
0 21 * * * /usr/bin/env http_proxy=url:port https_proxy=url:port bottoken=xxx tgid=yyy bash run.sh # run at 9pm everyday
```

Note:

* Complete your own `config.ini` file. If **always use the location in the last checkin**, just left `location` blank. If checkin requests do not use proxy, left `proxy` blank in config. Otherwise specify the proxy url and port exlicitly in config.ini (checkin.py ignores proxy setting in env!)
* If you **do not use telegram bot**, just write `/usr/bin/env bash run.sh` in crontab.

## Contributions

- [checkin.py](checkin.py) is written by [Maxwell Lyu](https://github.com/Maxwell-Lyu).

* Modified by [Antares](https://github.com/Antares0982).

