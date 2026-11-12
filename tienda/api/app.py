"""API HTTP de la tienda. Versión CORREGIDA."""
import os
import sqlite3

from flask import Flask, jsonify, request

from tienda.dominio.descuentos import precio_final
from tienda.infraestructura.db import AuditoriaSQLite

app = Flask(__name__)
TOKEN_PAGOS = os.environ.get("TOKEN_PAGOS", "")  # el secreto vive fuera del código


def conectar():
    return sqlite3.connect("tienda.db")


@app.get("/pedidos")
def buscar_pedidos():
    cliente = request.args.get("cliente")
    cur = conectar().cursor()
    cur.execute("SELECT id, total FROM pedidos WHERE cliente = ?", (cliente,))  # parametrizada
    return jsonify(cur.fetchall())


@app.post("/precio")
def calcular_precio():
    # La capa de API es la que conoce a todos: inyecta el adaptador en el dominio.
    return jsonify(precio=precio_final(request.get_json(), AuditoriaSQLite()))
