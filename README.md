# Realestate Bot

![realestate bot logo](./realestate-bot-logo.png "Logo")

### Install requirements

```bash
# create venv 
virtualenv venv

# activate venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt
```

### Run webscraper
```bash
cd webscraper

python scraper.py
```

### Overview

The website being scraped is [beverly.patriotproperties.com](https://beverly.patriotproperties.com). We are using [selenium](https://selenium-python.readthedocs.io/getting-started.html) as our webdriver along with chrome. We are also using [overpy](https://pypi.org/project/overpy/) which is a python wrapper of the "Open Street Maps" API called "Overpass" to grab all the streets in beverly so we search for them on patriot properties website. This has got most of the streets but not all of them. The plan is to implement a backend service using [python django](https://docs.djangoproject.com/en/5.1/) so save the scrapped data to and build an API on top of.