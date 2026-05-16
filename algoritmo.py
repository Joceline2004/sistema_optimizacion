import random
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Configura el backend para generar archivos sin GUI
import matplotlib.pyplot as plt
import time

#Generacion de ciudades
num_ciudades = 12

ciudades = {
    i : (   random.randint(0, 100), random.randint(0,100))
    for i in range(num_ciudades)
}
#distancia entre dos ciudades

def distancia(ciudad1, ciudad2):
    x1, y1 = ciudades[ciudad1]
    x2, y2 = ciudades[ciudad2]
    return math.sqrt((x2-x1)**2 + (y2 - y1)**2)

# calculo de fitness de la ruta

def fitness(ruta):
    distancia_total = 0
    tiempo_total = 0
    costo_total = 0
    
    for i in range (len(ruta) -1 ):
        d = distancia (ruta[i], ruta[i+1])

        distancia_total += d
        tiempo_total += d
        costo_total += d *0.8

    fitness_total = (
        0.4 * distancia_total +
        0.3 * tiempo_total +
        0.3 * costo_total
    )
    return fitness_total

#calculo de poblaciones

def crear_poblacion(size):

    poblacion = []

    for _ in range(size):
        individuo = list(ciudades.keys())
        random.shuffle(individuo)
        poblacion.append(individuo)

    return poblacion

#seleccion de poblaciones
def seleccion(poblacion):

    torneo = random.sample(poblacion, 3)

    torneo.sort(key=fitness)

    return torneo[0]

#cruza
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
#mutacion
def mutacion(individuo, prob=0.1):

    if random.random() < prob:

        a, b = random.sample(range(len(individuo)), 2)

        individuo[a], individuo[b] = individuo[b], individuo[a]

    return individuo
#recorrido
def recorrido_simulado(solucion):
    actual = solucion[:]
    mejor = solucion[:]

    temperatura = 100
    enfriamiento = 0.95

    while temperatura > 1:
        vecino= actual[:]
        a , b = random.sample(range(len(vecino)), 2)
        vecino [a], vecino[b] = vecino [b], vecino[a]

        fit_actual = fitness(actual)
        fit_vecino = fitness(vecino)
        diferencia = fit_vecino - fit_actual

        if diferencia < 0:
            actual = vecino[:]

        else:
            probabilidad = math.exp(-diferencia /temperatura)

            if random.random() < probabilidad:
                actual = vecino[:]
        
        if fitness(actual) < fitness(mejor):
            mejor = actual[:]
        temperatura *= enfriamiento
    
    return mejor

#algoritmo hibrido
def ejecutar_algoritmo():

    inicio_tiempo = time.time()

    generaciones = 100
    poblacion_size = 50

    poblacion = crear_poblacion(poblacion_size)

    historial_fitness = []

    for gen in range(generaciones):

        nueva_poblacion = []

        poblacion.sort(key=fitness)

        mejor = poblacion[0]

        mejor = recorrido_simulado(mejor)

        historial_fitness.append(fitness(mejor))

        nueva_poblacion.append(mejor)

        while len(nueva_poblacion) < poblacion_size:

            padre1 = seleccion(poblacion)
            padre2 = seleccion(poblacion)

            hijo = cruza(padre1, padre2)

            hijo = mutacion(hijo)

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    fin_tiempo = time.time()

    mejor_ruta = min(poblacion, key=fitness)

    tiempo_ejecucion = fin_tiempo - inicio_tiempo

    desviacion = np.std(historial_fitness)

    generar_graficas(historial_fitness, mejor_ruta)

    return {
        'fitness': round(fitness(mejor_ruta), 2),
        'tiempo': round(tiempo_ejecucion, 2),
        'desviacion': round(desviacion, 2),
        'ruta': mejor_ruta
    }

#graficas
def generar_graficas(historial, mejor_ruta):
    # --- CONFIGURACIÓN DE ESTILO "DARK ELECTRIC" ---
    plt.rcParams.update({
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "#b0b3c1",
        "ytick.color": "#b0b3c1",
        "axes.edgecolor": "#35517cd0", # Tu borde azul definido en el CSS
        "axes.linewidth": 0.8,
        "grid.color": "#35517cd0",
        "grid.alpha": 0.2,
        "figure.facecolor": "none", # Transparente
        "axes.facecolor": "none",   # Transparente
        "font.family": "sans-serif" # Si tienes instalada Poppins en el sistema, ponla aquí
    })

    # 1. CONVERGENCIA (Estilo Neón)
    plt.figure(figsize=(8, 5))
    # Azul eléctrico para la línea
    plt.plot(historial, color='#00f2fe', linewidth=2, label='Fitness')
    # Degradado bajo la curva (transparencia azul)
    plt.fill_between(range(len(historial)), historial, color='#00f2fe', alpha=0.1)
    
    plt.title('Progreso de Optimización', fontsize=14, pad=20, fontweight='light')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.grid(True, axis='y', linestyle=':')
    
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    # IMPORTANTE: transparent=True para que se vea el fondo del dashboard detrás
    plt.savefig('static/graficas/convergencia.png', bbox_inches='tight', dpi=120, transparent=True)
    plt.close()

    # 2. COMPARACIÓN (Barras Estilo Vidrio)
    plt.figure(figsize=(6, 5))
    etiquetas = ['Inicial', 'Optimizado']
    valores = [historial[0], historial[-1]]
    
    # Colores eléctricos de tu paleta
    barras = plt.bar(etiquetas, valores, color=['#35517cd0', '#00f2fe'], width=0.5, edgecolor="white", linewidth=0.5)
    
    # Etiquetas blancas sobre barras
    plt.bar_label(barras, padding=5, fmt='%.2f', color='white', fontsize=10, fontweight='bold')
    
    plt.title('Mejora de Rendimiento', fontsize=14, pad=20)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.yticks([]) 

    plt.savefig('static/graficas/comparacion.png', bbox_inches='tight', dpi=120, transparent=True)
    plt.close()

    # 3. MAPA DE RUTA (Nodos Eléctricos)
    plt.figure(figsize=(8, 6))
    
    # Líneas de conexión azul suave
    for i in range(len(mejor_ruta) - 1):
        x1, y1 = ciudades[mejor_ruta[i]]
        x2, y2 = ciudades[mejor_ruta[i + 1]]
        plt.plot([x1, x2], [y1, y2], color='#00f2fe', alpha=0.4, zorder=1, linewidth=1)

    # Nodos estilo neón
    x_coords = [c[0] for c in ciudades.values()]
    y_coords = [c[1] for c in ciudades.values()]
    plt.scatter(x_coords, y_coords, color='#d66564', s=80, edgecolors='white', linewidth=1, zorder=2)

    # Etiquetas blancas
    for i, (x, y) in ciudades.items():
        plt.text(x + 1.5, y + 1.5, str(i), fontsize=10, color='white', fontweight='light')

    plt.title('Configuración de Ruta Final', fontsize=14, pad=20)
    plt.axis('off') 
    
    plt.savefig('static/graficas/ruta.png', bbox_inches='tight', dpi=120, transparent=True)
    plt.close()