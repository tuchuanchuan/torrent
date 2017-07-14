FROM centos:7

User root

RUN yum install -y boost boost-devel
RUN yum install -y make gcc gcc-c++ kernel-devel python-devel
RUN mkdir -p /usr/src &&
    wget https://github.com/arvidn/libtorrent/releases/download/libtorrent-1_0_10/libtorrent-rasterbar-1.0.10.tar.gz -O /usr/src/libtorrent-rasterbar-1.0.10.tar.gz

WORKDIR /usr/src

RUN tar zxvf libtorrent-rasterbar-1.0.10.tar.gz
RUN cd libtorrent-rasterbar-1.0.10 && ./configure --disable-debug --with-boost-libdir=/usr/lib64 --disable-encryption --enable-python-binding
RUN make && make install
ENV LD_LIBRARY_PATH /usr/local/lib/
RUN cd bindings/python && python setup.py build && python setup.py install
