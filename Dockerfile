FROM python:3.7-slim-buster
WORKDIR /code/agriworks_platform
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 4000
RUN chmod u+x start.sh
RUN echo ' --host 0.0.0.0' >> start.sh
CMD sh ./start.sh
