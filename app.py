from flask import Flask

#Isso não passa de um main que pode ser alterado
#e pode ser usado como um exemplo de como funciona
#uma função em flask, LEIA O TXT CHAMADO 'LEIA_ISSO.txt'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
