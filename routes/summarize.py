from flask import Flask, render_template, jsonify
from routes.summarize import summarize_routes

app = Flask(__name__)
app.register_blueprint(summarize_routes)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
