FROM python:3.10.6-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Executar migrações do Django
#RUN python manage.py migrate

RUN apt-get update && apt-get install -y cron

#DELETE CRON
#RUN rm -rf /etc/cron.d/*

RUN touch /var/log/cron.log
#GRAVANDO COMANDO CRON PARA EXECUTAR O COMANDO DJANGO
RUN echo '30 12 * * * root /usr/local/bin/python /app/manage.py updatepayments >> /var/log/cron.log 2>&1' > /etc/cron.d/my_cron_job

# PERMISSAO DE EXECUCAO CRON
RUN chmod 0644 /etc/cron.d/my_cron_job
# gravacao do cron
RUN crontab /etc/cron.d/my_cron_job


COPY . .


EXPOSE 8000

CMD service cron start  && python manage.py runserver 0.0.0.0:8000
