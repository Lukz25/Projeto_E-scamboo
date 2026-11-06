from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Titulo

bp_titulo = Blueprint("/titulo/", "__name__", url_prefix= "/titulo")


