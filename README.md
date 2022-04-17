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

## Contributions

- [checkin.py](checkin.py) is written by [Maxwell Lyu](https://github.com/Maxwell-Lyu).

* Modified by [Antares](https://github.com/Antares0982).

* Also modified by [Limos](https://github.com/cubiccm).
