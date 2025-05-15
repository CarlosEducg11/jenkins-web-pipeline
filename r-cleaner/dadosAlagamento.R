# Load CSV
dados <- read.csv("data/dadosAlagamentoPI.csv", sep = ",", na.strings = "", stringsAsFactors = TRUE)

# Basic summaries (can be removed if not needed)
head(dados)
summary(dados)

# Show incomplete Solo entries
dados[!complete.cases(dados$Solo),]

# Fix outlier Temperaturas
tempErrado <- dados[dados$Temperatura < -6 | dados$Temperatura > 41, ]$Temperatura
medianaTemperatura <- median(dados[dados$Temperatura > -6 & dados$Temperatura < 41, ]$Temperatura)
dados[dados$Temperatura < -6 | dados$Temperatura > 41, ]$Temperatura <- medianaTemperatura

# Fix outlier Vazao.atual
vazErrado <- dados[dados$Vazao.atual < 999 | dados$Vazao.atual > 400001, ]$Vazao.atual
medianaVazao <- median(dados[dados$Vazao.atual > 999 & dados$Vazao.atual < 400001, ]$Vazao.atual)
dados[dados$Vazao.atual < 999 | dados$Vazao.atual > 400001, ]$Vazao.atual <- medianaVazao

# Normalize Solo values
dados$Solo[dados$Solo == "arenoso" | dados$Solo == "ARENOSO"] <- "Arenoso"
dados$Solo[dados$Solo == "argiloso" | dados$Solo == "ARGILOSO"] <- "Argiloso"
dados$Solo[dados$Solo == "humifero"] <- "Humífero"
dados$Solo[is.na(dados$Solo)] <- "Arenoso"
dados$Solo <- factor(dados$Solo)

# Save cleaned data
write.csv(dados, "data/dadosCorretosPI.csv", row.names = TRUE)

cat("✔️ Arquivo 'dadosCorretosPI.csv' gerado com sucesso!\n")