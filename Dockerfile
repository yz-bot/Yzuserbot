# We're using Ubuntu 20.10
FROM ximfine/xproject:buster

#
# Clone repo and prepare working directory
#
RUN git clone -o yz https://github.com/yz-bot/Yzuserbot /root/userbot
RUN mkdir /root/userbot/.bin
RUN pip install --upgrade pip setuptools
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install -r https://'githubusercontent.com'/yz-bot/Yzuserbot/requirements.txt

CMD ["python3","-m","userbot"]
