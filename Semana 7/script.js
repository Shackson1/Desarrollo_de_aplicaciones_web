
const productos = [
  { nombre: "Leche", precio: "1.00", descripcion: "Leche de vaca" },
  { nombre: "Huevos", precio: "0.15", descripcion: "Huevos de gallina." },
];

const listaProductos = document.getElementById("listaProductos");
const contadorProductos = document.getElementById("contadorProductos");


function crearElementoProducto(producto) {
  const item = document.createElement("li");
  item.className = "list-group-item";

  item.innerHTML = `
    <div class="d-flex justify-content-between align-items-start">
      <div class="me-3">
        <div class="fw-semibold">${producto.nombre}</div>
        <div class="text-muted small">${producto.descripcion}</div>
      </div>
      <span class="badge text-bg-success">$ ${producto.precio}</span>
    </div>
  `;

  return item;
}



function actualizarContador() {
  contadorProductos.textContent =
    productos.length === 1 ? "1 producto" : `${productos.length} productos`;
}

function renderizarProductos() {
  listaProductos.innerHTML = "";

  for (const producto of productos) {
    const item = crearElementoProducto(producto);
    listaProductos.appendChild(item);
  }

  actualizarContador();
}


renderizarProductos();
