$.ajax({
  url: "/api_turnos",
  type: "GET",

  success: function (datos_json) {
    let lista = datos_json;
    let container = document.getElementById("container");

    lista.forEach((elemento, indice, arr) => {
      const div = document.createElement("div");

      // Crear el contenedor principal
      const cardContainer = document.createElement("div");
      cardContainer.classList.add("bg-[#F0E9D2]");

      // Contenido de la Tarjeta
      const cardContent = document.createElement("div");
      cardContent.classList.add("flex", "justify-between", "items-center");

      // Crear la sección de imagen
      const imageSection = document.createElement("div");
      imageSection.classList.add(
        "p-2",
        "bg-[#E6DDC4]",
        "h-[150px]",
        "flex",
        "items-center"
      );

      const image = document.createElement("img");
      image.classList.add("h-40", "w-40");
      image.src = "/static/patio-de-recreo.png";
      image.alt = "patio";

      // Agregar imagen a la sección de imagen
      imageSection.appendChild(image);

      // Crear la sección de texto
      const textSection = document.createElement("div");
      textSection.classList.add(
        "flex",
        "w-[100%]",
        "items-center",
        "justify-between"
      );

      const title = document.createElement("h2");
      title.classList.add("text-center", "font-['SF_Mono']");
      title.textContent = "Of. Jorge Gonzalez";

      const timeSection = document.createElement("div");
      timeSection.classList.add("w-[30%]", "border-l-4", "border-black");

      const time = document.createElement("p");
      time.classList.add("text-center");
      time.textContent = "17:00 hs";

      // Agregar texto y tiempo a la sección de texto
      timeSection.appendChild(time);
      textSection.appendChild(title);
      textSection.appendChild(timeSection);

      // Agregar sección de imagen y texto al contenido de la tarjeta
      cardContent.appendChild(imageSection);
      cardContent.appendChild(textSection);

      // Crear la sección inferior de la tarjeta
      const bottomSection = document.createElement("div");
      const bottomText = document.createElement("p");
      bottomText.classList.add(
        "uppercase",
        "bg-[#181D31]",
        "text-center",
        "text-white"
      );
      bottomText.textContent = "patio";
      bottomSection.appendChild(bottomText);

      // Agregar contenido a la tarjeta
      cardContainer.appendChild(cardContent);
      cardContainer.appendChild(bottomSection);

      // Agregar la tarjeta al contenedor principal del documento
      document.body.appendChild(cardContainer);

      container.appendChild(div);
    });
  },

  error: function () {
    console.log("Error al obtener de la API");
  },
});
