FROM python:3.6-alpine3.8

RUN mkdir /tmp/requirement && mkdir /awdff

COPY requirement/ /tmp/requirement

RUN pip3 install -r /tmp/requirement/dev.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && apk add -U tzdata

#设置时区
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' >/etc/timezone

WORKDIR /awdff