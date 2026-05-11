from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# FALHA 1: Debug mode ligado (Permite execução de código remoto se houver erro)
app.config['DEBUG'] = True 

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.execute('CREATE TABLE users (id INTEGER, user TEXT, secret TEXT)')
    conn.execute("INSERT INTO users VALUES (1, 'admin', 'SENHA_EXPOSTA_123')")
    return conn

db = init_db()

@app.route('/')
def index():
    # FALHA 2: Cross-Site Scripting (XSS) - Reflete o que vem na URL sem filtrar
    name = request.args.get('name', 'Visitante')
    return render_template_string(f'<h1>Olá, {name}</h1><p>Vá para /user?id=1</p>')

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    
    # FALHA 3: SQL Injection - Concatenando entrada do usuário diretamente na query
    query = f"SELECT user, secret FROM users WHERE id = {user_id}"
    
    try:
        cursor = db.execute(query)
        result = cursor.fetchone()
        return f"Dados: {result}"
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    # FALHA 4: Bind em 0.0.0.0 (Exposição desnecessária em redes públicas)
    app.run(host='0.0.0.0', port=5000)
