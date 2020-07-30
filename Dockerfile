FROM python:3.7-slim-buster
WORKDIR /code/agriworks_platform
COPY requirements.txt requirements.txt
# RUN apt-get update && apt-get install python3 pip3 -y
# RUN apt update && apt -y install python3-pip
RUN pip3 install -r requirements.txt
RUN apt update && apt -y install curl
COPY . .
EXPOSE 4000
RUN chmod u+x start.sh
# RUN ./start.sh &
# RUN FLASK_APP=application.py
# RUN FLASK_ENV=development
# RUN FLASK_RUN_PORT=4000

# RUN apt update && apt -y install curl gnupg
# RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
# RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
# RUN apt -y install git yarn && apt-get -y install nodejs

##UNCOMMENT
# RUN curl localhost:4000
# WORKDIR /code/
# RUN git clone https://github.com/Hack4Impact-Boston-University/agriworks_portal
# WORKDIR /code/agriworks_portal
# RUN yarn install
# EXPOSE 8080
# CMD ["yarn", "run", "serve"]

CMD sh ./start.sh
# CMD ["./start.sh"]
# ["chmod", "+x", "start.sh", "&&", "./start.sh"]