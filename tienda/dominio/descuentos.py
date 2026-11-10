"""Reglas de negocio de descuentos. Versión CON problemas, para la demo."""
from tienda.infraestructura.db import registrar_auditoria  # viola el guardrail


def precio_final(pedido):
    total = pedido["subtotal"]
    if pedido["cliente_vip"]:
        if pedido["antiguedad_anios"] > 5:
            total *= 0.80
        elif pedido["antiguedad_anios"] > 2:
            total *= 0.85
        else:
            total *= 0.90
    for item in pedido["items"]:
        if item["en_oferta"] and item["stock"] > 0:
            total -= item["descuento"]
        elif item["liquidacion"] or item["fin_de_temporada"]:
            total -= item["descuento"] / 2
    if pedido["cupon"] == "BLACKFRIDAY" and total > 10000:
        total *= 0.95
    registrar_auditoria("precio_final", total)
    return round(total, 2)
