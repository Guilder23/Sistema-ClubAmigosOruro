# Historias de Usuario Detalladas

## HU-16 Buscador de productos (Prioridad: Baja)
- Como usuario quiero buscar productos por nombre para encontrar rapidamente items dentro del catalogo.
- Criterios de aceptacion:
  - Se puede buscar por codigo, detalle o categoria.
  - El filtrado se aplica en tiempo real con JavaScript.
  - Si no hay resultados, la tabla queda vacia sin romper el layout.
- Alcance tecnico:
  - Vista: templates/productos/productos.html
  - JS: static/js/productos/productos.js

## HU-17 Categorias (Prioridad: Media)
- Como administrador quiero organizar productos por categorias para mantener el catalogo ordenado.
- Criterios de aceptacion:
  - Listado de categorias con estado.
  - Modals para crear, ver, editar y eliminar.
  - Busqueda y filtro por estado.
- Alcance tecnico:
  - Vista: templates/categorias/categorias.html
  - Modals: templates/categorias/modals/

## HU-18 Productos destacados (Prioridad: Baja)
- Como administrador quiero destacar ciertos productos para resaltarlos en el sistema.
- Criterios de aceptacion:
  - Listado de productos destacados.
  - Acciones CRUD mediante modals.
- Alcance tecnico:
  - Vista: templates/destacados/destacados.html
  - Modals: templates/destacados/modals/

## HU-19 Control de stock (Prioridad: Media)
- Como administrador quiero controlar la cantidad disponible para evitar quiebres de inventario.
- Criterios de aceptacion:
  - Se muestra stock actual y minimo por producto.
  - Se permiten acciones desde modals.
- Alcance tecnico:
  - Vista: templates/stock/stock.html
  - Modals: templates/stock/modals/

## HU-20 Estadisticas basicas (Prioridad: Baja)
- Como administrador quiero ver metricas simples del sistema para tomar decisiones rapidas.
- Criterios de aceptacion:
  - Tarjetas con metricas clave.
  - Vista de detalle mediante modal.
- Alcance tecnico:
  - Vista: templates/estadisticas/estadisticas.html
  - Modals: templates/estadisticas/modals/

## HU-21 Historial de cambios (Prioridad: Baja)
- Como administrador quiero ver cambios realizados en productos para trazabilidad.
- Criterios de aceptacion:
  - Tabla con fecha, usuario, accion y producto.
  - Modal para revisar detalle.
- Alcance tecnico:
  - Vista: templates/historial/historial.html
  - Modals: templates/historial/modals/

## Estructura definida
- Cada HTML tiene su CSS y JS dedicado.
- Todas las gestiones tienen carpeta principal y subcarpeta modals:
  - crear
  - ver
  - editar
  - eliminar
- Layout compartido clonado de Sistema-Inventario para:
  - Navbar
  - Sidebar
  - Footer
