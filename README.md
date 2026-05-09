# p3_msr

## Grafica Ruedas vs Tiempo

![grafica](imgs/Posicion_Ruedas.png)

## Grafica G-Parcial vs Tiempo

![grafica](imgs/Gasto_Parcial.png)

## Grafica Aceleracion vs Tiempo

![grafica](imgs/Aceleracion_IMU.png)


### Fase 1: Recogida y depósito del cubo verde (0s - 50s)

**Gasto Parcial:** Al inicio de la simulación (t = 0s a 25s), observamos una altísima actividad en la gráfica de gasto, con múltiples picos de esfuerzo que alcanzan valores cercanos a 1800. Esto corresponde a la primera planificación de MoveIt, el brazo SCARA sale de su estado de reposo, vence la inercia, se extiende para agarrar el cubo verde frente a él y realiza el esfuerzo necesario para levantarlo contra la gravedad y depositarlo en el compartimento superior del chasis.

**Posición de las ruedas:** Se mantiene en 0 radianes (líneas planas). El chasis está completamente estático y anclado al suelo para proporcionar una base firme durante la manipulación.

**IMU:** La aceleración en el eje Z (verde) se mantiene estable en torno a ~9.8 m/s² (fuerza de la gravedad). Los ejes X e Y muestran un ligero ruido, indicativo de las vibraciones mecánicas que el movimiento del pesado brazo SCARA transmite al chasis principal.

### Fase 2: Maniobras de reposicionamiento (75s - 150s)

**Gasto Parcial:** Cae prácticamente a cero. El brazo está en posición de reposo, consumiendo únicamente el par mínimo necesario para mantener su postura frente a la gravedad mientras la base móvil se desplaza.

**Posición de las ruedas:** A partir del segundo 75, las ruedas empiezan a moverse. Observamos desplazamientos escalonados donde las ruedas derechas (línea roja/naranja) toman valores positivos y las izquierdas (línea verde/azul) toman valores negativos. Esta divergencia en la rotación de los ejes indica que el robot está realizando maniobras de giro sobre su propio eje para reorientarse.

**IMU:** la IMU registra fuertes picos de aceleración en los ejes X e Y (aceleraciones y frenadas bruscas derivadas del control por teclado).

### Fase 3: Manipulación del cubo azul sobre el rojo (170s - 200s)

**Gasto Parcial:** Se registra el mayor pico de esfuerzo de toda la prueba, superando el valor de 2500 en la sumatoria absoluta. Se corresponde con agarrar el cubo azul, levantarlo para dejarlo sobre el cubo rojo.

**Posición de las ruedas:** Las ruedas permanecen sin movimiento, el robot se detuvo por completo para cojer el cubo azul. Luego vemos como vuelve a girar sobre su propio eje, para dejarlo sobre el cubo rojo.

**IMU:** En el segundo 175 destaca un pico de aceleración brutal en el eje Z que supera los 60 m/s². Se debe al choque de la pinza con el cubo azul. Despues vemos la IMU registra fuertes picos de aceleración en los ejes X e Y (aceleraciones y frenadas bruscas derivadas del control por teclado).

### Fase 4: Avance en línea recta de 10 metros (200s - 340s)

**Gasto Parcial:** Se mantiene muy bajo, presentando únicamente un ruido de fondo constante (pequeños picos menores a 200). El brazo en esta fase no hace nada.

**Posición de las ruedas:** Una vez soltado el cubo azul, vemos como va aumentando la posicion de las ruedas hasta llegar a los 10m.

**IMU:** Se observa un ruido oscilatorio constante y prolongado en todos los ejes (especialmente en Z). A diferencia del suelo liso perfecto, el entorno de urjc_excavation_world tiene un terreno con textura y ligeros desniveles; la IMU está registrando las vibraciones continuas del rodamiento sobre esta superficie irregular de tierra.
