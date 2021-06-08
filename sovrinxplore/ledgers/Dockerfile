FROM psyhitus/libindy-nodejs

RUN apt-get update && \
    apt-get install -y software-properties-common
    
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update 
RUN apt-get install -y python3.7

RUN python3.7 -m pip install -U pip
RUN python3.7 -m pip install rocksdb==0.7.0 python3-indy


WORKDIR /app

ENTRYPOINT ["python3.7", "ledgers/main.py"]
