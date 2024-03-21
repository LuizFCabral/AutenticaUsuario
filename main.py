from flask import Flask, render_template, request
import json
from cryptography.fernet import Fernet

app = Flask(__name__)

#funções para lidar com o usuário


#criptografia da senha


def criptografar(senha):
    chave_cripto = Fernet.generate_key()
    fernet = Fernet(chave_cripto)
    return {"senha_cripto": fernet.encrypt(senha.encode()).decode(), "chave": chave_cripto.decode()}

def descriptografar(senha, chave):
    fernet = Fernet(chave)
    return fernet.decrypt(senha.encode()).decode()

def verificar_usuario(email, senha):
    #se caso desejo fazer só a verificação do email
    if(senha==""):
        with open('usuarios.json', 'r') as arquivo:
            for linha in arquivo:
                usuario = json.loads(linha)
                if usuario['email'] == email:
                    return True
        return False
    #verifica o usuário completamente
    else:
        with open('usuarios.json', 'r') as arquivo:
            for linha in arquivo:
                usuario = json.loads(linha)
                if (usuario['email'] == email) and (descriptografar(usuario['senha']['senha_cripto'], usuario['senha']['chave']) == senha):
                    return True
        return False

#---------------------------------------------------------------------------------

@app.route("/")
def login():
    return render_template("login.html", mensagem_erro='')

@app.route("/cadastro")
def cadastro():
    return render_template("cadastrar.html", mensagem_erro='')


@app.route("/logar", methods=['POST'])
def logar():
    email = request.form['email']
    senha = request.form['senha']

    if verificar_usuario(email, senha):
        return "Usuário Cadastrado!"
    else:
        return render_template("login.html", mensagem_erro="Usuário não cadastrado!")

@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    #verifica se o usuário já está cadastrado
    if verificar_usuario(email, ""):
        return render_template('cadastrar.html', mensagem_erro='Este e-mail já está cadastrado.')
    else:
        #caso o usuário não esteja cadastrado
        usuario = {
            "nome": nome,
            "email": email,
            "senha": criptografar(senha)

        }

        with open('usuarios.json', 'a') as arquivo:
            json.dump(usuario, arquivo)
            arquivo.write('\n')

        return render_template('login.html')


#roda automaticamente o site após uma alteração
if __name__ == "__main__":
    app.run(debug=True)