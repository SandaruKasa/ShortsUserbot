FROM python:3.10-alpine

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip wheel && pip install --no-cache-dir -r requirements.txt

COPY shorts_userbot.py /app/
ENV PYTHONPATH=/modules/

COPY Shorts.session /var/pyrogram/
VOLUME [ "/var/pyrogram/" ]
ENV PYROGRAM_WORKDIR=/var/pyrogram/

CMD [ "python", "/app/shorts_userbot.py" ]
STOPSIGNAL SIGINT
