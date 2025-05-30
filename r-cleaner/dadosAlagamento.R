<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1a39fbc (a)
library(filelock)

print("Entrando em Loop")
repeat {
  print("Loop")

  # Aguarda até o arquivo existir
  while (!file.exists("data/dadosAlagamentoPI.csv")) {
    print("Arquivo ainda não criado. Aguardando...")
    Sys.sleep(1)
  }

  # Tenta obter lock exclusivo
  lock_path <- "data/dadosAlagamentoPI.csv.lock"
  lock <- filelock::lock(lock_path, timeout = 5000)

  if (!is.null(lock)) {
    atual_mtime <- file.info("data/dadosAlagamentoPI.csv")$mtime

    if (!exists("last_mtime") || atual_mtime != last_mtime) {
      print("Dados divergentes, re-tratando")

      # Carrega e trata dados
      dados <- read.csv("data/dadosAlagamentoPI.csv", sep=",", na.strings = "", stringsAsFactors = T)
      
      # Tratamento temperatura
      medianaTemperatura <- median(dados[dados$Temperatura > -6 & dados$Temperatura < 41, ]$Temperatura, na.rm = TRUE)
      dados$Temperatura[dados$Temperatura < -6 | dados$Temperatura > 41] <- medianaTemperatura
      
      # Tratamento vazão
      dados <- subset(dados, Vazao.atual < Vazao.Media * 2)

      # Tratamento solo
      dados$Solo <- tolower(dados$Solo)
      dados$Solo[dados$Solo == "arenoso"] <- "Arenoso"
      dados$Solo[dados$Solo == "argiloso"] <- "Argiloso"
      dados$Solo[dados$Solo == "humifero"] <- "Humífero"
      dados$Solo[is.na(dados$Solo)] <- "Arenoso"
      dados$Solo <- factor(dados$Solo)

      # ID e index
      dados <- dados[, -1]
      row.names(dados) <- NULL

      # Renomeia colunas
      colnames(dados) <- c("vazaoMedia","vazaoAtual","milimitroHora","milimitroDia","milimitroSeteDias",
                           "temperatura","velocidadeVento","costa","cidade","vegetacao",
                           "montanha","solo","notas","alagou")

      write.csv(dados, "data/dadosCorretosPI.csv", row.names = TRUE)

      print("Dados divergentes tratados")
      last_mtime <- atual_mtime
    }

    # Libera o lock
    unlock(lock)
  } else {
    print("Arquivo está em uso por outro processo. Tentando novamente...")
  }

  Sys.sleep(5)
<<<<<<< HEAD
=======
csv_path <- "data/dadosAlagamentoPI.csv"
last_mtime <- NULL

# Wait until file has rows
repeat {
  cat("Checking if CSV has data...\n")
  if (file.exists(csv_path)) {
    dados <- read.csv(csv_path, sep=",", na.strings="", stringsAsFactors=TRUE)
    if (nrow(dados) > 0) {
      cat("CSV has at least one data row. Proceeding...\n")
      break
    }
  }
  Sys.sleep(5)
}

# Initial processing
process_dados <- function(dados) {
  if (nrow(dados) == 0) {
    cat("No rows to process. Skipping...\n")
    return(NULL)
  }

  # Tratamento temperatura
  medianaTemperatura <- median(dados[dados$Temperatura > -6 & dados$Temperatura < 41, "Temperatura"], na.rm = TRUE)
  dados[dados$Temperatura < -6 | dados$Temperatura > 41, "Temperatura"] <- medianaTemperatura

  # Tratamento vazão
  dados <- subset(dados, Vazao.atual < Vazao.Media * 2)

  # Tratamento solo
  dados$Solo <- as.character(dados$Solo)
  dados$Solo[dados$Solo %in% c("arenoso", "ARENOSO")] <- "Arenoso"
  dados$Solo[dados$Solo %in% c("argiloso", "ARGILOSO")] <- "Argiloso"
  dados$Solo[dados$Solo == "humifero"] <- "Humífero"
  dados$Solo[is.na(dados$Solo)] <- "Arenoso"
  dados$Solo <- factor(dados$Solo)

  # Tratamento ID e index
  dados <- dados[ , -1, drop = FALSE]
  row.names(dados) <- NULL

  # Renomear colunas
  colnames(dados) <- c("vazaoMedia","vazaoAtual","milimitroHora","milimitroDia","milimitroSeteDias","temperatura","velocidadeVento","costa","cidade","vegetacao","montanha","solo","notas","alagou")

  # Escreve dados tratados
  write.csv(dados, "dadosCorretosPI.csv", row.names = TRUE)
  return(dados)
}

dados <- process_dados(dados)
last_mtime <- file.info(csv_path)$mtime
cat("[Entrando em Loop]\n")

# Loop para atualização
repeat {
  cat("[Loop]\n")

  if (!file.exists(csv_path)) {
    cat("File missing, skipping...\n")
    Sys.sleep(15)
    next
  }

  atual_mtime <- file.info(csv_path)$mtime
  if (is.na(atual_mtime) || is.na(last_mtime)) {
    Sys.sleep(15)
    next
  }

  if (atual_mtime != last_mtime) {
    cat("New version of CSV detected.\n")
    dados <- read.csv(csv_path, sep=",", na.strings="", stringsAsFactors=TRUE)
    if (nrow(dados) > 0) {
      process_dados(dados)
      cat("Data processed.\n")
    } else {
      cat("New file is empty. Skipping.\n")
    }
    last_mtime <- atual_mtime
  }

  Sys.sleep(15)
>>>>>>> b4de054 (a)
=======
>>>>>>> 1a39fbc (a)
}