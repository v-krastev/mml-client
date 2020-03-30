FROM python:3.7.7-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        libasound2-dev \
	ffmpeg \
	&& apt-get clean

RUN python -m pip install -r requirements.txt

EXPOSE 5000/tcp

ENTRYPOINT ["python", "main.py"]
