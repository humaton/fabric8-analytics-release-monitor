FROM registry.centos.org/centos/centos:7
MAINTAINER Tomas Hrcka <thrcka@redhat.com>

ENV LANG=en_US.UTF-8 \
    F8A_WORKER_VERSION=30100bf

RUN useradd coreapi

RUN yum --setopt=tsflags=nodocs install -y epel-release && \
    yum --setopt=tsflags=nodocs install -y gcc python34-pip git wget python34-devel libxml2-devel libxslt-devel python34-pycurl && \
    yum clean all

RUN mkdir -p /home/release_monitor/

COPY . /tmp/release_monitor/
COPY hack/run_release_monitor.sh /usr/bin/

RUN pushd /tmp/release_monitor/ && \
    pip3 install --upgrade pip && pip install --upgrade wheel && \
    pip3 install . && \
    pip3 install -r /tmp/release_monitor/requirements.txt && \
    pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@${F8A_WORKER_VERSION} && \
    popd && \
    rm -rf /tmp/release_monitor

USER coreapi

CMD ["/usr/bin/run_release_monitor.sh"]
