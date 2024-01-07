from flask import Flask, render_template, request, jsonify
from publicador import RabbitmqPublisher

app = Flask(__name__)
mensagens_recebidas = []

@app.route('/')
def index():
    return render_template('index.html', mensagens=mensagens_recebidas)

@app.route('/publicar', methods=['POST'])
def publicar():
    data = request.get_json()
    message = data.get('message', '')
    
    if message:
        mensagens_recebidas.append(message)
        publisher = RabbitmqPublisher()
        publisher.send_message({"mensagem": message})
        
        return jsonify({"status": "success", "message": "Mensagem enviada com sucesso!"})
    else:
        return jsonify({"status": "error", "message": "Mensagem vazia!"})

if __name__ == '__main__':
    app.run(debug=True)
