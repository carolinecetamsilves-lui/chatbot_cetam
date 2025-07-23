import sqlite3

# Conecta (ou cria) o banco de dados cursos.db
conn = sqlite3.connect('cursos.db')
cursor = conn.cursor()

# ⚠️ Apaga a tabela "cursos" caso ela já exista (limpa tudo)
cursor.execute('DROP TABLE IF EXISTS cursos')

# 🛠 Cria novamente a tabela com a estrutura correta
cursor.execute('''
CREATE TABLE cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    local TEXT NOT NULL,
    data_inicio TEXT NOT NULL,
    data_termino TEXT NOT NULL, 
    horario TEXT NOT NULL,
    carga_horaria TEXT NOT NULL,
    inscricao TEXT NOT NULL
)
''')

# 🔒 Salva as alterações e fecha a conexão
conn.commit()
conn.close()

# ✅ Mensagem de sucesso
print("✅ Banco de dados resetado com sucesso!")