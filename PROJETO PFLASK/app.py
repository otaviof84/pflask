from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui' 



alunos = [
    {"id": 1, "nome": "João", "idade": 16},
    {"id": 2, "nome": "Sara", "idade": 17}
]

professores = [
    {"id": 1, "nome": "Sr. Carlos", "disciplina": "Matemática"},
    {"id": 2, "nome": "Sra. Ana", "disciplina": "Português"}
]



@app.route('/')
def index():
    return render_template('index.html', titulo='Dashboard')

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html', titulo='Relatórios')

@app.route('/user')
def user():
    return render_template('usuarios.html', titulo='Usuários')

@app.route('/config')
def config():
    return render_template('config.html', titulo='Configurações')

@app.route('/sobre')
def sobre():
    return render_template('sobre_escola.html', titulo='Sobre a Escola')





@app.route('/alunos')
def listar_alunos():
    return render_template('alunos.html', alunos=alunos, titulo='Alunos')

@app.route('/adicionar_aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        novo_id = max([a['id'] for a in alunos]) + 1 if alunos else 1
        alunos.append({
            "id": novo_id,
            "nome": request.form['nome'],
            "idade": int(request.form['idade']) 
        })
        return redirect(url_for('listar_alunos'))
    return render_template('adicionar_aluno.html', titulo='Adicionar Aluno')

@app.route('/editar_aluno/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = next((a for a in alunos if a["id"] == id), None)
    if not aluno:
        return "Aluno não encontrado", 404
    
    if request.method == 'POST':
        aluno['nome'] = request.form['nome']
        aluno['idade'] = int(request.form['idade'])
        return redirect(url_for('listar_alunos'))
        
    return render_template('editar_aluno.html', aluno=aluno, titulo='Editar Aluno')

@app.route('/excluir_aluno/<int:id>')
def excluir_aluno(id):
    global alunos
    alunos = [a for a in alunos if a["id"] != id]
    return redirect(url_for('listar_alunos'))


@app.route('/professores')
def listar_professores():
    return render_template('professores.html', professores=professores, titulo='Professores')

@app.route('/adicionar_professor', methods=['GET', 'POST'])
def adicionar_professor():
    if request.method == 'POST':
        novo_id = max([p['id'] for p in professores]) + 1 if professores else 1
        professores.append({
            "id": novo_id,
            "nome": request.form['nome'],
            "disciplina": request.form['disciplina']
        })
        return redirect(url_for('listar_professores'))
    return render_template('adicionar_professor.html', titulo='Adicionar Professor')

@app.route('/editar_professor/<int:id>', methods=['GET', 'POST'])
def editar_professor(id):
    professor = next((p for p in professores if p["id"] == id), None)
    if not professor:
        return "Professor não encontrado", 404
    
    if request.method == 'POST':
        professor['nome'] = request.form['nome']
        professor['disciplina'] = request.form['disciplina']
        return redirect(url_for('listar_professores'))
        
    return render_template('editar_professor.html', professor=professor, titulo='Editar Professor')

@app.route('/excluir_professor/<int:id>')
def excluir_professor(id):
    global professores
    professores = [p for p in professores if p["id"] != id]
    return redirect(url_for('listar_professores'))






@app.route('/saudacao1/<nome>')
def saudacao1(nome):
    return render_template(
        'saudacao/saudacao.html', 
        valor_recebido=f'Saudação via Rota: Olá, {nome}!',
        titulo='Saudação 1'
    )


@app.route('/saudacao2/')
def saudacao2():
    nome = request.args.get('nome', 'Visitante (nenhum nome enviado)') 
    return render_template(
        'saudacao/saudacao.html', 
        valor_recebido=f'Saudação via Query String: Olá, {nome}!',
        titulo='Saudação 2'
    )


@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']
    
    dados = f"Login Recebido! Usuário: {usuario} | Senha: {senha}"
    
    return render_template(
        'saudacao/saudacao.html', 
        valor_recebido=dados,
        titulo='Login POST'
    )



@app.route('/cadastro')
def formulario_cadastro():
    return render_template('desafio/cadastro.html', titulo='Desafio Obrigatório')

@app.route('/processa_cadastro', methods=['POST'])
def processa_cadastro():
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    cpf = request.form['cpf']
    nome_mae = request.form['nome_mae']
    
    dados_recebidos = {
        'Nome': nome,
        'Data de Nascimento': data_nascimento,
        'CPF': cpf,
        'Nome da Mãe': nome_mae
    }

    return render_template(
        'desafio/resultado.html', 
        dados=dados_recebidos,
        titulo='Dados Recebidos'
    )


if __name__ == '__main__':
    app.run(debug=True)








