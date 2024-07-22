FROM python:3.8.0-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python","seeder.py" ]