FROM python:3.6.7
ENV PYTHONUNBUFFERED 1
COPY pip.conf /root/.pip/pip.conf
RUN mkdir -p /usr/local/myserver/spsback
WORKDIR /usr/local/myserver/spsback
ADD . /usr/local/myserver/spsback
RUN pip install -r requirements.txt
