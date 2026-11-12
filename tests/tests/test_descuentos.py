"""El refactor tiene que preservar el comportamiento: los tests lo verifican."""
from tienda.dominio.descuentos import precio_final


class AuditoriaFalsa:
    def __init__(self):
        self.eventos = []

    def registrar(self, evento, valor):
        self.eventos.append((evento, valor))


def item(descuento=100, en_oferta=False, stock=1, liquidacion=False, fin_de_temporada=False):
    return {
        "descuento": descuento,
        "en_oferta": en_oferta,
        "stock": stock,
        "liquidacion": liquidacion,
        "fin_de_temporada": fin_de_temporada,
    }


def pedido(subtotal=1000, vip=False, antiguedad=0, items=(), cupon=""):
    return {
        "subtotal": subtotal,
        "cliente_vip": vip,
        "antiguedad_anios": antiguedad,
        "items": list(items),
        "cupon": cupon,
    }


def test_vip_con_mas_de_cinco_anios_tiene_20_por_ciento():
    assert precio_final(pedido(vip=True, antiguedad=6), AuditoriaFalsa()) == 800.0


def test_item_en_liquidacion_descuenta_la_mitad():
    p = pedido(items=[item(descuento=100, liquidacion=True)])
    assert precio_final(p, AuditoriaFalsa()) == 950.0


def test_blackfriday_solo_aplica_sobre_10000():
    assert precio_final(pedido(subtotal=20000, cupon="BLACKFRIDAY"), AuditoriaFalsa()) == 19000.0
    assert precio_final(pedido(subtotal=5000, cupon="BLACKFRIDAY"), AuditoriaFalsa()) == 5000.0


def test_registra_el_evento_en_la_auditoria():
    auditoria = AuditoriaFalsa()
    precio_final(pedido(), auditoria)
    assert auditoria.eventos == [("precio_final", 1000)]
