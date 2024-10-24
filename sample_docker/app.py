from flask import Flask, jsonify

app = Flask(__name__)

# 기본 경로에 대한 응답
@app.route('/')
def home():
    return "Hello, Flask!"

# 헬스체크 엔드포인트
@app.route('/health')
def health():
    return jsonify(status="healthy"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)