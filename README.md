# Cuaderno de Síntesis · Unidad 1 — Diseño de Circuitos

**Universidad Nacional de Loja** · Carrera de Computación · 2.º ciclo A · Grupo 8
**Estudiante:** Matías Joel Ortega Correa · **Docente:** Ing. Luis Darío Sinche Cueva
**Período:** septiembre 2026 – marzo 2027

> Unidad 1 — *Análisis de lógica combinacional con diseño clásico* (semanas 1 a 6).

🔗 **Ver el cuaderno:** `https://<tu-usuario>.github.io/<nombre-del-repo>/](https://matiasoc10.github.io/PortafolioDigitalDise-oCircuitos/`

## Contenido

| Semana | Tema | Circuito resuelto |
|---|---|---|
| 1 | Sistemas numéricos, códigos (BCD, Gray, ASCII) y compuertas | Conversiones, complemento a 2, tabla de las 7 compuertas |
| 2 | Álgebra de Boole y formas canónicas | Alarma de 3 sensores: canónica vs. simplificada |
| 3 | Mapas de Karnaugh, condiciones indiferentes, universalidad NAND/NOR | Función de 4 variables con *don't cares* solo con NAND |
| 4 | Semisumador, sumador completo, sumador paralelo, resta en C2, comparador | Sumador completo, sumador/restador de 4 bits |
| 5 | MUX, DEMUX, codificador, decodificador, display de 7 segmentos | Función con MUX 8:1 y 4:1, segmento *a* del BCD→7 seg |
| 6 | Consolidación | Procedimiento general, errores frecuentes, ejercicios de repaso |

Incluye también el **registro de dudas pendientes** y la **declaración de uso de IA**.

## Estructura del repositorio

```
├── index.html                 # El cuaderno (página de GitHub Pages)
├── img/                       # Esquemas y mapas de Karnaugh (SVG)
├── scripts/
│   └── generar_figuras.py     # Genera los SVG y verifica cada simplificación
├── .nojekyll
└── README.md
```

## Verificación

Cada expresión simplificada se comprueba por fuerza bruta contra su tabla de verdad:

```bash
pip install schemdraw pyparsing
python scripts/generar_figuras.py
# -> Todas las verificaciones pasaron.
```
