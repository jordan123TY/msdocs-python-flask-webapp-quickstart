import os
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_oidc import OpenIDConnect

app = Flask(__name__)
# Configurez ces valeurs avec celles de votre application Azure B2C
app.config['B2C_TENANT'] = "ab39bc97-fa3e-44e9-a2c6-e0f1aa8183f7"
app.config['B2C_CLIENT_ID'] = "3c0393e1-d9ea-4d48-84b7-a1f4c3f5c98c"
app.config['B2C_CLIENT_SECRET'] = "x9E8Q~3c7z12nfit7JCs4w5VI7D7uZmVB_Db_a17"
app.config['B2C_REDIRECT_URI'] = "https://application-test-bluink.azurewebsites.net"  # Changez pour votre URL de production
app.config['B2C_AUTHORITY'] = "https://application-test-bluink.azurewebsites.net"
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
