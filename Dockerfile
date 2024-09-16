FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/bookstore
COPY requirements.txt ./
COPY fixtures/ ./
COPY entrypoint.sh ./
RUN pip install -r requirements.txt
