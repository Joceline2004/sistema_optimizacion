function mostrar(id){

    let secciones = document.querySelectorAll('.seccion');

    secciones.forEach(sec => {
        sec.classList.remove('activa');
    });

    document.getElementById(id).classList.add('activa');
}
document.addEventListener("DOMContentLoaded", function () {

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