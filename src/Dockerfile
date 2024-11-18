FROM debian:latest

# Install the required packages for C development
RUN apt-get update && \
    apt-get upgrade -y

RUN apt-get install -y \
    build-essential \
    make \
    g++ \
    valgrind \
    strace \
    libreadline-dev \
    git \
    bat \
    jq