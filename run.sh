#!/bin/bash

set -e

shell_dir=$(dirname $(readlink -f "$0"))

RESULT=$(python3 $shell_dir/checkin.py)

echo "$RESULT"

if [[ -z $TELEGRAM_TOKEN || -z $TELEGRAM_TO ]]; then
    echo "no tgid or bot token"
    exit
fi

# for telegram message

curl "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage?chat_id=${TELEGRAM_TO}&parse_mode=HTML&disable_notification=true&text=${RESULT}"