FROM python:3.9.6-alpine

WORKDIR /home/azure/ecommerce

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN \
 apk add --no-cache postgresql-libs python3-dev libffi-dev && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev 
 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
