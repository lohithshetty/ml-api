FROM python:3
WORKDIR /app/restapi_ml/
COPY . /app/restapi_ml/
RUN pip install -r /app/restapi_ml/requirements.txt
EXPOSE 5000
CMD python /app/restapi_ml/app.py
