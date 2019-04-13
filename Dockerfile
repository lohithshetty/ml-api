FROM ubuntu:18.10

RUN apt-get update -y && apt-get install -y python3 python3-dev python3-pip 

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["/bin/bash", "deploy-rest-ml.sh" ]
