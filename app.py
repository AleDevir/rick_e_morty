'''
API Flask Rick & Morty
'''

import os
from typing import Any
from flask import Flask, render_template, send_from_directory, abort, redirect
import requests
from werkzeug.exceptions import HTTPException
# import json

app = Flask(__name__)

@app.route('/api/<path:url>')
def get_json_data_for(url: str) -> dict[str, Any]:
    '''
    Retorna os dados da URL informada.
    '''
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        abort(response.status_code)
    data = response.json()
    return data


@app.route('/favicon.ico')
def favicon():
    '''
    favicon:
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


@app.route('/episodios')
def episodios_sem_pagina():
    '''
    Episódios
    '''
    return redirect('/episodios/1')


@app.route('/episodios/<int:page>')
def episodios(page: int):
    '''
    Episódios
    '''
    data = get_json_data_for(f"https://rickandmortyapi.com/api/episode?page={page}")
    return render_template('episodios.html', dados=data, page=page)

@app.route('/personagens_do_episodio/<int:idt>')
def personagens_do_episodio(idt: int):
    '''
    Episódio de identificador informado.
    '''
    data = get_json_data_for(f"https://rickandmortyapi.com/api/episode/{idt}")
    data['characters_ids'] = [
        c.split('/')[-1] for c in data['characters']
    ]
    return render_template('episodio.html', dados=data)

@app.route('/localizacoes')
def localizacoes_sem_pagina():
    '''
    Localizações
    '''
    return redirect('/localizacoes/1')


@app.route('/localizacoes/<int:page>')
def localizacoes(page: int):
    '''
    Localizações
    '''
    data = get_json_data_for(f"https://rickandmortyapi.com/api/location?page={page}")
    return render_template('localizacoes.html', dados=data, page=page)


@app.route('/localizacao/<int:idt>')
def residentes_da_localizacao(idt: int):
    '''
    Localização de identificador informado.
    '''
    data = get_json_data_for(f"https://rickandmortyapi.com/api/location/{idt}")
    data['characters_ids'] = [
        c.split('/')[-1] for c in data['residents']
    ]
    return render_template('localizacao.html', dados=data)


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
    data = get_json_data_for(f"https://rickandmortyapi.com/api/character?page={page}")
    return render_template('personagens.html', dados=data, page=page)


@app.route('/personagem/<int:idt>')
def personagem(idt: int):
    '''
    Personagem
    '''
    data = get_json_data_for(f"https://rickandmortyapi.com/api/character/{idt}")
    return render_template('personagem.html', dados=data)


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
    print(f"type(e)={type(e)} ERRO:{str(e)}")
    return render_template('erro.html', error={
        'code': '44',
        'msg': 'Página não encontrada!',
    }), 404

@app.errorhandler(500)
def page_page_error(e):
    '''
    Erro inesperado
    status code = 500
    '''
    print(f"type(e)={type(e)} ERRO:{str(e)}")
    return render_template('erro.html', error={
        'code': '50',
        'msg': 'Ops! Ocorreu um erro inesperado.',
    }), 500


@app.errorhandler(Exception)
def handle_exception(exception: Exception):
    '''
    Captura as exceções
    https://flask.palletsprojects.com/en/2.3.x/errorhandling/
    '''
    if isinstance(exception, HTTPException):
        return exception
    return render_template('erro.html', error={
        'code': '50',
        'msg': 'Ops! Ocorreu um erro inesperado.',
    }), 500


if __name__ == "__main__":
    app.run(debug=True, port=6969)
