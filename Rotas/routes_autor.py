from flask import Blueprint, request, jsonify
from classes import Autor

bp_autor = Blueprint("/autor/", "__name__", url_prefix= "/autor")


