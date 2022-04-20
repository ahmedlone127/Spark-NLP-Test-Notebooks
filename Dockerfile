 
FROM ubuntu:latest
WORKDIR   /app/src/new
COPY nlu_test_runs.py .
ENV   LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN apt update \
   
	&& apt install -y software-properties-common nano \
  
  	&& add-apt-repository ppa:deadsnakes/ppa \
    
	&& apt update -y \
  
	&& apt install -y python3.7 \
 
	&& apt install -y python3-pip \
    
    
	&& apt-get install -y openjdk-8-jre
RUN echo 'alias python=python3.7' >> ~/.bashrct 
# RUN export PYSPARK_PYTHON=/usr/bin/python3.7

ENV PYSPARK_PYTHON=/usr/bin/python3.7
RUN python3.7 -m pip install  pyspark==3.0.3 spark-nlp==3.4.3 \
	&& apt -y install git \
 	&& git clone https://github.com/ahmedlone127/spark-nlp-workshop \
	&& python3.7 -m pip install nbconvert \
 
	&& python3.7 -m pip install numpy \
 
	&& apt -y install nano \
	
	&& apt-get install wget
CMD ["python3.7", "nlu_test_runs.py","-f","/app/src/new/spark-nlp-workshop/jupyter/annotation/english/spark-nlp-basics/"]
