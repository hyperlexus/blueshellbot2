FROM --platform=linux/arm64 arm64v8/ubuntu:latest
RUN apt-get update && apt-get install -y software-properties-common libreadline-dev libterm-readline-gnu-perl software-properties-common \
    && apt-get install -y ffmpeg libavdevice-dev libavformat-dev libavcodec-dev libavutil-dev libswresample-dev libswscale-dev

FROM python:3.10.0
COPY --from=0 /usr/bin/ffmpeg /usr/bin/ffmpeg

ENV LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN git clone https://github.com/hyperlexus/blueshellbot2.git /app
RUN pip install -r requirements.txt

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "main.py"]