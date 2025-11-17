from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Chave secreta é obrigatória para usar o flash (mensagens de notificação)
app.config['SECRET_KEY'] = 'chave_muito_secreta_e_forte_para_o_ifpi' 

# --- DADOS EM MEMÓRIA (SIMULANDO O BANCO DE DADOS) ---

alunos = [
    {"id": 1, "nome": "João Silva", "idade": 16},
    {"id": 2, "nome": "Sara Lima", "idade": 17}
]

professores = [
    {"id": 1, "nome": "Sr. Carlos", "disciplina": "Matemática"},
    {"id": 2, "nome": "Sra. Ana", "disciplina": "Português"},
    {"id": 3, "nome": "Pedro Oliveira", "disciplina": "Biologia"}
]

cursos = [
    {"id": 1, "nome_curso": "Informática"},
    {"id": 2, "nome_curso": "Administração"},
    {"id": 3, "nome_curso": "Enfermagem"},
    {"id": 4, "nome_curso": "Eletrotécnica"}
]

turmas = [
    {"id": 1, "semestre": "2024.1", "curso_id": 1, "professor_id": 1},
    {"id": 2, "semestre": "2024.1", "curso_id": 3, "professor_id": 3},
    {"id": 3, "semestre": "2024.2", "curso_id": 4, "professor_id": 1}
]


# --- FUNÇÕES AUXILIARES ---
def _proximo_id(lista):
    """Gera o próximo ID sequencial."""
    return max([item['id'] for item in lista]) + 1 if lista else 1

def _buscar_por_id(lista, id):
    """Busca um item na lista pelo ID."""
    return next((item for item in lista if str(item["id"]) == str(id)), None)


# ------------------------------------------------------------------
# --- ROTAS PRINCIPAIS DO MENU (ADAPTADAS AO SEU HTML) ---
# ------------------------------------------------------------------

@app.route('/')
def index():
    """Rota para a página inicial (index.html)."""
    return render_template('index.html', titulo='Dashboard')

@app.route('/relatorios')
def relatorios():
    """Rota para Relatórios (relatorios.html)."""
    return render_template('relatorios.html', titulo='Relatórios Gerenciais')

# ROTA ADAPTADA: SEU HTML usa href="/user"
@app.route('/user') 
def usuarios():
    """Rota para Usuários (usuarios.html)."""
    return render_template('usuarios.html', titulo='Gestão de Usuários')

# ROTA ADAPTADA: SEU HTML usa href="/config"
@app.route('/config') 
def configuracoes():
    """Rota para Configurações (config.html)."""
    return render_template('config.html', titulo='Configurações do Sistema')

@app.route('/sobre')
def sobre_escola():
    """Rota para Sobre a Escola (sobre_escola.html)."""
    return render_template('sobre_escola.html', titulo='Sobre a Escola')

# ROTA ADAPTADA: SEU HTML usa href="/saudacao1/Testando..."
@app.route('/saudacao1/<valor_recebido>')
def saudacoes(valor_recebido):
    """
    Rota para Saudações (saudacao/saudacao.html).
    Captura o valor 'Testando...' da URL.
    """
    return render_template('saudacao/saudacao.html', 
                           titulo='Saudações', 
                           valor_recebido=valor_recebido)
    
# ROTA ADAPTADA: SEU HTML usa href="/cadastro"
@app.route('/cadastro')
def desafio1():
    """Rota para Desafio 1 (desafio/cadastro.html)."""
    return render_template('desafio/cadastro.html', titulo='Desafio 1 - Cadastro')


# ------------------------------------------------------------------
# --- ROTAS DE ALUNOS (CRUD) ---
# ------------------------------------------------------------------
@app.route('/alunos')
def listar_alunos():
    """Exibe a lista de alunos (alunos.html)."""
    return render_template('alunos.html', alunos=alunos, titulo='Alunos')

@app.route('/aluno/novo')
def novo_aluno():
    """Exibe o formulário de adição de aluno (adicionar_aluno.html)."""
    return render_template('adicionar_aluno.html', titulo='Adicionar Aluno')

@app.route('/aluno/editar/<int:id>')
def editar_aluno(id):
    """Busca e exibe o formulário de edição de aluno (editar_aluno.html)."""
    aluno = _buscar_por_id(alunos, id)
    if not aluno:
        flash("Aluno não encontrado.", "danger")
        return redirect(url_for('listar_alunos'))
    return render_template('editar_aluno.html', titulo=f'Editar Aluno: {aluno["nome"]}', aluno=aluno)

@app.route('/aluno/salvar', methods=['POST'])       
@app.route('/aluno/salvar/<int:id>', methods=['POST']) 
def salvar_aluno(id=None):
    """Processa a inserção ou atualização de um aluno."""
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    
    if not nome or not idade:
        flash("Nome e Idade são obrigatórios.", "danger")
        return redirect(url_for('listar_alunos')) 

    try:
        idade = int(idade)
    except ValueError:
        flash("Idade deve ser um número válido.", "danger")
        return redirect(url_for('listar_alunos'))

    if id is None:
        # Inserção
        global alunos
        novo_id = _proximo_id(alunos)
        alunos.append({"id": novo_id, "nome": nome, "idade": idade})
        flash(f"Aluno(a) '{nome}' adicionado(a) com sucesso!", "success")
    else:
        # Atualização
        aluno = _buscar_por_id(alunos, id)
        if aluno:
            aluno['nome'] = nome
            aluno['idade'] = idade
            flash(f"Aluno(a) '{nome}' atualizado(a) com sucesso!", "success")
    return redirect(url_for('listar_alunos'))

@app.route('/aluno/remover/<int:id>')
def remover_aluno(id):
    """Remove um aluno pelo ID."""
    global alunos
    aluno_removido = _buscar_por_id(alunos, id)
    if aluno_removido:
        alunos = [a for a in alunos if str(a["id"]) != str(id)]
        flash(f"Aluno(a) '{aluno_removido['nome']}' removido(a) com sucesso!", "success")
    else:
        flash("Aluno não encontrado para remoção.", "danger")
    return redirect(url_for('listar_alunos'))


# ------------------------------------------------------------------
# --- ROTAS DE PROFESSORES (CRUD) ---
# ------------------------------------------------------------------
@app.route('/professores')
def listar_professores():
    """Exibe a lista de professores (professores.html)."""
    return render_template('professores.html', professores=professores, titulo='Professores')

@app.route('/professor/novo')
def novo_professor():
    """Exibe o formulário de adição de professor (adicionar_professor.html)."""
    return render_template('adicionar_professor.html', titulo='Adicionar Professor')

@app.route('/professor/editar/<int:id>')
def editar_professor(id):
    """Busca e exibe o formulário de edição de professor (editar_professor.html)."""
    professor = _buscar_por_id(professores, id)
    if not professor:
        flash("Professor não encontrado.", "danger")
        return redirect(url_for('listar_professores'))
    return render_template('editar_professor.html', titulo=f'Editar Professor: {professor["nome"]}', professor=professor)

@app.route('/professor/salvar', methods=['POST'])       
@app.route('/professor/salvar/<int:id>', methods=['POST']) 
def salvar_professor(id=None):
    """Processa a inserção ou atualização de um professor."""
    nome = request.form.get('nome')
    disciplina = request.form.get('disciplina')
    
    if not nome or not disciplina:
        flash("Nome e Disciplina são obrigatórios.", "danger")
        return redirect(url_for('listar_professores')) 

    if id is None:
        # Inserção
        global professores
        novo_id = _proximo_id(professores)
        professores.append({"id": novo_id, "nome": nome, "disciplina": disciplina})
        flash(f"Professor(a) '{nome}' adicionado(a) com sucesso!", "success")
    else:
        # Atualização
        professor = _buscar_por_id(professores, id)
        if professor:
            professor['nome'] = nome
            professor['disciplina'] = disciplina
            flash(f"Professor(a) '{nome}' atualizado(a) com sucesso!", "success")
        else:
            flash("Professor não encontrado para atualização.", "danger")
    return redirect(url_for('listar_professores'))

@app.route('/professor/remover/<int:id>')
def remover_professor(id):
    """Remove um professor pelo ID."""
    global professores
    professor_removido = _buscar_por_id(professores, id)
    if professor_removido:
        professores = [p for p in professores if str(p["id"]) != str(id)]
        flash(f"Professor(a) '{professor_removido['nome']}' removido(a) com sucesso!", "success")
    else:
        flash("Professor não encontrado para remoção.", "danger")
    return redirect(url_for('listar_professores'))


# ------------------------------------------------------------------
# --- ROTAS DE TURMAS (CRUD) ---
# ------------------------------------------------------------------
@app.route('/turmas')
def listar_turmas():
    """Exibe a lista de turmas (turmas.html) com detalhes de Curso e Professor."""
    lista_turmas_detalhada = []
    # Combina turmas, cursos e professores (Simulando JOIN)
    for turma in sorted(turmas, key=lambda t: t['id'], reverse=True):
        curso = _buscar_por_id(cursos, turma['curso_id'])
        professor = _buscar_por_id(professores, turma['professor_id'])
        
        lista_turmas_detalhada.append({
            "id": turma['id'],
            "semestre": turma['semestre'],
            # Obtém nomes de FKs
            "curso_nome": curso['nome_curso'] if curso else "Curso não encontrado",
            "professor_nome": professor['nome'] if professor else "Professor não encontrado",
            "professor_disciplina": professor['disciplina'] if professor else "N/A"
        })
        
    return render_template('turmas.html', 
                           turmas=lista_turmas_detalhada, 
                           titulo='Listagem de Turmas')

@app.route('/turma/novo')
def novo_turma():
    """Exibe o formulário de adição de turma (adicionar_turma.html) com listas de FKs."""
    return render_template('adicionar_turma.html', 
                           titulo='Adicionar Turma',
                           lista_cursos=cursos,
                           lista_professores=professores)

@app.route('/turma/editar/<int:id>')
def editar_turma(id):
    """Busca e exibe o formulário de edição de turma (editar_turma.html) com listas de FKs."""
    turma = _buscar_por_id(turmas, id)
    if not turma:
        flash("Turma não encontrada para edição.", "danger")
        return redirect(url_for('listar_turmas'))
        
    return render_template('editar_turma.html', 
                           titulo=f'Editar Turma: {turma["semestre"]}', 
                           turma=turma,
                           lista_cursos=cursos,
                           lista_professores=professores)

@app.route('/turma/salvar', methods=['POST'])       
@app.route('/turma/salvar/<int:id>', methods=['POST']) 
def salvar_turma(id=None):
    """Processa a inserção ou atualização de uma turma."""
    semestre = request.form.get('semestre')
    
    try:
        curso_id = int(request.form.get('curso_id'))
        professor_id = int(request.form.get('professor_id'))
    except (ValueError, TypeError):
        flash("Erro: Seleção de curso ou professor inválida.", "danger")
        return redirect(url_for('listar_turmas'))

    if id is None:
        # Inserção
        global turmas
        novo_id = _proximo_id(turmas)
        turmas.append({
            "id": novo_id, 
            "semestre": semestre, 
            "curso_id": curso_id, 
            "professor_id": professor_id
        })
        flash(f"Turma do semestre '{semestre}' adicionada com sucesso!", "success")
    else:
        # Atualização
        turma = _buscar_por_id(turmas, id)
        if turma:
            turma['semestre'] = semestre
            turma['curso_id'] = curso_id
            turma['professor_id'] = professor_id
            flash(f"Turma do semestre '{semestre}' atualizada com sucesso!", "success")
        else:
            flash("Erro ao atualizar: Turma não encontrada.", "danger")

    return redirect(url_for('listar_turmas'))

@app.route('/turma/remover/<int:id>')
def remover_turma(id):
    """Remove uma turma pelo ID."""
    global turmas
    tamanho_original = len(turmas)
    turma_removida = _buscar_por_id(turmas, id)
    
    turmas = [t for t in turmas if str(t["id"]) != str(id)]

    if len(turmas) < tamanho_original and turma_removida:
        flash(f"Turma do semestre '{turma_removida['semestre']}' removida com sucesso!", "success")
    else:
        flash("Erro ao remover: Turma não encontrada.", "danger")

    return redirect(url_for('listar_turmas'))


# --- ROTA PRINCIPAL DE EXECUÇÃO ---
if __name__ == '__main__':
    app.run(debug=True)










