from flask import Blueprint, request, jsonify
from classes import Proposta

bp_proposta = Blueprint("/proposta/", "__name__", url_prefix= "/proposta")


