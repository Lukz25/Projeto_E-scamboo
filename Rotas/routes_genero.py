from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Genero

bp_genero = Blueprint("/genero/", "__name__", url_prefix= "/genero")


