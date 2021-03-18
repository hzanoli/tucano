FROM cern/cc7-base:latest

# Add ALICE repository
COPY alice-system-deps.repo /etc/yum.repos.d/

# Install dependencies 
RUN yum update -y \
    && yum install -y \
    alice-o2-full-deps \
    centos-release-scl \
    epel-release \
    lz4-devel \
    ninja-build \
    parallel \
    patch \
    python-pip \
    && yum-config-manager --enable rhel-server-rhscl-7-rpms \
    && yum install -y devtoolset-7 \
    && ln -nfs /usr/bin/ninja-build /usr/local/bin/ninja \
    && yum clean all \
    && rm -rf /var/cache/yum

ARG ALIBUILD_VERSION=1.6.4
# Update pip and alibuild
RUN pip install alibuild==${ALIBUILD_VERSION}

ENV ALIBUILD_WORK_DIR=/workspace/sw

RUN mkdir -p ${ALIBUILD_WORK_DIR}

# Activate devtool-7 by default.
COPY scl_enable /scl/

ENV BASH_ENV=/scl/scl_enable \
    ENV=/scl/scl_enable \
    PROMPT_COMMAND=". /scl/scl_enable"

WORKDIR alice

CMD ["/bin/bash"]
