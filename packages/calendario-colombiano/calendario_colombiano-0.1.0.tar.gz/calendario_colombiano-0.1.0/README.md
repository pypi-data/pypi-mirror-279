# Calendario Colombiano


La biblioteca calendario_colombiano proporciona funcionalidades para manejar los festivos y fechas especiales en Colombia.

# Instalación

### Puedes instalar la biblioteca usando pip:

`pip install calendario_colombiano`


### Uso

A continuación se muestra un ejemplo básico de cómo utilizar la biblioteca:

`Python`

```from calendario_colombiano.calendario import CalendarioColombiano
from datetime import date

calendario = CalendarioColombiano()

# Verificar si una fecha es festivo
fecha = date(2024, 1, 1)
es_festivo = calendario.es_festivo(fecha)
print(f"¿{fecha} es festivo en Colombia? {es_festivo}")

# Obtener los festivos de un año específico
festivos_2024 = calendario.obtener_festivos(2024)
print(f"Festivos en Colombia para el año 2024: {festivos_2024}")

# Obtener el próximo festivo
proximo_festivo = calendario.proximo_festivo(date.today())
print(f"El próximo festivo es: {proximo_festivo}")
```

### Contribuir

- Clona el repositorio (git clone https://github.com/MarkSerna/calendario_colombiano.git)
- Crea tu rama de características (git checkout -b mi-caracteristica)
- Realiza tus cambios
- Haz commit de tus cambios (git commit -am 'Añadir nueva caracteristica')
- Sube tus cambios (git push origin mi-caracteristica)
- Abre un Pull Request

### Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](https://github.com/MarkSerna/calendario_colombiano/blob/main/LICENSE) para más detalles.


### Contacto

Si tienes preguntas o sugerencias, no dudes en contactarme a través de mi perfil de GitHub @MarkSerna.