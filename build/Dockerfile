FROM alpine
MAINTAINER Christian Gatzlaff <cgatzlaff@gmail.com>

# basic flask environment
RUN apk add --no-cache bash git nginx uwsgi uwsgi-python3 \
    && pip3 install --upgrade pip \
        && pip3 install flask

# application folder
ENV APP_DIR /app

# app dir
RUN mkdir ${APP_DIR} \
    && chown -R nginx:nginx ${APP_DIR} \
        && chmod 777 /run/ -R \
            && chmod 777 /root/ -R
            VOLUME [${APP_DIR}]
            WORKDIR ${APP_DIR}

VOLUME ["/data"]

RUN pip3 install -U connexion
RUN pip3 install -U pickledb

RUN apk add --no-cache libffi-dev autoconf automake libtool
RUN apk add --no-cache gcc python3-dev
RUN apk add --no-cache libressl libressl-dev
RUN apk add --no-cache libc-dev

RUN pip3 install -U web3
RUN pip3 install -U ipython
RUN pip3 install -U numpy

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# copy config files into filesystem
COPY nginx.conf /etc/nginx/nginx.conf
COPY app.ini /app.ini
COPY entrypoint.sh /entrypoint.sh

# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]
