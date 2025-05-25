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
  password = "projeto"
)

# Read data from the table (e.g., 'rios')
dados <- dbReadTable(con, "rios")

# View basic info
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

# Save cleaned data to a new table (drop if it already exists)
if ("rios_corrigidos" %in% dbListTables(con)) {
  dbRemoveTable(con, "rios_corrigidos")
}
dbWriteTable(con, "rios_corrigidos", dados, row.names = FALSE)

# Disconnect
dbDisconnect(con)

cat("✔️ Tabela 'rios_corrigidos' gravada com sucesso no banco MySQL!\n")
