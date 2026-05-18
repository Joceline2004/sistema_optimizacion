/**
 * SISTEMA DE NAVEGACIÓN Y RENDERIZADO DE DASHBOARD - IntelRR
 * Gestiona la visibilidad de las secciones y la actualización de métricas en tiempo real.
 */

/**
 * Controla el cambio de pestañas (Tabs) en la interfaz.
 * @param {string} id - El ID del elemento HTML que se desea visualizar.
 */
function mostrar(id) {
    // Selecciona todos los contenedores con la clase '.seccion'
    let secciones = document.querySelectorAll('.seccion');

    // Oculta todas las secciones eliminando la clase de visibilidad
    secciones.forEach(sec => {
        sec.classList.remove('activa');
    });

    // Activa únicamente la sección solicitada por ID
    document.getElementById(id).classList.add('activa');
}

/**
 * Inicialización de componentes visuales una vez cargado el DOM.
 * Gestiona plugins de gráficos y vinculación de variables del motor metaheurístico.
 */
document.addEventListener("DOMContentLoaded", function () {

    /**
     * Plugin personalizado para Chart.js: centerText.
     * Dibuja el valor principal (Fitness) en el centro de los gráficos de dona/progreso.
     */
    const centerTextPlugin = {
        id: 'centerText',

        beforeDraw(chart) {
            const { width, height, ctx } = chart;
            ctx.restore();


            let fontSize = (height / 8).toFixed(2);
            ctx.font = fontSize + "px Arial";
            ctx.textBaseline = "middle";
            ctx.fillStyle = "#21deffb0"; 


            const value = chart.config.data.datasets[0].data[0];
            const text = value.toFixed(2);

            const textX = Math.round(
                (width - ctx.measureText(text).width) / 2
            );
            const textY = height / 2;

            ctx.fillText(text, textX, textY);
            ctx.save();
        }
    };

    /**
     * VINCULACIÓN DE MÉTRICAS DEL ALGORITMO HÍBRIDO
     * Se inyectan los resultados del objeto global 'window.resultados' 
     * generado por el backend de Python.
     */


    document.getElementById("fitnessValor").innerText = 
        window.resultados.fitness.toFixed(2);


    document.getElementById("tiempoValor").innerText = 
        window.resultados.tiempo.toFixed(2) + " s";


    document.getElementById("stdValor").innerText =
        "± " + window.resultados.robustez.toFixed(2);


    document.getElementById("convValor").innerText =
        "Gen " + window.resultados.generacion_estable;


    document.getElementById("mejoraValor").innerText =
        window.resultados.mejora_porcentaje.toFixed(2) + "%";
});