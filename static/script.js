$.ajax({
  url: "/api-turnos",
  type: "GET",
  success: function (datos) {
    let lista = datos;
    let container = document.getElementById("container");
    lista.forEach((elemento, indice, arr) => {
      const div = document.createElement("div");
      div.innerHTML = `    <h1> ${elemento["guardia"]} </h1>
                           <h2> ${elemento["espacio"]}</h2>
                           <h3> ${elemento["hora_inicio"]} - ${elemento["hora_fin"]} </h3>
                           <p> - - - - - - - - - - - - - - - - - - - - - -</p>`;
      container.appendChild(div);
    });
  },
  error: function () {
    console.log("Error al obtener datos de la API");
  },
});
