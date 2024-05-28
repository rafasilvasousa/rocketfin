FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y redis-server

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]