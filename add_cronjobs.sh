#!/bin/bash
echo "Adding tigerone cron jobs..."
crontab -l -u user | cat - cronjobs | crontab -u user -
