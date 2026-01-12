const urlImagen = document.getElementById("urlImagen");
const btnAgregar = document.getElementById("btnAgregar");
const btnEliminar = document.getElementById("btnEliminar");
const galeria = document.getElementById("galeria");

btnAgregar.addEventListener("click", () => {
    const url = urlImagen.value.trim();
    
    if (url === "") {
        alert("Por favor ingresa una URL");
        return;
    }

    const img = document.createElement("img");
    img.src = url;
    img.alt = "Imagen de galería";
    
    img.addEventListener("click", () => {
        const todasImagenes = document.querySelectorAll(".galeria img");
        todasImagenes.forEach(imagen => {
            imagen.classList.remove("seleccionada");
        });
        img.classList.add("seleccionada");
    });

    galeria.appendChild(img);
    urlImagen.value = "";
});

btnEliminar.addEventListener("click", () => {
    const imagenSeleccionada = document.querySelector(".galeria img.seleccionada");
    
    if (imagenSeleccionada) {
        imagenSeleccionada.remove();
    } else {
        alert("Selecciona una imagen primero");
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Delete") {
        const imagenSeleccionada = document.querySelector(".galeria img.seleccionada");
        if (imagenSeleccionada) {
            imagenSeleccionada.remove();
        }
    }
});

urlImagen.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        btnAgregar.click();
    }
});