FROM python:latest

WORKDIR /home/azure/ecommerce

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN \
 apt-get -y update && apt-get -y upgrade && apt-get -y install wget apt-utils ca-certificates lsb-release && \
 sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
 wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
 apt-get update && \
 apt-get -y install python3-dev libffi-dev && \
 apt-get -y install gcc musl-dev postgresql postgresql-contrib netcat
 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
