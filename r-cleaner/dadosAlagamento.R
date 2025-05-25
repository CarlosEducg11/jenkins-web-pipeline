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

# Show incomplete Solo entries
dados[!complete.cases(dados$Solo),]

# Fix outlier Temperaturas
medianaTemperatura <- median(dados[dados$Temperatura > -6 & dados$Temperatura < 41, ]$Temperatura, na.rm = TRUE)
dados[dados$Temperatura < -6 | dados$Temperatura > 41, ]$Temperatura <- medianaTemperatura

# Fix outlier Vazao.atual
medianaVazao <- median(dados[dados$Vazao.atual > 999 & dados$Vazao.atual < 400001, ]$Vazao.atual, na.rm = TRUE)
dados[dados$Vazao.atual < 999 | dados$Vazao.atual > 400001, ]$Vazao.atual <- medianaVazao

# Normalize Solo values
dados$Solo <- tolower(dados$Solo)
dados$Solo[dados$Solo == "humifero"] <- "Humífero"
dados$Solo[dados$Solo == "arenoso"] <- "Arenoso"
dados$Solo[dados$Solo == "argiloso"] <- "Argiloso"
dados$Solo[is.na(dados$Solo)] <- "Arenoso"
dados$Solo <- factor(dados$Solo)

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