# Especificación final del sistema de gestión de estacionamiento

## 1. Propósito del sistema

El sistema permite administrar por consola las operaciones básicas de un estacionamiento: registrar ingresos y egresos de vehículos, consultar espacios disponibles, gestionar clientes registrados y visualizar estadísticas simples.

El proyecto se desarrollará en Python con una complejidad adecuada a un nivel inicial. Por lo tanto, se priorizará una solución clara, modular y comprensible, basada en funciones, estructuras condicionales, estructuras repetitivas, validaciones simples y persistencia mediante archivos.

La persistencia será real: los datos se leerán y escribirán en archivos del proyecto. Sin embargo, algunos datos iniciales podrán ser ficticios para permitir una demostración completa sin cargar manualmente una gran cantidad de operaciones.

## 2. Alcance funcional

### 2.1 Funciones incluidas

El sistema incluirá las siguientes funciones principales:

- registrar ingreso de un vehículo;
- registrar egreso de un vehículo;
- registrar cliente;
- consultar cliente;
- consultar espacios disponibles;
- consultar estadísticas;
- finalizar el programa.

### 2.2 Funciones no incluidas

Para mantener el alcance acorde a la consigna, no se implementarán:

- interfaz gráfica;
- base de datos;
- usuarios con contraseña;
- reservas anticipadas;
- emisión real de comprobantes fiscales;
- integración con medios de pago;
- control de patentes;
- tarifas diferenciadas por tipo de vehículo.

La identificación principal del cliente será el DNI. La identificación física de la ocupación será el código del espacio.

## 3. Conceptos principales

### 3.1 Cliente

Un cliente representa a una persona que utiliza el estacionamiento. Puede estar registrado o no.

Para simplificar el funcionamiento, todo ingreso solicitará un DNI. Si el DNI no existe en el archivo de clientes, el sistema ofrecerá registrarlo. Si el usuario decide no registrar al cliente, igualmente podrá continuar el ingreso como cliente no registrado, guardando el DNI en el movimiento.

Los clientes registrados tendrán acumulación de horas históricas y podrán acceder a beneficios informativos o descuentos simples.

### 3.2 Espacio

Un espacio representa un lugar físico disponible para estacionar. Cada espacio tendrá:

- un código único;
- un piso;
- un número de orden dentro del piso.

Ejemplo de código: `P1-E01`, donde `P1` representa el piso 1 y `E01` representa el espacio 1.

El archivo de espacios será de configuración estática. Esto significa que define la capacidad total del estacionamiento y no se modificará durante la ejecución normal del sistema.

### 3.3 Movimiento

Un movimiento es un registro de ingreso o egreso asociado a un espacio, un DNI y una fecha/hora.

El sistema utilizará una bitácora de movimientos. Cada operación agregará una línea al archivo, sin borrar los movimientos anteriores.

### 3.4 Ocupación actual

La ocupación actual no se guardará en un archivo separado. Se calculará al iniciar el programa leyendo:

1. la lista completa de espacios;
2. la bitácora de movimientos.

Si el último movimiento de un espacio fue un ingreso, el espacio estará ocupado. Si el último movimiento fue un egreso, el espacio estará disponible. Si un espacio no tiene movimientos, también estará disponible.

Esta decisión evita duplicar información y permite reconstruir el estado del estacionamiento a partir del historial real de operaciones.

## 4. Flujo general del programa

### 4.1 Inicio del sistema

Al iniciar, el programa realizará las siguientes acciones:

1. cargar la configuración de espacios;
2. cargar los clientes registrados;
3. leer la bitácora de movimientos;
4. reconstruir la ocupación actual;
5. cargar estadísticas acumuladas;
6. mostrar el menú principal.

Si algún archivo de datos no existe, el sistema podrá crearlo con una estructura inicial válida, excepto el archivo de espacios, que debe existir porque define la capacidad del estacionamiento.

### 4.2 Menú principal

El menú principal mostrará opciones numeradas:

1. Registrar ingreso
2. Registrar egreso
3. Registrar cliente
4. Consultar cliente
5. Consultar espacios disponibles
6. Consultar estadísticas
7. Finalizar programa

El usuario deberá ingresar el número de la opción. Si ingresa un valor inválido, el sistema mostrará un mensaje claro y volverá a solicitar la opción.

### 4.3 Continuidad después de cada operación

Después de completar una operación, el sistema volverá al menú correspondiente.

En operaciones de consulta, el sistema podrá mostrar el mensaje:

`Presione Enter para volver al menú...`

No será necesario preguntar en cada consulta si desea continuar, porque la opción de finalizar programa ya estará disponible en el menú principal. Esto simplifica el flujo y evita salidas accidentales.

### 4.4 Finalización

Al seleccionar finalizar, el sistema mostrará un mensaje como:

`Cerrando sistema...`

Luego terminará la ejecución. Si se desea simular un cierre más realista, puede utilizarse una pausa breve con `time.sleep(1)`.

## 5. Flujo de usuario por operación

### 5.1 Registrar ingreso

#### Objetivo

Registrar que un vehículo ocupa un espacio disponible del estacionamiento.

#### Flujo

1. El usuario selecciona `Registrar ingreso`.
2. El sistema solicita el DNI del cliente.
3. El sistema valida que el DNI tenga formato numérico y una longitud razonable, por ejemplo entre 7 y 8 dígitos.
4. El sistema busca el DNI en el archivo de clientes.
5. Si el cliente existe, muestra un saludo o confirmación breve con su nombre.
6. Si el cliente no existe, pregunta si desea registrarlo.
7. Si el usuario decide registrarlo, se solicita el nombre y se crea el cliente.
8. Si el usuario decide no registrarlo, el ingreso continúa como cliente no registrado.
9. El sistema verifica si existen espacios disponibles.
10. Si no hay espacios disponibles, informa que el estacionamiento está completo y vuelve al menú.
11. Si hay espacios disponibles, sugiere el espacio más cercano.
12. El usuario puede aceptar el espacio sugerido o elegir otro espacio disponible.
13. El sistema registra el movimiento de ingreso en la bitácora.
14. El sistema actualiza las estadísticas correspondientes al día.
15. El sistema muestra un mensaje de éxito con el espacio asignado.

#### Criterio para sugerir espacio

El espacio sugerido será el disponible con menor piso y menor número dentro del piso.

Ejemplo: si están disponibles `P1-E03`, `P2-E01` y `P1-E01`, se sugerirá `P1-E01`.

Este criterio es simple, explicable y fácil de implementar con ciclos y comparaciones.

#### Elección manual de espacio

Si el usuario no acepta el espacio sugerido, el sistema mostrará los espacios disponibles agrupados por piso. Luego solicitará el código del espacio.

El sistema validará que:

- el código exista;
- el espacio esté disponible;
- el código se haya ingresado con el formato esperado.

Si el dato es inválido, mostrará un mensaje de error y permitirá reintentar o volver al menú.

### 5.2 Registrar egreso

#### Objetivo

Registrar la salida de un vehículo, liberar el espacio ocupado y calcular el importe a pagar.

#### Flujo

1. El usuario selecciona `Registrar egreso`.
2. El sistema solicita el código del espacio ocupado.
3. El sistema valida que el código exista.
4. El sistema verifica que el espacio esté actualmente ocupado.
5. Si el espacio no está ocupado, informa el error y vuelve a solicitar el dato.
6. Si el espacio está ocupado, obtiene el movimiento de ingreso activo asociado a ese espacio.
7. El sistema calcula la permanencia entre la fecha/hora de ingreso y la fecha/hora actual.
8. El sistema calcula el importe a pagar.
9. Si el DNI pertenece a un cliente registrado, actualiza su total de horas acumuladas.
10. El sistema informa si el cliente tiene o tendrá descuento disponible para futuras visitas.
11. El sistema registra el movimiento de egreso en la bitácora.
12. El sistema actualiza las estadísticas de permanencia.
13. El sistema muestra un resumen de la operación.

#### Datos mostrados al finalizar el egreso

El resumen del egreso incluirá:

- código de espacio;
- DNI;
- fecha y hora de ingreso;
- fecha y hora de egreso;
- tiempo de permanencia;
- importe a pagar;
- información de cliente registrado, si corresponde.

#### Cálculo de permanencia

La permanencia se calculará en horas. Para evitar importes con decimales difíciles de explicar, se utilizará el criterio de cobrar por hora o fracción.

Ejemplos:

- 30 minutos se cobran como 1 hora;
- 1 hora y 10 minutos se cobran como 2 horas;
- 2 horas exactas se cobran como 2 horas.

Este cálculo puede implementarse de manera sencilla usando minutos totales y una división entera con redondeo hacia arriba.

#### Cálculo de importe

El importe se calculará con una tarifa fija por hora.

Ejemplo:

`importe = horas_a_cobrar * tarifa_por_hora`

La tarifa podrá definirse como una constante en el código, por ejemplo:

`TARIFA_POR_HORA = 1000`

#### Descuento para clientes registrados

Para mantener la lógica simple, el descuento será un beneficio de fidelización basado en horas acumuladas.

Regla propuesta:

- si el cliente registrado tiene 10 o más horas acumuladas antes del egreso, se aplica un 10% de descuento sobre el importe actual;
- luego del egreso, se suman las horas de permanencia al total acumulado;
- si el cliente alcanza las 10 horas después de esta operación, el sistema informa que tendrá descuento disponible en su próxima visita.

Esta regla evita la contradicción entre aplicar un descuento en la visita actual y, al mismo tiempo, informar un descuento para la próxima visita.

### 5.3 Registrar cliente

#### Objetivo

Crear un cliente registrado para acumular horas y acceder a beneficios.

#### Flujo

1. El usuario selecciona `Registrar cliente`.
2. El sistema solicita el DNI.
3. El sistema valida el formato del DNI.
4. El sistema verifica si el cliente ya existe.
5. Si ya existe, muestra un mensaje indicando que el cliente está registrado.
6. Si no existe, solicita el nombre.
7. El sistema valida que el nombre no esté vacío.
8. El sistema guarda el cliente con `total_horas` igual a 0.
9. El sistema muestra un mensaje de éxito.

#### Datos mínimos del cliente

Cada cliente registrado tendrá:

- DNI;
- nombre;
- total de horas acumuladas.

No se guardarán datos sensibles adicionales.

### 5.4 Consultar cliente

#### Objetivo

Mostrar la información almacenada de un cliente registrado.

#### Flujo

1. El usuario selecciona `Consultar cliente`.
2. El sistema solicita el DNI.
3. El sistema valida el formato del DNI.
4. El sistema busca el cliente.
5. Si existe, muestra sus datos.
6. Si no existe, informa que no está registrado y pregunta si desea registrarlo.
7. Si el usuario acepta, se inicia el flujo de registro de cliente.
8. Si el usuario no acepta, se vuelve al menú principal.

#### Datos mostrados

La consulta mostrará:

- DNI;
- nombre;
- total de horas acumuladas;
- estado del beneficio de descuento.

### 5.5 Consultar espacios disponibles

#### Objetivo

Mostrar qué espacios se encuentran libres.

#### Flujo

1. El usuario selecciona `Consultar espacios disponibles`.
2. El sistema reconstruye o consulta en memoria la ocupación actual.
3. El sistema muestra los espacios disponibles agrupados por piso.
4. El sistema muestra también la cantidad total de espacios libres y ocupados.

#### Formato sugerido

Ejemplo:

```text
Espacios disponibles

Piso 1: P1-E01, P1-E04, P1-E05
Piso 2: P2-E02, P2-E03
Piso 3: sin espacios disponibles

Libres: 5 | Ocupados: 10 | Total: 15
```

Este formato es más simple que una tabla con columnas variables y resulta más fácil de implementar y explicar.

### 5.6 Consultar estadísticas

#### Objetivo

Mostrar indicadores simples del funcionamiento del estacionamiento.

#### Menú de estadísticas

El sistema mostrará un menú anidado:

1. Porcentaje de ocupación actual
2. Cantidad de vehículos atendidos hoy
3. Tiempo promedio de permanencia
4. Volver al menú principal

#### Porcentaje de ocupación actual

Se calculará con la ocupación reconstruida desde los movimientos:

`porcentaje = espacios_ocupados * 100 / espacios_totales`

Se mostrará con uno o dos decimales.

#### Cantidad de vehículos atendidos hoy

Se considera vehículo atendido a cada ingreso registrado durante el día actual.

El valor se obtendrá desde las estadísticas diarias acumuladas. También podría calcularse recorriendo los movimientos del día, pero usar estadísticas acumuladas permite conservar datos ficticios iniciales y simplificar las consultas.

#### Tiempo promedio de permanencia

El sistema permitirá mostrar promedios:

- por mes;
- por día de la semana.

El promedio se calculará a partir de datos agregados:

`promedio = total_horas / cantidad_egresos`

Si la cantidad de egresos es 0, el sistema mostrará `Sin datos suficientes`.

## 6. Persistencia de datos

### 6.1 Carpeta de datos

Los archivos de datos se ubicarán en una carpeta del proyecto, por ejemplo:

```text
data/
  espacios.csv
  movimientos.csv
  clientes.json
  estadisticas.json
```

La carpeta `data/` contendrá datos reales para la ejecución del sistema, aunque los datos iniciales sean ficticios.

### 6.2 Archivo de espacios

#### Nombre

`data/espacios.csv`

#### Propósito

Define los espacios físicos existentes en el estacionamiento.

#### Tipo

CSV de solo lectura durante la ejecución normal.

#### Formato

```csv
codigo,piso,numero
P1-E01,1,1
P1-E02,1,2
P1-E03,1,3
P2-E01,2,1
P2-E02,2,2
```

#### Reglas

- `codigo` debe ser único;
- `piso` debe ser numérico;
- `numero` debe ser numérico;
- el archivo debe cargarse al iniciar el sistema;
- si el archivo está vacío o tiene datos inválidos, el sistema debe informar el problema.

### 6.3 Archivo de movimientos

#### Nombre

`data/movimientos.csv`

#### Propósito

Guardar la bitácora de ingresos y egresos.

#### Tipo

CSV de escritura por agregado. Cada nueva operación agrega una línea al final.

#### Formato

```csv
fecha_hora,codigo_espacio,dni,accion
2026-07-08 09:15:00,P1-E01,12345678,INGRESO
2026-07-08 11:40:00,P1-E01,12345678,EGRESO
```

#### Acciones válidas

- `INGRESO`
- `EGRESO`

#### Reglas

- no se debe registrar un ingreso en un espacio ocupado;
- no se debe registrar un egreso en un espacio libre;
- cada egreso debe corresponder al último ingreso activo del mismo espacio;
- el archivo no se borra al cerrar el programa;
- al iniciar, se recorre completo para reconstruir la ocupación actual.

### 6.4 Archivo de clientes

#### Nombre

`data/clientes.json`

#### Propósito

Guardar los clientes registrados y sus horas acumuladas.

#### Tipo

JSON. Se carga completo en memoria, se modifica el diccionario y se reescribe completo cuando cambia.

#### Formato

```json
{
  "12345678": {
    "nombre": "Juan Perez",
    "total_horas": 15
  },
  "87654321": {
    "nombre": "Maria Lopez",
    "total_horas": 4
  }
}
```

#### Reglas

- la clave principal será el DNI como texto;
- `nombre` no debe estar vacío;
- `total_horas` será un número entero;
- si el archivo no existe, puede crearse con `{}`;
- si el archivo existe pero está dañado, el sistema debe mostrar un mensaje de error comprensible.

### 6.5 Archivo de estadísticas

#### Nombre

`data/estadisticas.json`

#### Propósito

Guardar estadísticas acumuladas sin necesidad de cargar miles de movimientos ficticios.

#### Tipo

JSON con datos agregados.

#### Formato sugerido

```json
{
  "por_fecha": {
    "2026-07-08": {
      "ingresos": 12,
      "egresos": 10,
      "total_horas": 36
    }
  },
  "por_mes": {
    "2026-06": {
      "egresos": 180,
      "total_horas": 540
    },
    "2026-07": {
      "egresos": 10,
      "total_horas": 36
    }
  },
  "por_dia_semana": {
    "lunes": {
      "egresos": 40,
      "total_horas": 130
    },
    "martes": {
      "egresos": 38,
      "total_horas": 110
    },
    "miercoles": {
      "egresos": 42,
      "total_horas": 126
    },
    "jueves": {
      "egresos": 36,
      "total_horas": 100
    },
    "viernes": {
      "egresos": 55,
      "total_horas": 190
    },
    "sabado": {
      "egresos": 60,
      "total_horas": 210
    },
    "domingo": {
      "egresos": 22,
      "total_horas": 70
    }
  }
}
```

#### Justificación de este archivo

Este archivo resuelve la necesidad de mostrar estadísticas históricas sin crear miles de registros de movimientos.

En lugar de guardar cada estadía histórica ficticia, se guardan totales acumulados:

- cantidad de ingresos;
- cantidad de egresos;
- total de horas.

Con esos valores se pueden calcular promedios históricos de manera simple y realista.

#### Actualización de estadísticas

Cuando se registra un ingreso:

- se incrementa `ingresos` en `por_fecha` para la fecha actual.

Cuando se registra un egreso:

- se incrementa `egresos` en `por_fecha`;
- se suma la permanencia en horas a `total_horas` de `por_fecha`;
- se incrementa `egresos` en `por_mes`;
- se suma la permanencia en horas a `total_horas` de `por_mes`;
- se incrementa `egresos` en `por_dia_semana`;
- se suma la permanencia en horas a `total_horas` de `por_dia_semana`.

## 7. Datos en memoria

Durante la ejecución, el sistema trabajará con estructuras simples:

### Espacios

Lista de diccionarios:

```python
espacios = [
    {"codigo": "P1-E01", "piso": 1, "numero": 1},
    {"codigo": "P1-E02", "piso": 1, "numero": 2}
]
```

### Clientes

Diccionario por DNI:

```python
clientes = {
    "12345678": {"nombre": "Juan Perez", "total_horas": 15}
}
```

### Ocupación actual

Diccionario por código de espacio:

```python
ocupacion = {
    "P1-E01": {
        "dni": "12345678",
        "fecha_hora_ingreso": "2026-07-08 09:15:00"
    }
}
```

Si un código no aparece en `ocupacion`, se considera disponible.

## 8. Validaciones

### 8.1 Validaciones generales

El sistema debe validar:

- que las opciones de menú sean números dentro del rango esperado;
- que el DNI sea numérico y tenga longitud válida;
- que el nombre no esté vacío;
- que el código de espacio exista;
- que el espacio elegido esté disponible al registrar ingreso;
- que el espacio elegido esté ocupado al registrar egreso;
- que los archivos tengan un formato mínimo correcto.

### 8.2 Mensajes de error

Los mensajes deben ser claros y orientados a la acción.

Ejemplos:

- `Opción inválida. Ingrese un número del menú.`
- `DNI inválido. Debe ingresar solo números.`
- `El espacio ingresado no existe.`
- `El espacio seleccionado ya está ocupado.`
- `No hay espacios disponibles en este momento.`
- `No se puede registrar el egreso porque el espacio está libre.`

### 8.3 Reintentos y salida

Cuando el usuario ingrese un dato inválido, el sistema volverá a pedirlo.

Para no complicar la implementación con detección de teclas especiales, no se usará `Esc`. En su lugar, en las pantallas de carga se podrá aceptar `0` como opción para cancelar y volver al menú.

Ejemplo:

`Ingrese DNI del cliente o 0 para cancelar:`

Esta decisión es más simple para consola y más fácil de implementar en Python inicial.

## 9. Organización sugerida del código

El proyecto puede organizarse en módulos simples. Una estructura posible es:

```text
main.py
data/
  espacios.csv
  movimientos.csv
  clientes.json
  estadisticas.json
src/
  archivos.py
  clientes.py
  espacios.py
  movimientos.py
  estadisticas.py
  menus.py
  validaciones.py
```

Si se prefiere una estructura más simple, también se puede trabajar con menos archivos, siempre que el código quede modularizado en funciones.

## 10. Responsabilidades sugeridas por módulo

### 10.1 `main.py`

Responsabilidades:

- iniciar el programa;
- cargar datos iniciales;
- llamar al menú principal;
- coordinar el cierre.

### 10.2 `archivos.py`

Responsabilidades:

- leer archivos CSV;
- escribir líneas nuevas en CSV;
- leer JSON;
- guardar JSON.

### 10.3 `clientes.py`

Responsabilidades:

- registrar clientes;
- consultar clientes;
- actualizar horas acumuladas;
- calcular estado del descuento.

### 10.4 `espacios.py`

Responsabilidades:

- cargar espacios;
- buscar espacios por código;
- listar espacios disponibles;
- sugerir el espacio más cercano.

### 10.5 `movimientos.py`

Responsabilidades:

- registrar ingresos;
- registrar egresos;
- reconstruir ocupación actual;
- obtener el ingreso activo de un espacio.

### 10.6 `estadisticas.py`

Responsabilidades:

- cargar estadísticas;
- actualizar estadísticas por ingreso;
- actualizar estadísticas por egreso;
- calcular porcentaje de ocupación;
- calcular promedios.

### 10.7 `menus.py`

Responsabilidades:

- mostrar menú principal;
- mostrar menú de estadísticas;
- recibir opciones del usuario;
- coordinar llamadas a las operaciones.

### 10.8 `validaciones.py`

Responsabilidades:

- validar DNI;
- validar nombre;
- validar opciones de menú;
- validar códigos de espacio.

## 11. Casos de prueba mínimos

### 11.1 Caso válido de ingreso

1. Seleccionar `Registrar ingreso`.
2. Ingresar DNI válido.
3. Registrar cliente si no existe.
4. Aceptar espacio sugerido.
5. Verificar mensaje de éxito.
6. Consultar espacios disponibles y comprobar que el espacio ya no aparece como libre.

### 11.2 Caso válido de egreso

1. Seleccionar `Registrar egreso`.
2. Ingresar código de un espacio ocupado.
3. Verificar cálculo de permanencia.
4. Verificar cálculo de importe.
5. Confirmar que el espacio queda libre.
6. Confirmar actualización de estadísticas.

### 11.3 Caso de validación

1. Intentar ingresar un DNI con letras.
2. Verificar mensaje de error.
3. Intentar registrar egreso de un espacio libre.
4. Verificar mensaje de error.

### 11.4 Caso de estadísticas

1. Consultar porcentaje de ocupación.
2. Registrar un ingreso.
3. Consultar nuevamente el porcentaje.
4. Registrar un egreso.
5. Consultar promedio de permanencia.

## 12. Criterios de implementación

La implementación debe priorizar:

- código simple y legible;
- funciones con responsabilidades claras;
- uso de listas y diccionarios;
- ciclos para recorrer archivos y estructuras;
- condicionales para validaciones y decisiones;
- mensajes claros para el usuario;
- separación básica entre lógica, menús y archivos;
- comentarios breves solo cuando ayuden a comprender una parte no evidente.

No se buscará una solución avanzada. La calidad del sistema estará dada por su coherencia, funcionamiento correcto y comprensión por parte del equipo.

## 13. Decisiones finales de diseño

### 13.1 Uso de DNI y código de espacio

El DNI identifica al cliente y el código de espacio identifica la ocupación física. Para registrar egresos se usará el código de espacio, porque permite encontrar directamente el ingreso activo y evita ambigüedades.

### 13.2 Historial mediante bitácora

Los ingresos y egresos se guardarán como eventos en `movimientos.csv`. Esto permite reconstruir el estado actual sin mantener un archivo adicional de ocupación.

### 13.3 Estadísticas históricas agregadas

Los datos históricos ficticios se guardarán en `estadisticas.json` como totales acumulados. Esto permite mostrar promedios por mes y día de la semana sin generar miles de movimientos falsos.

### 13.4 Datos ficticios pero persistencia real

Los archivos iniciales podrán incluir datos ficticios para la demostración. A partir de la ejecución del sistema, toda operación nueva modificará realmente los archivos correspondientes.

### 13.5 Complejidad adecuada al nivel inicial

Se evitarán técnicas avanzadas innecesarias. La solución debe poder explicarse con conocimientos de algoritmos, estructuras de datos básicas, archivos, funciones, ciclos, condicionales y validaciones.
