FROM python:3.10

RUN apt-get -qq -y update
RUN apt-get -qq -y upgrade

RUN apt-get install -qq -y make

RUN pip install smallscheme
RUN echo '(+ 1 1)' | smallscheme
