from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Chave secreta obrigatória para usar as mensagens 'flash'
app.config['SECRET_KEY'] = 'chave_muito_secreta_e_forte_para_o_ifpi' 


# --- DADOS EM MEMÓRIA ---
alunos = [
    {"id": 1, "nome": "João Silva", "idade": 16},
    {"id": 2, "nome": "Sara Lima", "idade": 17}
]

professores = [
    {"id": 1, "nome": "Sr. Carlos", "disciplina": "Matemática"},
    {"id": 2, "nome": "Sra. Ana", "disciplina": "Português"}
]


# --- FUNÇÕES AUXILIARES ---
def _proximo_id(lista):
    """Retorna o próximo ID disponível para a lista."""
    return max([item['id'] for item in lista]) + 1 if lista else 1

def _buscar_por_id(lista, id):
    """Retorna um item pelo ID ou None."""
    # Usamos str(id) para garantir que funcione, caso o ID seja passado como string.
    return next((item for item in lista if str(item["id"]) == str(id)), None)


# --- ROTAS PRINCIPAIS (MANTIDAS) ---

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

# Rota de login/cadastro, etc., mantidas...
@app.route('/saudacao1/<nome>')
def saudacao1(nome):
    return render_template('saudacao/saudacao.html', valor_recebido=f'Saudação via Rota: Olá, {nome}!', titulo='Saudação 1')

@app.route('/saudacao2/')
def saudacao2():
    nome = request.args.get('nome', 'Visitante (nenhum nome enviado)') 
    return render_template('saudacao/saudacao.html', valor_recebido=f'Saudação via Query String: Olá, {nome}!', titulo='Saudação 2')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']
    dados = f"Login Recebido! Usuário: {usuario} | Senha: {senha}"
    return render_template('saudacao/saudacao.html', valor_recebido=dados, titulo='Login POST')

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

    return render_template('desafio/resultado.html', dados=dados_recebidos, titulo='Dados Recebidos')


# ------------------------------------------------------------------
# --- ROTAS DE ALUNOS (CRUD COMPLETO) ---
# ------------------------------------------------------------------

@app.route('/alunos')
def listar_alunos():
    # Rota de Listagem. O template 'alunos.html' deve ter os botões.
    return render_template('alunos.html', alunos=alunos, titulo='Alunos')

# Rota para o formulário de adição (chama 'adicionar_aluno.html')
@app.route('/aluno/novo')
def novo_aluno():
    return render_template('adicionar_aluno.html', titulo='Adicionar Aluno')

# Rota para o formulário de edição (chama 'editar_aluno.html')
@app.route('/aluno/editar/<int:id>')
def editar_aluno(id):
    aluno = _buscar_por_id(alunos, id)
    if not aluno:
        flash("Aluno não encontrado para edição.", "danger")
        return redirect(url_for('listar_alunos'))
        
    # Envia o objeto 'aluno' preenchido para o template de edição
    return render_template('editar_aluno.html', titulo=f'Editar Aluno: {aluno["nome"]}', aluno=aluno)


# Rota Polimórfica: Salva (Insere OU Atualiza)
# Recebe a requisição POST de adicionar_aluno.html (sem ID) ou editar_aluno.html (com ID)
@app.route('/aluno/salvar', methods=['POST'])       
@app.route('/aluno/salvar/<int:id>', methods=['POST']) 
def salvar_aluno(id=None):
    nome = request.form.get('nome')
    
    try:
        idade = int(request.form.get('idade'))
    except ValueError:
        flash(f"Idade inválida para {nome}.", "danger")
        # Retorna ao formulário de edição/adição se houver erro de validação
        if id:
            return redirect(url_for('editar_aluno', id=id))
        else:
            return redirect(url_for('novo_aluno'))


    if id is None:
        # INSERÇÃO (veio de adicionar_aluno.html)
        global alunos
        novo_id = _proximo_id(alunos)
        alunos.append({"id": novo_id, "nome": nome, "idade": idade})
        flash(f"Aluno(a) '{nome}' adicionado(a) com sucesso!", "success")
    else:
        # ATUALIZAÇÃO (veio de editar_aluno.html)
        aluno = _buscar_por_id(alunos, id)
        if aluno:
            aluno['nome'] = nome
            aluno['idade'] = idade
            flash(f"Aluno(a) '{nome}' atualizado(a) com sucesso!", "success")
        else:
            flash("Erro ao atualizar: Aluno não encontrado.", "danger")

    return redirect(url_for('listar_alunos'))

# Rota para REMOVER Aluno
@app.route('/aluno/remover/<int:id>')
def remover_aluno(id):
    global alunos
    tamanho_original = len(alunos)
    aluno_removido = _buscar_por_id(alunos, id)
    
    # Remove o aluno da lista
    alunos = [a for a in alunos if str(a["id"]) != str(id)]

    if len(alunos) < tamanho_original and aluno_removido:
        flash(f"Aluno(a) '{aluno_removido['nome']}' removido(a) com sucesso!", "success")
    else:
        flash("Erro ao remover: Aluno não encontrado.", "danger")

    return redirect(url_for('listar_alunos'))


# ------------------------------------------------------------------
# --- ROTAS DE PROFESSORES (CRUD COMPLETO) ---
# ------------------------------------------------------------------

@app.route('/professores')
def listar_professores():
    return render_template('professores.html', professores=professores, titulo='Professores')

@app.route('/professor/novo')
def novo_professor():
    return render_template('adicionar_professor.html', titulo='Adicionar Professor')

@app.route('/professor/editar/<int:id>')
def editar_professor(id):
    professor = _buscar_por_id(professores, id)
    if not professor:
        flash("Professor não encontrado para edição.", "danger")
        return redirect(url_for('listar_professores'))
        
    return render_template('editar_professor.html', titulo=f'Editar Professor: {professor["nome"]}', professor=professor)

@app.route('/professor/salvar', methods=['POST'])       
@app.route('/professor/salvar/<int:id>', methods=['POST']) 
def salvar_professor(id=None):
    nome = request.form.get('nome')
    disciplina = request.form.get('disciplina')

    if id is None:
        global professores
        novo_id = _proximo_id(professores)
        professores.append({"id": novo_id, "nome": nome, "disciplina": disciplina})
        flash(f"Professor(a) '{nome}' adicionado(a) com sucesso!", "success")
    else:
        professor = _buscar_por_id(professores, id)
        if professor:
            professor['nome'] = nome
            professor['disciplina'] = disciplina
            flash(f"Professor(a) '{nome}' atualizado(a) com sucesso!", "success")
        else:
            flash("Erro ao atualizar: Professor não encontrado.", "danger")

    return redirect(url_for('listar_professores'))


@app.route('/professor/remover/<int:id>')
def remover_professor(id):
    global professores
    tamanho_original = len(professores)
    professor_removido = _buscar_por_id(professores, id)
    
    professores = [p for p in professores if str(p["id"]) != str(id)]

    if len(professores) < tamanho_original and professor_removido:
        flash(f"Professor(a) '{professor_removido['nome']}' removido(a) com sucesso!", "success")
    else:
        flash("Erro ao remover: Professor não encontrado.", "danger")

    return redirect(url_for('listar_professores'))


if __name__ == '__main__':
    app.run(debug=True)









