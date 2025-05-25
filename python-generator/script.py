import random
import mysql.connector
import time
from mysql.connector import Error

for i in range(10):
    try:
        conn = mysql.connector.connect(
            host="db",
            user="projeto",
            password="projeto",
            database="app_db",
            port=3306
        )
        print("Connected to DB!")
        break
    except Error as e:
        print(f"Retrying DB connection ({i+1}/10): {e}")
        time.sleep(3)
else:
    print("Failed to connect to DB after retries.")

cursor = conn.cursor()

# Data generation
ffT = [False, False, True]
ttF = [False, True, True]
solos = ['Arenoso', 'Arenoso', 'Arenoso', 'Argiloso', 'Argiloso', 'Humífero',
         'arenoso', 'ARENOSO', 'arenoso', 'argiloso', 'ARGILOSO', 'humifero']
notas = ['Queimada Recente', 'Historicamente alagavel', 'Mare alta']

for idRio in range(10):
    mediaVazao = round(random.triangular(2000, 200000, 5000))

    if random.random() < 0.05:
        vazao = round(random.triangular(mediaVazao*50, mediaVazao*200, mediaVazao*100))
    else:
        vazao = round(random.triangular(mediaVazao/2, mediaVazao*2, mediaVazao))

    miliHora = round(random.triangular(0, 65, 5)) if random.random() < 0.5 else 0
    miliDia = round(random.triangular(0, 100, 0))
    mili7 = round(random.triangular(0, 500, 4))
    temp = round(random.triangular(70, 500, 300)) if random.random() < 0.05 else round(random.triangular(-5, 40, 24))
    veloVen = round(random.triangular(20, 110, 20)) if miliHora >= 10 else round(random.triangular(1, 40, 5))

    costa = random.choice(ffT)
    cidade = random.choice(ffT)
    vegetacao = random.choice(ttF)
    montanha = random.choice(ffT)
    solo = None if random.random() < 0.05 else random.choice(solos)
    nota = random.choice(notas) if random.random() < 0.15 else None

    alagou = False
    if vazao > (mediaVazao * 1.5):
        alagou = True
    elif miliHora > 35 and miliDia > 70:
        alagou = True
    elif temp > 30 and montanha:
        alagou = True
    elif miliHora > 60 and veloVen < 15:
        alagou = True
    elif (solo and 'arenoso' in solo.lower()) and not vegetacao and miliHora > 40:
        alagou = True
    elif mili7 > 400 and cidade:
        alagou = True
    elif costa and nota == 'Mare alta':
        alagou = True

    # Insert into MySQL
    cursor.execute("""
        INSERT INTO dados_alagamento (
            media_vazao, vazao, mili_hora, mili_dia, mili_7,
            temperatura, velocidade_vento, costa, cidade, vegetacao,
            montanha, solo, nota, alagou
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        mediaVazao, vazao, miliHora, miliDia, mili7,
        temp, veloVen, costa, cidade, vegetacao,
        montanha, solo, nota, alagou
    ))

conn.commit()
cursor.close()
conn.close()