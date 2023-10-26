import sqlite3

conn = sqlite3.connect('C:/Users/Usuario/OneDrive/docs/PROJETOS/Apps e Softwares/Softwares/CustomTKinter/Consulta CNPJ/Data/UserData.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL,
    User TEXT NOT NULL,
    Password TEXT NOT NULL
);
""")
print("Conectado a o Banco de Dados")