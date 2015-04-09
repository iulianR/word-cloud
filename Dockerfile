# Set the base image to Ubuntu
FROM    ubuntu:utopic

RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip

# Copy and install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Define working directory
WORKDIR /src
ADD . /src
