from flask import Flask, request, jsonify, render_template
import os
import qianfan

app = Flask(__name__)

# 设置环境变量
os.environ["QIANFAN_ACCESS_KEY"] = ""
os.environ["QIANFAN_SECRET_KEY"] = ""

chat_comp = qianfan.ChatCompletion()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # 调用 qianfan API
    resp = chat_comp.do(model="ERNIE-3.5-8K", messages=[{
        "role": "user",
        "content": user_message
    }])
    
    return jsonify({"result": resp["body"]["result"]})

if __name__ == '__main__':
    app.run(debug=True)