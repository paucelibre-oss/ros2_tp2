# Ejercicios Clase 2 - ROS 2

Este repositorio contiene la solución de los dos ejercicios de la clase 2 de ROS 2: un contador con reset por servicio, y un par de nodos que se comunican por action para "republicar" un texto palabra por palabra.

## Contenido

Tres paquetes:

- **`tp_interfaces`** – acá se describen las interfaces custom: el servicio `ResetCounter` y la action `RepublishText`.
- **`tp_ejercicio1`** – el contador. Tiene un nodo que publica y otro que escucha y decide cuándo pedir el reset.
- **`tp_ejercicio2`** – el action server/client del texto.

## Cómo correrlo

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Con `--symlink-install`, si se modifica algo de los `.py`, no hace falta recompilar — solo reiniciar el nodo. Los cambios en los `.srv` / `.action` sí piden un `colcon build` de nuevo.
