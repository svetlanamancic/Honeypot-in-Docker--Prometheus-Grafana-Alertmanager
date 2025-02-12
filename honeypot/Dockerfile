FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN find /etc/apt/sources.list* -type f -exec sed -i 'p; s/^deb /deb-src /' '{}' +

RUN apt-get update

WORKDIR /usr/src/cloud/setup

COPY ./setup/ .

RUN apt-get install -y $(cat  requirements1.txt)
RUN bash modify_source.sh
RUN bash install-req.sh

ENV C_PATH /usr/src/cloud/scripts
WORKDIR $C_PATH

COPY ./scripts/ .
RUN chmod +x $C_PATH/container_entry.sh

RUN apt-get install -y python3 pip
RUN pip3 install prometheus-client pygtail

EXPOSE 22
EXPOSE 8000

ENTRYPOINT bash /usr/src/cloud/scripts/container_entry.sh
