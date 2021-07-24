##AVAILABLE IN th3h04x/bountycat in dockerhub
FROM ubuntu

WORKDIR /opt

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install git -y
RUN apt-get install python3-pip -y

#cloning repo
RUN git clone https://github.com/blessingcharles/bountycat.git
RUN cd /opt/bountycat && pip3 install -r requirements.txt

#setting up the gecko driver
RUN apt-get install wget
RUN apt-get install tar
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN export PATH=$PATH:.

#additional requirements
RUN apt-get install iputils-ping -y


#running the basic start script
ENTRYPOINT ["python3","/opt/bountycat/start.py"]