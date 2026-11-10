# Demo: análisis estático como quality gate

Prueba de concepto para la presentación de *Static Code Analysis* (Ingeniería de Software II).
Una mini API de una tienda, en Python, con tres capas (`api`, `dominio`, `infraestructura`)
y problemas plantados a propósito. Dos herramientas los detectan sin ejecutar el código:

| Herramienta | Qué encuentra en esta demo | Atributo de calidad |
| --- | --- | --- |
| Ruff | Import sin usar, secreto hardcodeado (S105), SQL armado con texto (S608), complejidad 8 > 6 (C901) | Maintainability, Security, Testability |
| Semgrep con reglas propias | Inyección SQL por *taint* (dato del usuario hasta `execute`, CWE-89) y violación del guardrail hexagonal | Security, Conceptual Integrity |

## Requisitos

- Python 3.11 o superior.
- `pip install ruff==0.16.9 semgrep==1.184.0` (las versiones con las que se probó).
- En Windows, si `pip install semgrep` da problemas, usar WSL u Opengrep (el fork libre, mismas reglas).

## Correrlo en la compu

```bash
ruff check .                                   # 4 hallazgos, en milisegundos
semgrep scan --config reglas/ --error --metrics=off   # 2 hallazgos bloqueantes, en segundos
```

Ambos comandos terminan con código de salida 1: eso es lo que hace fallar el pipeline.

## Armarlo en GitHub (antes de la presentación)

1. Crear un repositorio y subir esta carpeta tal cual a la rama `main`.
2. En *Settings → Branches*, proteger `main` y exigir el check `quality-gate` antes de mergear.
3. Crear una rama `feature/buscar-pedidos`, tocar cualquier archivo y abrir un pull request:
   el check queda en rojo y el botón de merge, bloqueado.
4. Grabar la pantalla del PR en rojo y en verde como respaldo por si falla internet en vivo.

## Aplicar la corrección

Copiar los archivos de `_solucion/` sobre el proyecto:

```bash
cp -r _solucion/tienda/. tienda/
cp -r _solucion/tests/. tests/
ruff check . && semgrep scan --config reglas/ --error --metrics=off   # todo en verde
python -m pytest -q tests                                            # 4 tests pasan
```

Qué cambia:

- **Inyección SQL:** la consulta pasa a ser parametrizada (`... WHERE cliente = ?`, `(cliente,)`).
- **Secreto:** el token se lee de una variable de entorno.
- **Guardrail hexagonal:** el dominio declara un puerto `Auditoria` (un `Protocol`) y la API inyecta
  el adaptador `AuditoriaSQLite`. El dominio deja de importar infraestructura.
- **Complejidad:** `precio_final` se parte en funciones chicas. Los tests de `_solucion/tests`
  verifican que el comportamiento no cambió (también se comparó contra la versión original
  con 20.000 pedidos aleatorios).

## Guion de la demo (5 minutos)

| Minuto | Qué se muestra | Qué se dice |
| --- | --- | --- |
| 0:00–0:45 | Las tres carpetas y los dos YAML de `reglas/` | "Estas reglas son guardrails escritos como código." |
| 0:45–1:45 | `ruff check .` | Cuatro problemas en milisegundos, sin ejecutar nada. |
| 1:45–3:00 | `semgrep scan --config reglas/ --error` | Fuente (`request.args`) y sumidero (`execute`); el dominio importando infraestructura. |
| 3:00–4:15 | El pull request en GitHub con el check rojo | El merge está bloqueado: el prompt sugiere, el gate exige. |
| 4:15–5:00 | La corrección y el check verde | Qué atributo protegió cada regla y cuánto tardó. |
