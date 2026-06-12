## Setup with with pip

##### Create Virtual Environment on Mac
```
python3 -m venv .venv
source .venv/bin/activate
```

##### Create Virtual Environment on Windows
```
python3 -m venv .venv
.\venv\Scripts\Activate.ps1
```

##### Install dependencies
```
pip install -r requirements.txt
pip install --upgrade pip
```

##### Migrate to database
```
python manage.py migrate
python manage.py createsuperuser
```

##### Run application
```
python manage.py runserver
```
http://localhost:8000
