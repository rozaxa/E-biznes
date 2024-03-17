FROM ubuntu:20.04

ENV TZ=Europe/Warsaw
EXPOSE 8080 

RUN apt-get update -y && \
    apt-get install -y python3.8

RUN apt-get install -y openjdk-8-jdk


RUN apt-get install -y python3-pip && \
    python3.8 -m pip install --upgrade pip

RUN apt-get install -y wget unzip
RUN wget https://github.com/JetBrains/kotlin/releases/download/v1.6.10/kotlin-compiler-1.6.10.zip
RUN unzip kotlin-compiler-1.6.10.zip -d /opt/

ENV PATH="${PATH}:/opt/kotlinc/bin"

RUN wget https://services.gradle.org/distributions/gradle-7.4-bin.zip
RUN unzip gradle-7.4-bin.zip -d /opt/
ENV PATH="${PATH}:/opt/gradle-7.4/bin"

WORKDIR /app

COPY build.gradle .

CMD ["sh", "-c", "python3 --version && java -version && kotlinc -version && gradle -version"]
