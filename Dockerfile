FROM ubuntu:latest

EXPOSE 8080
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
