FROM citizenstig/dvwa:latest

RUN apt-get update

RUN apt-get install ssh -y

COPY run.sh /

RUN chmod 777 /run.sh
RUN chmod -R 777 /var/www/html