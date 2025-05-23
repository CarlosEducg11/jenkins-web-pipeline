USE app_db;

CREATE TABLE IF NOT EXISTS dados_alagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    media_vazao FLOAT,
    vazao FLOAT,
    mili_hora INT,
    mili_dia INT,
    mili_7 INT,
    temperatura FLOAT,
    velocidade_vento FLOAT,
    costa BOOLEAN,
    cidade BOOLEAN,
    vegetacao BOOLEAN,
    montanha BOOLEAN,
    solo VARCHAR(50),
    nota VARCHAR(100),
    alagou BOOLEAN
);