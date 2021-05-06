FROM python:3.6.13
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /opt/make_dataset

RUN pip install -r /opt/make_dataset/requirements.txt

WORKDIR /opt/make_dataset
