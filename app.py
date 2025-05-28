from flask import Flask, request, jsonify, send_from_directory
import random
import math
import os
from collections import deque

app = Flask(__name__, static_folder='static')

# Coordenadas fijas para las ciudades
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def tabu_search(ruta_inicial, coord, temperatura, minima, velocidad):
    mejor_ruta = ruta_inicial[:]
    mejor_distancia = evalua_ruta(mejor_ruta, coord)

    actual = ruta_inicial[:]
    actual_distancia = mejor_distancia

    # tamaño de la lista tabú depende de "velocidad"
    lista_tabu = deque(maxlen=velocidad)

    iteraciones = int((temperatura - minima) / 0.1)
    for _ in range(iteraciones):
        vecinos = []
        for i in range(len(actual)):
            for j in range(i + 1, len(actual)):
                vecino = actual[:]
                vecino[i], vecino[j] = vecino[j], vecino[i]
                if vecino not in lista_tabu:
                    vecinos.append((vecino, evalua_ruta(vecino, coord)))

        if not vecinos:
            break

        vecino, dist = min(vecinos, key=lambda x: x[1])
        lista_tabu.append(vecino)

        actual = vecino[:]
        actual_distancia = dist

        if actual_distancia < mejor_distancia:
            mejor_ruta = actual[:]
            mejor_distancia = actual_distancia

    return mejor_ruta, mejor_distancia

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/optimizar", methods=["POST"])
def optimizar():
    data = request.get_json()
    print("Datos recibidos:", data)

    try:
        temperatura = float(data["temperatura"])
        minima = float(data["minima"])
        velocidad = int(data["velocidad"])
    except (KeyError, ValueError) as e:
        return jsonify({"error": "Datos inválidos", "detalle": str(e)}), 400

    ciudades = list(coord.keys())
    random.shuffle(ciudades)

    ruta_opt, dist_total = tabu_search(ciudades, coord, temperatura, minima, velocidad)

    return jsonify({
        "ruta": ruta_opt,
        "distancia": round(dist_total, 2)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
