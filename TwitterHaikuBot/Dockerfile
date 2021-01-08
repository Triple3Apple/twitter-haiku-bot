FROM python:3.7-alpine

COPY bot/haikumaker.py /bot/
COPY bot/badhaikubot.py /bot/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bot
CMD ["python3", "badhaikubot.py"]