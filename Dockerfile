FROM python:3.6-alpine3.8

RUN mkdir /tmp/requirement && mkdir /awdff

COPY requirement/ /tmp/requirement

RUN pip3 install -r /tmp/requirement/dev.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

WORKDIR /awdff