# Load necessary packages
library(DBI)
library(RMySQL)

# Connect to MySQL database
con <- dbConnect(
  RMySQL::MySQL(),
  dbname = "app_db",
  host = "db",
  port = 3306,
  user = "projeto",
  password = "projeto",
  client.flag = 131072
)

# Read data from the original table
dados <- dbReadTable(con, "dados_alagamento")

# Show some basic info (optional)
head(dados)
summary(dados)

# Save data as-is to a new table (drop if exists)
if ("rios_corrigidos" %in% dbListTables(con)) {
  dbRemoveTable(con, "rios_corrigidos")
}

# Export to CSV in ./data folder
dir.create("./data", showWarnings = FALSE)
write.csv(dados, "./data/dadosCorretosPI.csv", row.names = FALSE)
cat("✔️ Tabela 'rios_corrigidos' gravada com sucesso no banco MySQL!\n")
cat("✔️ CSV saved to ./data/rios_corrigidos.csv\n")

dbWriteTable(con, "rios_corrigidos", dados, row.names = FALSE, bulk = FALSE)

# Disconnect
dbDisconnect(con)

cat("✔️ Tabela 'rios_corrigidos' gravada com sucesso no banco MySQL!\n")