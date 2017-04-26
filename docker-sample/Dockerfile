FROM ubuntu:trusty

RUN apt-get update

ADD prepare_env.sh /docker/prepare_env.sh

RUN chmod +x /docker/prepare_env.sh
RUN /docker/prepare_env.sh

#EXPOSE 80 443 1234
