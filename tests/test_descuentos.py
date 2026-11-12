"""Tests de la versión CON problemas: pasan aunque el análisis estático falle."""
import pytest

from tienda.infraestructura import db


@pytest.fixture(autouse=True)
def base_temporal(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "BASE", str(tmp_path / "test.db"))


from tienda.dominio.descuentos import precio_final  # noqa: E402


def pedido(subtotal=1000, vip=False, antiguedad=0, items=(), cupon=""):
    return {"subtotal": subtotal, "cliente_vip": vip, "antiguedad_anios": antiguedad,
            "items": list(items), "cupon": cupon}


def test_vip_con_mas_de_cinco_anios_tiene_20_por_ciento():
    assert precio_final(pedido(vip=True, antiguedad=6)) == 800.0


def test_item_en_liquidacion_descuenta_la_mitad():
    item = {"descuento": 100, "en_oferta": False, "stock": 1,
            "liquidacion": True, "fin_de_temporada": False}
    assert precio_final(pedido(items=[item])) == 950.0


def test_blackfriday_solo_aplica_sobre_10000():
    assert precio_final(pedido(subtotal=20000, cupon="BLACKFRIDAY")) == 19000.0
    assert precio_final(pedido(subtotal=5000, cupon="BLACKFRIDAY")) == 5000.0
