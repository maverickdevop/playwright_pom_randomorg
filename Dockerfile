FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    default-jdk \
    && apt-get clean

RUN curl -o allure.tgz -L https://github.com/allure-framework/allure2/releases/download/2.21.0/allure-2.21.0.tgz \
    && tar -zxvf allure.tgz \
    && mv allure-2.21.0 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/bin/allure

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN python -m playwright install --with-deps


WORKDIR /app
COPY . /app

CMD ["pytest", "--alluredir=allure-results"]
