from flask import Blueprint, request, jsonify
from classes import Genero

bp_genero = Blueprint("/genero/", "__name__", url_prefix= "/genero")


