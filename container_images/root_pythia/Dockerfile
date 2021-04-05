FROM ubuntu:20.04 as builder

RUN apt-get update -qq \
    && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
    && apt-get -y install \
    ca-certificates \
    cmake \
    curl \
    davix-dev \
    dcap-dev \
    fonts-freefont-ttf \
    g++ \
    gcc \
    gfortran \
    git \
    libafterimage-dev \
    libcfitsio-dev \
    libfcgi-dev \
    libfftw3-dev \
    libfreetype6-dev \
    libftgl-dev \
    libgfal2-dev \
    libgif-dev \
    libgl2ps-dev \
    libglew-dev \
    libglu-dev \
    libgraphviz-dev \
    libgsl-dev \
    libjpeg-dev \
    liblz4-dev \
    liblzma-dev \
    libmysqlclient-dev \
    libpcre++-dev \
    libpng-dev \
    libpq-dev \
    libsqlite3-dev \
    libssl-dev \
    libtbb-dev \
    libtiff-dev \
    libx11-dev \
    libxext-dev \
    libxft-dev \
    libxml2-dev \
    libxpm-dev \
    libxxhash-dev \
    libz-dev \
    libzstd-dev \
    locales \
    make \
    python-dev \
    python3-dev \
    python3-numpy \
    rsync \
    srm-ifce-dev \
    unixodbc-dev \
    wget

RUN mkdir /build

#Install LHDPDF
ARG LHAPDF_VERSION=6.3.0
WORKDIR /sources
RUN curl -o /sources/lhapdf.tgz https://lhapdf.hepforge.org/downloads/?f=LHAPDF-${LHAPDF_VERSION}.tar.gz  \
    && tar -xzf /sources/lhapdf.tgz \
    && rm /sources/lhapdf.tgz  \
    && cd /sources/LHAPDF-${LHAPDF_VERSION}  \
    && ./configure --prefix=/usr/local \
    && make -j`nproc` \
    && make -j`nproc` install \
    && rm -rf /sources/LHAPDF-${LHAPDF_VERSION}

# Install PYTHIA8
ARG PYTHIA_VERSION=8303
RUN curl -o /sources/pythia8.tgz -s -S http://home.thep.lu.se/~torbjorn/pythia8/pythia${PYTHIA_VERSION}.tgz \
    && tar -xzf pythia8.tgz \
    && rm /sources/pythia8.tgz \
    && cd /sources/pythia${PYTHIA_VERSION} \
    && ./configure --prefix=/usr/local \
    --with-lhapdf6=/usr/local --enable-optdebug \
    && make -j`nproc` \
    && make -j`nproc` install \
    && rm -rf /sources/pythia${PYTHIA_VERSION}


#Install ROOT
ARG ROOT_VERSION=6.22.06
RUN curl -o /sources/root.tar.gz -s -S https://root.cern/download/root_v${ROOT_VERSION}.source.tar.gz \
    && tar -xzf root.tar.gz \
    && rm /sources/root.tar.gz \
    && mkdir /root-build \
    && cd /root-build \
    && cmake -Dgnuinstall=ON \
       /sources/root-${ROOT_VERSION} \
    && cmake --build . --target install -j`nproc`\
    && rm -rf /root-build

RUN ldconfig

# Install extra PDF sets
RUN lhapdf install CT14nnloIC

WORKDIR /workspace

CMD ["/bin/bash -c "]