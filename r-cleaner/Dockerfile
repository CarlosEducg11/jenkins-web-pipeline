FROM rocker/r-ver:4.2.2

RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && apt-get clean

RUN R -e "install.packages('readr')"

WORKDIR /app

COPY dadosAlagamento.R .

CMD ["Rscript", "dadosAlagamento.R"]