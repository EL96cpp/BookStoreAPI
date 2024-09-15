python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata fixtures/books.json
python3 manage.py loaddata fixtures/stores.json
python3 manage.py loaddata fixtures/customers.json
python3 manage.py loaddata fixtures/reviews.json
python3 manage.py runserver 0.0.0.0:8000