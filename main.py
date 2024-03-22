from flask import Flask, render_template, request
import json

from model.usuario import Usuario

def verificar_usuario(objUser, tipo):
    # se caso desejo fazer só a verificação do email
    if (tipo == "cad"):
        with open('usuarios.json', 'r') as arquivo:
            for linha in arquivo:
                usuario = json.loads(linha)
                if usuario['email'] == objUser.email:
                    return True
        return False
    # verifica o usuário completamente
    else:
        with open('usuarios.json', 'r') as arquivo:
            for linha in arquivo:
                usuario = json.loads(linha)
                if (usuario['email'] == objUser.email) and (objUser.descriptografar(usuario['senha']['senha_cripto'], usuario['senha']['chave']) == objUser.senha):
                    return True
        return False


app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html", mensagem_erro='')

@app.route("/cadastro")
def cadastro():
    return render_template("cadastrar.html", mensagem_erro='')


@app.route("/logar", methods=['POST'])
def logar():
    objUser = Usuario("", request.form['email'], request.form['senha'])

    if verificar_usuario(objUser, "login"):
        return "Usuário Cadastrado!"
    else:
        return render_template("login.html", mensagem_erro="Usuário não cadastrado!")

@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    objUser = Usuario(request.form['nome'], request.form['email'], request.form['senha'])

    #verifica se o usuário já está cadastrado
    if verificar_usuario(objUser, "cad"):
        return render_template('cadastrar.html', mensagem_erro='Este e-mail já está cadastrado.')
    else:
        #caso o usuário não esteja cadastrado
        with open('usuarios.json', 'a') as arquivo:
            usuario = {
                "nome": objUser.nome,
                "email": objUser.email,
                "senha": objUser.criptografar(objUser.senha)

            }
            json.dump(usuario, arquivo)
            arquivo.write('\n')

        return render_template('login.html')


#roda automaticamente o site após uma alteração
if __name__ == "__main__":
    app.run(debug=True)