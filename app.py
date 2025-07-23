from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
# Rota para listar apenas os nomes dos cursos (usado no frontend para exibir botões de cursos)
@app.route('/cursos')
def listar_cursos():
    conn = sqlite3.connect('cursos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT nome FROM cursos')  # DISTINCT evita nomes repetidos
    cursos = [{'nome': row[0]} for row in cursor.fetchall()]
    conn.close()
    return jsonify({'cursos': cursos})

# Rota para buscar informações completas de um curso pelo nome
@app.route('/curso_info')
def curso_info():
    nome = request.args.get('nome')
    conn = sqlite3.connect('cursos.db')
    cursor = conn.cursor()
    # Seleciona todas as informações de um curso pelo nome
    cursor.execute('''
        SELECT nome, local, data_inicio, data_termino, horario, carga_horaria, inscricao 
        FROM cursos 
        WHERE nome = ?
        LIMIT 1
    ''', (nome,))
    row = cursor.fetchone()
    conn.close()

    if row:
        curso = {
            'nome': row[0],
            'local': row[1],
            'data_inicio': row[2],
            'data_termino': row[3],
            'horario': row[4],
            'carga_horaria': row[5],
            'inscricao': row[6]
        }
        return jsonify({'success': True, 'curso': curso})
    else:
        return jsonify({'success': False, 'message': 'Curso não encontrado'})

# Rota principal para exibir o HTML (chatbot)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para responder as mensagens do chatbot
@app.route('/responder', methods=['POST'])
def responder():
    user_message = request.json['message'].lower()

    if "curso" in user_message:
        conn = sqlite3.connect('cursos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT nome, local, data_inicio, data_termino, carga_horaria FROM cursos')
        cursos = cursor.fetchall()
        conn.close()

        if cursos:
            resposta = "📋 Cursos Disponíveis:\n"
            for curso in cursos:
                resposta += f"- {curso[0]} em {curso[1]} (De {curso[2]} a {curso[3]} - {curso[4]})\n"
        else:
            resposta = "❗️ Não há cursos cadastrados no momento."

#Rota de respostas para as informações 
    elif "inscrição" in user_message or "período" in user_message:
        resposta = "📅 As inscrições estão abertas até 30/07/2025."

    elif "edital" in user_message:
        resposta = (
            "📄 Acesse o edital: "
            "<a href='https://www.cetam.am.gov.br/wp-content/uploads/2025/07/Edital-006_2025-Etapa-2.pdf' target='_blank'>"
            "Clique aqui para abrir o edital</a>"
        )

    elif "cadastro" in user_message:
        resposta = (
            "ℹ️ Dúvidas sobre cadastro? Assista ao vídeo explicativo: "
            "<a href='https://www.youtube.com/watch?v=zR0d9Td9Jpw' target='_blank'>Clique aqui para abrir o vídeo</a>"
        )

    elif "portal" in user_message:
        resposta = (
            "👩‍🎓 Portal do candidato, acesse: "
            "<a href='https://inscricao.cetam.am.gov.br/' target='_blank'>Clique aqui para entrar</a>"
        )

    elif "secretaria" in user_message or "fale" in user_message:
        resposta = (
            "📞 Para falar com a secretaria ETP Wilson Carvalho Pereira, envie sua mensagem para: "
            "<a href='https://wa.me/559294853462' target='_blank'>Clique aqui</a>"
        )

    elif "segunda via" in user_message:
        resposta = (
            "📄 Para solicitar a 2ª via do certificado, envie um e-mail com seu nome completo e curso para: "
            "cetam_certificados@edu.cetam.am.gov.br"
        )

    elif "agendamento" in user_message:
        resposta = "📅 Para agendar atendimento, acesse: https://www.cetam.am.gov.br/agendamento"

    else:
        resposta = (
            "Desculpe, não entendi sua pergunta. Por favor, escolha uma opção do menu."
        )

    return jsonify({'response': resposta})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
