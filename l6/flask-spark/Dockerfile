FROM python:3.7 
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

RUN echo 'deb "http://ftp.debian.org/debian" stretch main\ndeb-src "http://ftp.de.debian.org/debian" stretch main' > /etc/apt/sources.list.d/java.list
RUN apt-get update && apt-get install -y openjdk-8-jdk && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./  
RUN pip install --no-cache-dir -r requirements.txt  && rm requirements.txt 

WORKDIR /app

RUN useradd -ms /bin/bash sample
USER sample