from flask import Flask, make_response, jsonify, request
from model import tierOneModel

app = Flask(__name__)
advisor = tierOneModel()

@app.route('/', methods=['POST'])
def main():
    context = request.json['context']
    answer = advisor.get_answer('What should I wear today?', context)
    return jsonify({'answer': answer})


app.run(debug=True, host="0.0.0.0", port="8081")