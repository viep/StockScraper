FROM mysql:latest
#Copy schema to /data directory
ADD files/run_db files/init_db files/stockScraperSchema.sql /tmp/
RUN chmod -R 777 /tmp/init_db
RUN /tmp/init_db
ENTRYPOINT /bin/sh

RUN export PATH=$PATH:/usr/local/mysql/bin

RUN apt-get update && \
   apt-get install -y python-dev python-pip && \
   pip install urllib3 && \
   pip install mysql-connector-repackaged && \
   pip install datetime && \
   pip install pandas && \
   pip install SQLAlchemy 
ADD files/stockScraper.py .

CMD ["python", "stockScraper.py"]
