function mostrar(id){

    let secciones = document.querySelectorAll('.seccion');

    secciones.forEach(sec => {
        sec.classList.remove('activa');
    });

    document.getElementById(id).classList.add('activa');
}
document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // PLUGIN: TEXTO EN EL CENTRO
    // ==============================
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


    // ==============================
    // FUNCION PARA CREAR GRAFICAS
    // ==============================
    function crearGrafica(id, valor, color, maximo = null) {

        // Evitar errores de escala
        if (!maximo) {
            maximo = valor * 1.5;
        }

        new Chart(document.getElementById(id), {

            type: 'doughnut',

            data: {

                labels: ['Valor', 'Restante'],

                datasets: [{
                    data: [valor, Math.max(maximo - valor, 0)],
                    backgroundColor: [color, '#e0e0e0'],
                    borderWidth: 0
                }]
            },

            options: {

                responsive: true,

                cutout: '70%',

                plugins: {
                    legend: {
                        display: false
                    }
                }
            },

            plugins: [centerTextPlugin]
        });
    }


    // ==============================
    // CREAR GRAFICAS
    // ==============================

    crearGrafica(
        'fitnessChart',
        Number(resultados.fitness),
        '#6a0dad',
        1000
    );

    crearGrafica(
        'tiempoChart',
        Number(resultados.tiempo),
        '#ff6600',
        100
    );

    crearGrafica(
        'desviacionChart',
        Number(resultados.desviacion),
        '#00b894',
        100
    );


    // ==============================
    // MOSTRAR VALORES EN TEXTO
    // ==============================

    document.getElementById('fitnessValor').innerText =
        "Fitness: " + Number(resultados.fitness).toFixed(2);

    document.getElementById('tiempoValor').innerText =
        "Tiempo: " + Number(resultados.tiempo).toFixed(2) + " s";

    document.getElementById('desviacionValor').innerText =
        "Desviación: " + Number(resultados.desviacion).toFixed(2);

});