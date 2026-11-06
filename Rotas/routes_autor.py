from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Autor

bp_autor = Blueprint("/autor/", "__name__", url_prefix= "/autor")


