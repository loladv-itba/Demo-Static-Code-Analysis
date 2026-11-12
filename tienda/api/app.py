"""API HTTP de la tienda. Versión CON problemas, para la demo."""
import os
import sqlite3

from flask import Flask, jsonify, request
#muchos muchos cambios, mucho muy importantes.
from tienda.dominio.descuentos import precio_final

app = Flask(__name__)
TOKEN_PAGOS = "demo-token-pagos-hardcodeado-123"  # secreto hardcodeado


def conectar():
    return sqlite3.connect("tienda.db")


@app.get("/pedidos")
def buscar_pedidos():
    cliente = request.args.get("cliente")  # FUENTE: dato controlado por el usuario
    sql = f"SELECT id, total FROM pedidos WHERE cliente = '{cliente}'"
    cur = conectar().cursor()
    cur.execute(sql)  # SUMIDERO: inyección SQL (CWE-89)
    return jsonify(cur.fetchall())


@app.post("/precio")
def calcular_precio():
    return jsonify(precio=precio_final(request.get_json()))
