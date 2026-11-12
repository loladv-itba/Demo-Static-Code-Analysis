"""Reglas de negocio de descuentos. Versión CORREGIDA: dominio puro."""
from typing import Protocol


class Auditoria(Protocol):
    """Puerto: el dominio declara qué necesita; la infraestructura lo implementa."""

    def registrar(self, evento: str, valor: float) -> None: ...


def _factor_vip(antiguedad_anios: int) -> float:
    if antiguedad_anios > 5:
        return 0.80
    if antiguedad_anios > 2:
        return 0.85
    return 0.90


def _descuento_item(item: dict) -> float:
    if item["en_oferta"] and item["stock"] > 0:
        return item["descuento"]
    if item["liquidacion"] or item["fin_de_temporada"]:
        return item["descuento"] / 2
    return 0.0


def precio_final(pedido: dict, auditoria: Auditoria) -> float:
    total = pedido["subtotal"]
    if pedido["cliente_vip"]:
        total *= _factor_vip(pedido["antiguedad_anios"])
    for item in pedido["items"]:
        total -= _descuento_item(item)
    if pedido["cupon"] == "BLACKFRIDAY" and total > 10000:
        total *= 0.95
    auditoria.registrar("precio_final", total)
    return round(total, 2)
