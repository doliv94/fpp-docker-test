FROM ubuntu:24.04

WORKDIR /app
COPY mpi-files /app
COPY machinefile /app
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN apt update
RUN apt install -y nano

COPY hosts /etc

RUN apt update
RUN apt install -y python3 
RUN apt install -y python3-pip
RUN apt install -y python3-numpy
RUN apt install -y python3-mpi4py

RUN apt update
RUN apt-get install -y nfs-server
RUN apt-get install -y nfs-client

RUN apt update 
RUN apt-get install -y openssh-server

RUN mkdir /var/run/sshd
RUN echo "root:1234" | chpasswd
RUN sed -i "s/PermitRootLogin prohibit-password/PermitRootLogin yes/" /etc/ssh/sshd_config

COPY id_rsa_shared ./.ssh
COPY id_rsa_shared.pub ./.ssh
COPY id_rsa_shared.pub /root/.ssh/authorized_keys

RUN sed "s@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g" -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN apt-get install -y build-essential
RUN apt-get install -y mpich
RUN apt-get install -y mpich-doc

RUN apt-get install -y iputils-ping
RUN apt-get install -y openmpi-bin 
RUN apt-get install -y openmpi-doc 
RUN apt-get install -y libopenmpi-dev

RUN apt update

RUN useradd -ms /bin/bash admin
RUN echo "admin:1234" | chpasswd
RUN chown -R admin:admin /app
RUN chmod 755 /app

EXPOSE 22
ENTRYPOINT service ssh start && bash