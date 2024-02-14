import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'  # Chemin vers le fichier de configuration client OIDC
app.config['OIDC_ID_TOKEN_COOKIE_SECURE'] = False  # Permettre l'utilisation de cookies pour les tokens sur HTTP
oidc = OpenIDConnect(app)

@app.route('/')
@oidc.require_login
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
@oidc.require_login
def hello():
    name = request.form.get('name')
    if name:
        return render_template('hello.html', name=name)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
