# proyecto-base-de-datos
# SubcultureCentral  
Gestor de eventos para subculturas musicales (rave, dubstep, rock alternativo, metal, indie, techno, etc.)

Subculture Planner es una aplicación web CRUD desarrollada con **Python + Flask** y **MariaDB**, diseñada para gestionar eventos de música alternativa y underground.  
Permite administrar artistas, eventos, ubicaciones, lineups, asistentes, patrocinadores, entradas, merchandising y más.  
El proyecto está desplegado en un entorno distribuido con **dos máquinas virtuales**: una para la base de datos y otra para el servidor web.

---

## 🎯 Objetivo del Proyecto

El objetivo es demostrar:

- Modelado de datos relacional (ER + modelo lógico).
- Implementación de un sistema CRUD completo.
- Gestión de consultas complejas mediante una pantalla de búsqueda avanzada.
- Despliegue en un entorno distribuido (2 máquinas virtuales).
- Acceso público mediante dominio dinámico (No-IP / DuckDNS).
- Seguridad mediante usuarios SQL con privilegios limitados.

---

## 🧩 Funcionalidades Principales

### ✔ Gestión de artistas  
- Alta, edición, listado y eliminación.  
- Géneros musicales, subgéneros, enlaces sociales, caché, país.

### ✔ Gestión de eventos  
- Título, descripción, fecha, horarios, tipo de evento, estado.  
- Asociación con ubicaciones y artistas.

### ✔ Ubicaciones  
- Espacios públicos, salas, warehouses, ubicaciones secretas.  
- Capacidad, ciudad, coordenadas GPS.

### ✔ Lineup (relación N–M)  
- Artistas asignados a eventos.  
- Horarios de actuación y orden en el cartel.

### ✔ Asistentes y listas de invitados  
- Gestión de invitados, confirmaciones y notas.

### ✔ Solicitudes de equipo  
- Subwoofers, luces, pantallas LED, amplificadores, etc.

### ✔ Patrocinadores y relación con eventos  
- Marcas, colectivos, promotoras, tiendas alternativas.

### ✔ Tickets  
- Tipos de entrada, precios, QR, estado.

### ✔ Merchandising  
- Productos oficiales de artistas (camisetas, vinilos, pósters…).

### ✔ Búsqueda avanzada  
Filtros por:
- Género musical  
- Tipo de evento  
- Ciudad  
- Capacidad mínima  
- Rango de fechas  
- Artista participante  
- Ubicaciones secretas o públicas  

---

## 🗄️ Modelo de Datos

El sistema incluye **11 tablas**:

- `artista`
- `evento`
- `ubicación`
- `lineup`
- `asistente`
- `lista_invitados`
- `solicitud_equipo`
- `patrocinador`
- `evento_patrocinador`
- `ticket`
- `merch`
