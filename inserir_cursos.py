import sqlite3

# 🛠 Conecta ao banco de dados (ou cria se não existir)
conn = sqlite3.connect('cursos.db')
cursor = conn.cursor()

# 🗂 Garante que a tabela "cursos" existe (caso não tenha sido criada)
cursor.execute('''
CREATE TABLE IF NOT EXISTS cursos (
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

# 📋 Lista de cursos para inserir
cursos = [
    ("Informática Básica", "Silves - Escola Wilson Carvalho", "21/07/2025", "15/08/2025", "7h às 11h", "80h", "Até 19/07/2025"),
    ("Inglês Básico", "Silves - Escola Wilson Carvalho", "21/07/2025", "29/08/2025", "7h às 11h", "100h", "Até 19/07/2025"),
    ("Alongamento de Unhas em Gel", "Silves - Escola Wilson Carvalho", "21/07/2025", "29/08/2025", "13h às 17h", "80h", "Até 19/07/2025"),
    ("Informática Básica", "Silves - Escola Wilson Carvalho", "21/07/2025", "15/08/2025", "13h às 17h", "80h", "Até 19/07/2025"),
    ("Informática Avançada", "Silves - Escola Wilson Carvalho", "21/07/2025", "22/08/2025", "18h às 22h", "100h", "Até 19/07/2025"),
    ("Agente de Inclusão para Pessoa com TEA", "Silves - Escola Wilson Carvalho", "21/07/2025", "15/09/2025", "18h às 22h", "120h", "Até 19/07/2025")
]

# ✅ Insere apenas se ainda não existir o mesmo curso no mesmo local e horário
for curso in cursos:
    cursor.execute('''
        SELECT COUNT(*) FROM cursos 
        WHERE nome = ? AND local = ? AND horario = ?
    ''', (curso[0], curso[1], curso[4]))
    
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO cursos (nome, local, data_inicio, data_termino, horario, carga_horaria, inscricao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', curso)

# 💾 Salva e fecha a conexão
conn.commit()
conn.close()

# 🖨 Mensagem final
print("✅ Cursos inseridos (sem duplicação) com sucesso!")