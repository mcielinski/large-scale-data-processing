FROM python:3.7

EXPOSE 8501

COPY requirements.txt ./
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt  && rm requirements.txt

WORKDIR /usr/src/app

# COPY . .