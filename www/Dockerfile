FROM php:7-apache
ENV API_ENDPOINT="http://localhost:5000/api/"

COPY ./config/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./config/run_apache.sh /usr/local/bin/run_apache
RUN a2enmod rewrite

COPY src /var/www/
RUN chown -R www-data:www-data /var/www

CMD ["/usr/local/bin/run_apache"]
