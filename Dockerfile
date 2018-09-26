FROM registry.centos.org/centos/centos:7
MAINTAINER Tomas Hrcka <thrcka@redhat.com>

ENV LANG=en_US.UTF-8 \
    F8A_WORKER_VERSION=30100bf

RUN useradd coreapi

RUN yum --setopt=tsflags=nodocs install -y epel-release && \
    yum --setopt=tsflags=nodocs install -y gcc python34-pip git wget python34-devel libxml2-devel libxslt-devel python34-pycurl && \
    yum clean all

RUN mkdir -p /home/release_monitor/

COPY . /home/release_monitor/

WORKDIR /home/release_monitor/

RUN pip3 install --upgrade pip && pip install --upgrade wheel && \
    pip3 install -r /home/release_monitor/requirements.txt && \
    pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@${F8A_WORKER_VERSION}

USER coreapi

CMD ["python3", "/home/release_monitor/release_monitor.py"]
