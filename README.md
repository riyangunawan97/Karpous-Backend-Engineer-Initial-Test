# Investment Tracker API

## Overview
A lightweight Django REST API for tracking user investments.

## Setup

```bash
git clone <repo-url>
cd investment-tracker
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/sample_data.json
python manage.py runserver
