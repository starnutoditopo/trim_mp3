FROM python:3.9
ENV PYTHONUNBUFFERED 1

#RUN apt-get -y update && \
#    apt-get -y install ffmpeg libavcodec-extra && \
#        libfdk-aac-dev libass-dev libopus-dev libtheora-dev libvorbis-dev libvpx-dev libssl-dev \
#        nasm

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

