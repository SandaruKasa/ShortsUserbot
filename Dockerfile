FROM python:3.10-alpine

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY userbot /modules/userbot
ENV PYTHONPATH=/modules/

COPY *.session /var/pyrogram/
VOLUME [ "/var/pyrogram/" ]
ENV PYROGRAM_WORKDIR=/var/pyrogram/

CMD [ "python", "-m", "userbot" ]
STOPSIGNAL SIGINT
