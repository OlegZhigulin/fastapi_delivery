FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["app.main:app"]