'''
API Flask Rick & Morty

Documentação:
https://rickandmortyapi.com/documentation/#rest

https://rickandmortyapi.com/api/character

https://rickandmortyapi.com/api/location

https://rickandmortyapi.com/api/episode


Para executar a aplicação:
$ python app.py

Documentação
Favicon: https://flask.palletsprojects.com/en/2.3.x/patterns/favicon/

Development Server:
https://flask-fr.readthedocs.io/server/


Custom Error Pages:
https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/


Handling Application Errors
https://flask.palletsprojects.com/en/2.3.x/errorhandling/

Quickstart
https://flask.palletsprojects.com/en/1.1.x/quickstart/
'''

import os
from typing import Any
from flask import Flask, render_template, send_from_directory, abort, redirect
import requests
from werkzeug.exceptions import HTTPException
import json

app = Flask(__name__)

@app.route('/api/<path:url>')
def get_json_data_for(url: str) -> dict[str, Any]:
    '''
    Retorna os dados da URL informada.
    https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules
    '''
    uri = f"https://{url}"
    response = requests.get(uri)
    if response.status_code != 200:
        abort(response.status_code)
    data = response.json()
    # print('...................................')
    # print(json.dumps(data, indent=4))
    # print('...................................')
    return data


@app.route('/favicon.ico')
def favicon():
    '''
    favicon:
    https://flask.palletsprojects.com/en/2.3.x/patterns/favicon/
    '''
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

@app.route('/')
def home():
    '''
    Página principal
    '''
    return render_template('home.html')

@app.route('/personagens')
def personagens_sem_pagina():
    '''
    Personagens
    '''
    return redirect('/personagens/1')


@app.route('/personagens/<int:page>')
def personagens(page: int):
    '''
    Personagens
    '''
    data = get_json_data_for(f"rickandmortyapi.com/api/character?page={page}")
    return render_template('personagens.html', personagens_page=data, page=page)

#####################################################
####           TRATAMENTO  DE  ERROS             ####
#####################################################

@app.errorhandler(404)
def page_not_found(e):
    '''
    Página não encontrada
    status code = 404
    https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
    '''
    print(str(e))
    print(type(e))
    return render_template('erro.html', msg='Página não encontrada!'), 404


@app.errorhandler(500)
def page_not_found(e):
    '''
    Erro inesperado
    status code = 500
    '''
    print(str(e))
    return render_template('erro.html', msg='Ops! Ocorreu um erro inesperado.'), 500


@app.errorhandler(Exception)
def handle_exception(exception: Exception):
    '''
    Captura as exceções
    https://flask.palletsprojects.com/en/2.3.x/errorhandling/
    '''
    print('1111111111111111111')
    if isinstance(exception, HTTPException):
        return exception
    print('22222222222222222')
    return render_template("erro.html", msg=str(exception)), 500


if __name__ == "__main__":
    app.run(debug=True, port=8888)
