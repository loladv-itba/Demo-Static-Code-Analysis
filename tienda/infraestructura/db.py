"""Adaptador de persistencia (capa de infraestructura)."""
import sqlite3

BASE = "tienda.db"


def registrar_auditoria(evento, valor):
    with sqlite3.connect(BASE) as con:
        con.execute("CREATE TABLE IF NOT EXISTS auditoria (evento TEXT, valor REAL)")
        con.execute("INSERT INTO auditoria (evento, valor) VALUES (?, ?)", (evento, valor))


class AuditoriaSQLite:
    """Implementa el puerto Auditoria que define el dominio."""

    def registrar(self, evento: str, valor: float) -> None:
        registrar_auditoria(evento, valor)
