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


### Overview

The website being scraped is [beverly.patriotproperties.com](https://beverly.patriotproperties.com). We are using [selenium](https://selenium-python.readthedocs.io/getting-started.html) as our webdriver along with chrome. We are also using [overpy](https://pypi.org/project/overpy/) which is a python wrapper of the "Open Street Maps" API called "Overpass" to grab all the streets in beverly so we search for them on patriot properties website. This has got most of the streets but not all of them. The plan is to implement a backend service using [python django](https://docs.djangoproject.com/en/5.1/) so save the scrapped data to and build an API on top of.


### Django

#### Run server

```bash
cd realestateApi

python manage.py runserver
```

### Create db user account

```bash
python manage.py createsuperuser
```

- Navigate to http://127.0.0.1:8000/admin/
- Login with the creds you just crated

### Run webscraper
```bash
python manage.py scrape_and_save_data
```
- For now only reads array from sample data in `webscraper/streets_data/street_sample.json`

#### making db changes

```bash
python manage.py makemigrations realestate
python manage.py migrate
```

