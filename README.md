# Snake con IA (Python 3.9)

Proyecto realizado para la materia **Inteligencia Artificial 2** en la **Universidad Mayor de San Simón**, **semestre 1/2019**.

El juego de **Snake** está programado con orientación a objetos y puede ejecutarse de dos maneras:
- **Modo Jugador:** jugar manualmente con las flechitas.
- **Modo IA:** una red neuronal toma decisiones en tiempo real mientras el juego se visualiza.

Se incluye un modelo previamente entrenado (`model2000.h5`) para observar el comportamiento de la IA.

---

## Ejecución

Crear y activar entorno virtual:

    py -m venv .venv
    .venv\Scripts\Activate.ps1

Instalar dependencias:

    pip install -r requirements.txt

### Modo IA
    python neural.py

### Modo Manual
    python snakeGame.py

---

## Vista previa

![IA jugando Snake](media/neural_snake.gif)

---
