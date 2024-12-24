FROM ubuntu:24.04

RUN apt update

RUN apt install python3.12 -y

RUN apt install pip -y

RUN mkdir /apps

WORKDIR /apps

ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --break-system-packages

ADD ./IAC/ .

RUN echo $(ls -1 /apps) 

# ADD requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE 8051

CMD [ "streamlit", "run", "app.py" ]
