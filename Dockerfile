FROM python:3.10.6-slim-buster

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]