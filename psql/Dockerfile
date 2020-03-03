FROM postgres

#RUN mkdir /docker-entrypoint-initdb.d 2>/dev/null
COPY ./entrypoint.sh /docker-entrypoint-initdb.d/init-db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh
