function optimizarRuta() {
    const temperatura = document.getElementById("temperatura").value;
    const minima = document.getElementById("minima").value;
    const velocidad = document.getElementById("velocidad").value;

    fetch("/optimizar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            temperatura: temperatura,
            minima: minima,
            velocidad: velocidad
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultadoDiv = document.getElementById("resultado");
        resultadoDiv.style.display = "block";
        resultadoDiv.innerHTML = `
            <h2>Ruta Optimizada:</h2>
            <p><strong>Ruta:</strong> ${data.ruta.join(" → ")}</p>
            <p><strong>Distancia Total:</strong> ${data.distancia} unidades</p>
        `;
    })
    .catch(error => {
        alert("Error al optimizar la ruta.");
        console.error(error);
    });
}
