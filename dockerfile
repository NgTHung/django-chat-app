FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
ADD . /src

RUN pip install -r requirements.txt

RUN ./manage.py migrate
RUN ./manage.py collectstatic --no-input

CMD python server.py 3013

EXPOSE 3013