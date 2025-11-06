from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
    
    return render_template('index.html')

@app.route('/relatorios')
def relatorios():
    
    return render_template('relatorios.html')

@app.route('/user')
def user():
    
    return render_template('usuarios.html')

@app.route('/config')
def config():
    
    return render_template('config.html')

@app.route('/sobre')
def sobre():
    
    
    return render_template('sobre_escola.html')




@app.route('/alunos')
def listar_alunos():
    return render_template('alunos.html', alunos=alunos)

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
    return render_template('adicionar_aluno.html')

@app.route('/editar_aluno/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = next((a for a in alunos if a["id"] == id), None)
    if not aluno:
        return "Aluno não encontrado", 404
    
    if request.method == 'POST':
        aluno['nome'] = request.form['nome']
        aluno['idade'] = int(request.form['idade'])
        return redirect(url_for('listar_alunos'))
        
    return render_template('editar_aluno.html', aluno=aluno)

@app.route('/excluir_aluno/<int:id>')
def excluir_aluno(id):
    global alunos
    
    alunos = [a for a in alunos if a["id"] != id]
    return redirect(url_for('listar_alunos'))



@app.route('/professores')
def listar_professores():
    return render_template('professores.html', professores=professores)

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
    return render_template('adicionar_professor.html')

@app.route('/editar_professor/<int:id>', methods=['GET', 'POST'])
def editar_professor(id):
    professor = next((p for p in professores if p["id"] == id), None)
    if not professor:
        return "Professor não encontrado", 404
    
    if request.method == 'POST':
        professor['nome'] = request.form['nome']
        professor['disciplina'] = request.form['disciplina']
        return redirect(url_for('listar_professores'))
        
    return render_template('editar_professor.html', professor=professor)

@app.route('/excluir_professor/<int:id>')
def excluir_professor(id):
    global professores
    professores = [p for p in professores if p["id"] != id]
    return redirect(url_for('listar_professores'))


if __name__ == '__main__':
    app.run(debug=True)








