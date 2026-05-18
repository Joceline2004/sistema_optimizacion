#########################################################################################
#PROYECTO: IntelRR - Sistema de Optimización de Rutas Híbrido (GA + SA)
#Proyecto Final - Algoritmos Metaheurísticos
#AUTOR:Joceline Noemi De La Torre Segura
#DESCRIPCIÓN: Implementación de un algoritmo híbrido que combina Algoritmos Genéticos (GA) 
 #on Recocido Simulado (SA) para resolver el problema del viajante (TSP).
#########################################################################################
import random
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import time
from folium.plugins import AntPath
# --- CONFIGURACIÓN Y GENERACIÓN DE ESCENARIO ---
def generar_escenario_aleatorio(n):
    nuevas_ciudades = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in range(n)}
    nuevos_nombres = {i: f"ciudad_{i}" for i in range(n)}
    return nuevas_ciudades, nuevos_nombres

num_ciudades = 15 
ciudades, nombres_ciudades = generar_escenario_aleatorio(num_ciudades)
def distancia(ciudad1, ciudad2):
    x1, y1 = ciudades[ciudad1]
    x2, y2 = ciudades[ciudad2]
    return math.sqrt((x2-x1)**2 + (y2 - y1)**2)
# --- FUNCIÓN OBJETIVO (FITNESS) ---
def fitness(ruta):
    distancia_total = 0
    tiempo_total = 0
    costo_total = 0
    
    for i in range(len(ruta) - 1):
        d = distancia(ruta[i], ruta[i+1])
        distancia_total += d
        tiempo_total += d
        costo_total += d * 0.8

    fitness_total = (
        0.4 * distancia_total +
        0.3 * tiempo_total +
        0.3 * costo_total
    )
    return fitness_total
# --- OPERADORES DEL ALGORITMO GENÉTICO ---
# calculo de poblaciones
def crear_poblacion(size):
    poblacion = []
    for _ in range(size):
        individuo = list(ciudades.keys())
        random.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion

# seleccion de poblaciones
def seleccion(poblacion):
    torneo = random.sample(poblacion, 3)
    torneo.sort(key=fitness)
    return torneo[0]

# cruza
def cruza(padre1, padre2):
    inicio = random.randint(0, len(padre1) - 2)
    fin = random.randint(inicio, len(padre1) - 1)
    hijo = [-1] * len(padre1)
    hijo[inicio:fin] = padre1[inicio:fin]
    ptr = 0
    for ciudad in padre2:
        if ciudad not in hijo:
            while hijo[ptr] != -1:
                ptr += 1
            hijo[ptr] = ciudad
    return hijo

# mutacion
def mutacion(individuo, prob=0.2): 
    if random.random() < prob:
        a, b = sorted(random.sample(range(len(individuo)), 2))
        individuo[a:b] = reversed(individuo[a:b])
    return individuo
# --- COMPONENTE DE OPTIMIZACIÓN LOCAL (RECOCIDO SIMULADO) ---
# recorrido simulado
def recorrido_simulado(solucion):
    actual = solucion[:]
    mejor = solucion[:]
    temperatura = 1000  
    enfriamiento = 0.98  

    while temperatura > 0.1: 
        vecino = actual[:]

        i, j = sorted(random.sample(range(len(vecino)), 2))
        vecino[i:j] = reversed(vecino[i:j]) 

        fit_actual = fitness(actual)
        fit_vecino = fitness(vecino)
        
        if fit_vecino < fit_actual or random.random() < math.exp((fit_actual - fit_vecino) / temperatura):
            actual = vecino[:]
        
        if fitness(actual) < fitness(mejor):
            mejor = actual[:]
        temperatura *= enfriamiento
    return mejor
# --- MÉTODOS DE COMPARACIÓN (BASELINES) ---
# BASELINE ALEATORIO
def baseline_aleatorio():
    ruta = list(ciudades.keys())
    random.shuffle(ruta)
    return ruta

def evaluar_baseline_aleatorio(n=30):
    resultados = []
    for _ in range(n):
        ruta = baseline_aleatorio()
        resultados.append(fitness(ruta))
    return np.mean(resultados)

# BASELINE GREEDY
def baseline_greedy():
    nodos = list(ciudades.keys())
    actual = nodos[0]
    ruta = [actual]
    nodos.remove(actual)
    while nodos:
        siguiente = min(
            nodos,
            key=lambda x: distancia(actual, x)
        )
        ruta.append(siguiente)
        nodos.remove(siguiente)
        actual = siguiente
    return ruta

def evaluar_greedy():
    ruta = baseline_greedy()
    return fitness(ruta)
# --- ANÁLISIS DE RENDIMIENTO ---
def analizar_convergencia(historial):
    mejor_global = historial[0]
    generacion_estable = len(historial) 
    
    mejoras = []
    umbral_convergencia = 0.05 

    for i in range(1, len(historial)):
        mejora = abs(historial[i-1] - historial[i])
        mejoras.append(mejora)
        if mejora < umbral_convergencia and generacion_estable == len(historial):
            if i + 5 < len(historial):
                segmento = historial[i:i+5]
                if max(segmento) - min(segmento) < umbral_convergencia:
                    generacion_estable = i

    mejora_total = ((historial[0] - historial[-1]) / historial[0]) * 100

    return {
        "generacion_estable": generacion_estable,
        "mejora_total": mejora_total,
        "convergencia": np.mean(mejoras)
    }
def evaluar_robustez(n=5):
    resultados = []

    for _ in range(n):
        resultados.append(ejecutar_algoritmo_sin_graficas())

    return {
        "media": np.mean(resultados),
        "desviacion": np.std(resultados),
        "resultados": resultados
    }
# --- NÚCLEO DEL ALGORITMO HÍBRIDO ---
def ejecutar_algoritmo():
    inicio_tiempo = time.time()
    generaciones = 40
    poblacion_size = 20
    poblacion = crear_poblacion(poblacion_size)
    historial_hibrido = []
    historial_ga_simple = []
    pob_simple = poblacion[:]
    for _ in range(generaciones):
        pob_simple.sort(key=fitness)
        historial_ga_simple.append(fitness(pob_simple[0]))
        # Evolución estándar
        nueva = [pob_simple[0]]
        while len(nueva) < poblacion_size:
            h = mutacion(cruza(seleccion(pob_simple), seleccion(pob_simple)))
            nueva.append(h)
        pob_simple = nueva
    fit_ga_simple = fitness(pob_simple[0])

    pob_hibrida = poblacion[:] 
    for gen in range(generaciones):
        pob_hibrida.sort(key=fitness)
        mejor = pob_hibrida[0]
        
        mejor = recorrido_simulado(mejor)
        historial_hibrido.append(fitness(mejor))

        nueva_poblacion = [mejor]
        while len(nueva_poblacion) < poblacion_size:
            padre1 = seleccion(pob_hibrida)
            padre2 = seleccion(pob_hibrida)
            hijo = mutacion(cruza(padre1, padre2))
            nueva_poblacion.append(hijo)
        pob_hibrida = nueva_poblacion

    fin_tiempo = time.time()
    mejor_ruta = min(pob_hibrida, key=fitness)
    fitness_hibrido = fitness(mejor_ruta)
    baseline_aleat = evaluar_baseline_aleatorio()
    baseline_greed = evaluar_greedy()

    tiempo_ejecucion = fin_tiempo - inicio_tiempo
    analisis_conv = analizar_convergencia(historial_hibrido)
    def calc_mejora(actual):
        return round(((baseline_aleat - actual) / baseline_aleat) * 100, 2)

    tabla_comparativa = {
        "Aleatorio": {"fit": round(baseline_aleat, 2), "mejora": 0.0},
        "Greedy":    {"fit": round(baseline_greed, 2), "mejora": calc_mejora(baseline_greed)},
        "GA":        {"fit": round(fit_ga_simple, 2),  "mejora": calc_mejora(fit_ga_simple)},
        "Híbrido GA + SA":   {"fit": round(fitness_hibrido, 2),"mejora": calc_mejora(fitness_hibrido)}
    }
    generar_graficas(historial_hibrido, mejor_ruta)
    generar_mapa(mejor_ruta)
    grafica_baselines(tabla_comparativa) 
    robustez = evaluar_robustez(5)
    grafica_robustez(robustez["resultados"])

    return {
        'fitness': round(fitness_hibrido, 2),
        'tiempo': round(tiempo_ejecucion, 2),
        'robustez': robustez["desviacion"],
        'mejora_porcentaje': calc_mejora(fitness_hibrido),
        'generacion_estable': analisis_conv["generacion_estable"],
        'generacion_estable': analisis_conv["generacion_estable"],
        'convergencia': round(analisis_conv["convergencia"], 4),
        'tabla_data': tabla_comparativa, 
        'ruta': mejor_ruta
    }
# --- FUNCIONES DE VISUALIZACIÓN ---
def generar_graficas(historial, mejor_ruta):
    plt.rcParams.update({
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "#b0b3c1",
        "ytick.color": "#b0b3c1",
        "axes.edgecolor": "#35517cd0",
        "axes.linewidth": 0.8,
        "grid.color": "#35517cd0",
        "grid.alpha": 0.2,
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "font.family": "sans-serif"
    })

    plt.figure(figsize=(8, 5))

    x = [0, 1]  
    y = [historial[0], historial[-1]] 

    plt.plot(x, y, marker='o', markersize=10, linewidth=3, color='#00f2fe', markerfacecolor='white')
    
    plt.text(x[0]-0.05, y[0], f'{y[0]:.2f}', ha='right', va='center', fontsize=12, fontweight='bold', color='white')
    plt.text(x[1]+0.05, y[1], f'{y[1]:.2f}', ha='left', va='center', fontsize=12, fontweight='bold', color='#00f2fe')

    plt.xticks([0, 1], ['Baseline (Inicial)', 'Optimizado (Final)'])
    plt.xlim(-0.5, 1.5) 
    
    plt.title('Pendiente de Mejora (Fitness)')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_color('#35517cd0')
    plt.yticks([]) 
    
    plt.savefig('static/graficas/comparacion.png', bbox_inches='tight', dpi=120, transparent=True)
    plt.close()
# Versión sin graficas para evaluación de robustez
def ejecutar_algoritmo_sin_graficas():
    poblacion = crear_poblacion(50)

    for _ in range(100):
        poblacion.sort(key=fitness)
        mejor = recorrido_simulado(poblacion[0])

        nueva = [mejor]
        while len(nueva) < 50:
            nueva.append(mutacion(cruza(seleccion(poblacion), seleccion(poblacion))))

        poblacion = nueva

    return fitness(min(poblacion, key=fitness))
# Función para graficar la robustez estadística
def grafica_robustez(resultados):
    mejor = np.min(resultados)
    peor = np.max(resultados)
    media = np.mean(resultados)
    desviacion = np.std(resultados)
    mediana = np.median(resultados)
    cv = (desviacion / media) * 100  

    plt.figure(figsize=(6, 4))
    ax = plt.gca()
    ax.axis('off') 

    datos_tabla = [
        ["Mejor Resultado", f"{mejor:.2f}"],
        ["Peor Resultado", f"{peor:.2f}"],
        ["Media (Promedio)", f"{media:.2f}"],
        ["Mediana", f"{mediana:.2f}"],
        ["Desviación Estándar", f"{desviacion:.2f}"],
        ["Consistencia (CV%)", f"{cv:.2f}%"]
    ]

    tabla = plt.table(
        cellText=datos_tabla,
        colLabels=["Métrica de Robustez", "Valor Obtenido"],
        loc='center',
        cellLoc='left',
        colColours=["#35517c", "#35517c"], 
        bbox=[0.1, 0.1, 0.8, 0.8] 
    )


    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1.2, 2.5) 
    for (row, col), cell in tabla.get_celld().items():
        cell.set_text_props(color='white')
        cell.set_edgecolor((1, 1, 1, 0.1)) 
        
        if row == 0: 
            cell.set_text_props(weight='bold', color='#7fffd4') 
            cell.set_facecolor("#1a2a44")
        else: 
            cell.set_facecolor((0.05, 0.05, 0.1, 0.5))
            if col == 1: 
                cell.set_text_props(weight='bold')

    plt.title("Reporte de Estabilidad Estadística", color='white', pad=20, fontsize=14, fontweight='bold')
    

    plt.savefig("static/graficas/robustez.png", transparent=True, bbox_inches='tight', dpi=150)
    plt.close()
# Función para graficar los resultados de los baselines
def grafica_baselines(data):
    metodos = list(data.keys())
    valores_fit = [v["fit"] for v in data.values()]
    valores_fit_num = [float(f) if isinstance(f, str) else f for f in valores_fit]

    plt.figure(figsize=(9, 7))
    colores = ["#0090a3", "#12f3e0", "#59abb6", '#00f2fe']

    barras = plt.bar(metodos, valores_fit_num, color=colores, edgecolor='white', alpha=0.8)

    plt.bar_label(barras, padding=3, color='white', fontweight='bold', fontsize=10)

    plt.xticks([])

    column_labels = ["Fitness", "Mejora %"]
    table_data = []
    for m in metodos:
        mejora = data[m]['mejora']
        table_data.append([data[m]["fit"], f"{mejora}%"])

    the_table = plt.table(cellText=table_data,
                        rowLabels=metodos,
                        colLabels=column_labels,
                        rowColours=colores,
                        colColours=["#35517c", "#35517c"], 
                        cellLoc='center',
                        loc='bottom',
                        bbox=[0.0, -0.6, 1.0, 0.5]) 

    the_table.auto_set_font_size(False)
    the_table.set_fontsize(11) 
    
    for (row, col), cell in the_table.get_celld().items():
        cell.set_text_props(color='white')
        cell.set_edgecolor((1, 1, 1, 0.2)) 

        cell.set_height(0.15) 
        
        if row > 0:
            cell.set_facecolor((0.05, 0.05, 0.1, 0.6))
        if row == 0: 
            cell.set_text_props(weight='bold')
            cell.set_facecolor("#35517c")

    plt.title('Baseline: Comparación de Métodos', pad=25, color='white', fontsize=14)
    plt.ylabel('Fitness (Costo)', color='white')

    plt.subplots_adjust(left=0.2, bottom=0.45, right=0.95, top=0.9)
    
    plt.savefig("static/graficas/baseline.png", transparent=True, bbox_inches='tight', dpi=120)
    plt.close()
#creacion visual de mapa de ruta
def generar_mapa(mejor_ruta):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_axes([0, 0, 1, 1]) 
    try:
        img = plt.imread('static/mapa.png') 
        ax.imshow(img, extent=[0, 100, 0, 100], aspect='auto', alpha=0.9)
    except:
        ax.set_facecolor('#0d1117')

    x = [ciudades[c][0] for c in mejor_ruta]
    y = [ciudades[c][1] for c in mejor_ruta]
    x.append(ciudades[mejor_ruta[0]][0])
    y.append(ciudades[mejor_ruta[0]][1])

    plt.plot(x, y, color='#00f2fe', linewidth=3, zorder=2,
            path_effects=[patheffects.withStroke(linewidth=5, foreground="black")])

    plt.scatter(x[:-1], y[:-1], s=100, c='white', edgecolors='#00f2fe', linewidths=2, zorder=3)

    for i, ciudad_id in enumerate(mejor_ruta):
        plt.text(ciudades[ciudad_id][0] + 1, ciudades[ciudad_id][1] + 1, 
                f"{i+1}", color='white', fontsize=12, fontweight='bold',
                path_effects=[patheffects.withStroke(linewidth=3, foreground="black")], zorder=4)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off') 
    plt.savefig('static/graficas/mapa_ruta.png', 
                bbox_inches='tight', 
                pad_inches=0, 
                dpi=150)
    plt.close()
#########################################################################################