FROM rocker/r-ver:4.2.2

# Install system dependencies and MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    mysql-client \
    netcat \
    && apt-get clean

# Install required R packages
RUN install2.r --error \
    DBI \
    RMySQL

# Set working directory
WORKDIR /app

# Copy files
COPY dadosAlagamento.R .
COPY wait-for-mysql.sh .
RUN chmod +x wait-for-mysql.sh

# Start with wait script
CMD ["wait-for-mysql.sh", "db", "Rscript", "dadosAlagamento.R"]
