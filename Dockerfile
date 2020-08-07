FROM python:3.7-slim-buster
WORKDIR /platform
ENV FLASK_ENV development
ENV FLASK_APP application.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 4000
COPY . .
RUN pip install -r requirements.txt
EXPOSE 4000
CMD flask run