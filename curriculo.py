from flask import Flask, render_template, request, redirect, url_for, send_file, Blueprint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy

# Criação da instância do Flask
app2 = Flask(__name__)

# Criação do Blueprint
blueprint2 = Blueprint('app2', __name__)

# Configurando o banco de dados SQLite
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///curriculo.db'
db = SQLAlchemy(app2)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    data_nascimento = db.Column(db.String(20))
    objetivo = db.Column(db.Text)
    formacao = db.Column(db.Text)
    experiencia = db.Column(db.Text)
    outras_informacoes = db.Column(db.Text)
    filename = db.Column(db.String(200))

# Function to create the database tables
def create_tables():
    with app2.app_context():
        db.create_all()

def calculate_section_height(c, text, font_size, max_width):
    # Calculate the height required for the given text to fit within the max_width
    text_object = c.beginText(0, 0)
    text_object.setFont("Helvetica", font_size)
    lines = text.splitlines()
    for line in lines:
        text_object.textLine(line)
    _, text_ascent = text_object.getAscent()
    line_height = text_ascent + 2  # Adding 2 for spacing between lines
    total_height = len(lines) * line_height
    num_pages = total_height / letter[1]
    if num_pages > 1:
        total_height = len(lines) * line_height * num_pages
    return total_height

def generate_resume_pdf(nome, email, telefone, endereco, data_nascimento, objetivo, formacao, experiencia,
                        outras_informacoes):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    # Titulo - Nome
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 100, nome)

    # Informações de Contato
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 130, f"Contatos: {email} / {telefone}")
    c.drawString(50, height - 150, f"Endereço: {endereco}")
    c.drawString(50, height - 170, f"Data de nascimento: {data_nascimento}")

    # Objetivo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 220, "OBJETIVO")
    c.setFont("Helvetica", 12)
    texto_objetivo = c.beginText(50, height - 240)
    for line in objetivo.splitlines():
        texto_objetivo.textLine(line)
    c.drawText(texto_objetivo)

    # Formação
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 330, "FORMAÇÃO")
    c.setFont("Helvetica", 12)
    texto_formacao = c.beginText(50, height - 350)
    for line in formacao.splitlines():
        texto_formacao.textLine(line)
    c.drawText(texto_formacao)

    # Experiências de Trabalho
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 460, "EXPERIÊNCIAS DE TRABALHO")
    c.setFont("Helvetica", 12)
    texto_experiencia = c.beginText(50, height - 480)
    for line in experiencia.splitlines():
        texto_experiencia.textLine(line)
    c.drawText(texto_experiencia)

    # Outras Informações
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 560, "OUTRAS INFORMAÇÕES")
    c.setFont("Helvetica", 12)
    texto_outras_informacoes = c.beginText(50, height - 580)
    for line in outras_informacoes.splitlines():
        texto_outras_informacoes.textLine(line)
    c.drawText(texto_outras_informacoes)

    c.save()

    filename = f"{nome.replace(' ', '_')}_curriculo.pdf"

    with open(os.path.join(app2.root_path, 'static', filename), 'wb') as f:
        f.write(buffer.getvalue())

    buffer.close()
    return filename


@app2.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        data_nascimento = request.form['data_nascimento']
        objetivo = request.form['objetivo']
        formacao = request.form['formacao']
        experiencia = request.form['experiencia']
        outras_informacoes = request.form['outras_informacoes']

        filename = generate_resume_pdf(nome, email, telefone, endereco, data_nascimento, objetivo, formacao,
                                       experiencia,
                                       outras_informacoes)

        resume = Resume(nome=nome, email=email, telefone=telefone, endereco=endereco, data_nascimento=data_nascimento,
                        objetivo=objetivo, formacao=formacao, experiencia=experiencia,
                        outras_informacoes=outras_informacoes,
                        filename=filename)

        db.session.add(resume)
        db.session.commit()

        return redirect(url_for('resume', filename=filename))

    return render_template('form.html')


@app2.route('/resume/<filename>')
def resume(filename):
    static_folder = os.path.join(app2.root_path, 'static')
    pdf_path = os.path.join(static_folder, filename)

    if os.path.isfile(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return "File not found."


if __name__ == '__main__':
    create_tables()
    app2.run(port=5000, debug=True)
