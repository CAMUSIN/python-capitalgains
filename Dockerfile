FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y

ADD main.py .

WORKDIR /usr/src/app

COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./main.py" ]