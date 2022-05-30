FROM python:3.11.0a7-alpine3.15

WORKDIR /app

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src .

CMD [ "python", "index.py" ]