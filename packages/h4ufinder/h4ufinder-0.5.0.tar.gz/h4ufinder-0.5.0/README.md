# Hack4u Academy Courses Library

Una biblioteca python para consultar los cursos de la academia Hack4u

## Instalación

Instala el paquete utilizando 'pip3'
```python3
pip3 install h4ufinder
```
## Uso básico

### Listar todos los cursos
```python3
from hack4u import courses

for course in courses
print(course)
```
### Obtener un curso por nombre
```python3
from hack4u import search_course_by_name

course = search_course_by_name("Introducción a Linux")
print(course)
```
### Calcular duración total de los cursos
```python3
from hack4u import total_duration

print (f"duración total {total_duration()} horas")
```
