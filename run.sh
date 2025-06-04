#!/bin/sh

VENV_PATH=~/projects/fractalparserbot/env/bin/activate
SCRIPT1=~/projects/fractalparserbot/tg_bot/main.py  
SCRIPT2=~/projects/fractalparserbot/scrapper/monitoring_urls.py
SCRIPT3=~/projects/fractalparserbot/scrapper/monitoring_views.py
SCRIPT4=~/projects/fractalparserbot/scrapper/recheck_views.py
SCRIPT5=~/projects/fractalparserbot/scrapper/scrape_ads.py
SCRIPT6=~/projects/fractalparserbot/scrapper/db_cleaner.py

while true; do
    source $VENV_PATH
    python3 $SCRIPT1 
    echo "One or more scripts crashed. Restarting all in 5 seconds..."
    sleep 5
done
