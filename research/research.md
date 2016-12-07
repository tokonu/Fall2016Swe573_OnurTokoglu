TestApp written by the tutorial https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

Notes:
- to run mysql server from terminal /Applications/MAMP/Library/bin/mysql -u root -p
- if pycharm freezes in startup rm -rf .idea


Further reference: 

Jinja tutorial - https://realpython.com/blog/python/primer-on-jinja-templating/

Another tutorial - http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
- https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/

Github markdown cheatsheet - https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet


docker tutorial https://docs.docker.com/engine/tutorials/usingdocker/

Docker build image - docker build -t tokonu/swe573 .
Docker run image - docker run -i -t -d -P --name onur tokonu/swe573 python run.py
or /bin/bash instead of python run.py

docker images
docker rmi <image id>
docker rm <container name/id>
docker port <container name>
docker ps -a

!! have to run flask with flask.run(host="0.0.0.0") so that app replies running in docker container


//for ubuntu
FROM ubuntu:14.04
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python-all python-pip
ENV PYTHON_VERSION 3.5.2
ADD . /opt/webapp
RUN pip install -qr /opt/webapp/requirements.txt
WORKDIR /opt/webapp
EXPOSE 5000

then
sudo apt-get install python3-pip
pip3 install -r requirements.txt


uploading files to ec2 http://angus.readthedocs.io/en/2014/amazon/transfer-files-between-instance.html
flask ec2 tutorial - http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/
docker on ec2 - http://www.ybrikman.com/writing/2015/11/11/running-docker-aws-ground-up/


connect to ec2
ssh -i "swe573key.pem" ec2-user@ec2-54-174-216-122.compute-1.amazonaws.com

sudo yum install -y git-all
git clone https://github.com/tokonu/Fall2016Swe573_OnurTokoglu.git
cd Fall2016Swe573_OnurTokoglu/src
docker build -t tokonu/swe573:1.0 .













