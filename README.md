# Pinatos Manager
Software development project, solution for a textile company aimed to help them coordinate and optimize their activities. Mainly developed in Python with Django.

## Requirements

Before running the program, you must install the following libraries:

- Django
- pytz

You can install the required libraries using pip. It is recommended to use a virtual environment.

### 1. Create and activate a virtual environment (optional but recommended)

On Windows:
```
python -m venv venv
venv\Scripts\activate
```

### 2. Install the required libraries

```
pip install django pytz
```

Or, from `requirements.txt` file:
```
pip install -r requirements.txt
```

## Running the Program

1. Apply migrations to set up the database:
```
python manage.py migrate
```

2. Create a superuser (admin account) if needed:
```
python manage.py createsuperuser
```

3. Run the development server:
```
python manage.py runserver
```

4. Access the application in your browser at:
```
http://127.0.0.1:8000/
```

## Notes

- Make sure you have Python 3.8 or higher installed.
- For file uploads and static files, ensure the `media` and `static` directories exist and are writable.