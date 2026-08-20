from flask import Flask
app = Flask(__name__)

@app.route('/qwerty123')
def webhook():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
