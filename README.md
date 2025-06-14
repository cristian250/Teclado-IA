Teclado Virtual con la Mano – Proyecto de IA
Este proyecto es un teclado virtual controlado con la mano. En lugar de usar el mouse o el teclado físico, solo necesitas moverte frente a la cámara y usar tu dedo para seleccionar letras. ¡También puedes borrar todo juntando el dedo índice con el pulgar!

¿Qué hace este proyecto?
- Abre una ventana con un teclado grande en pantalla.
- Detecta tu mano con la cámara web.
- Sigue el dedo índice y selecciona letras por las que pasas.
- Tiene un retardo para evitar que se escriban muchas letras por error.
- Puedes borrar todo el texto con un gesto simple (índice + pulgar).
- Es ideal para personas con problemas de movilidad o simplemente para experimentar con visión por computadora.

¿Qué usé?
- Python 3
- OpenCV (para la cámara y mostrar el teclado)
- Mediapipe (para detectar la mano y el dedo)
- PyAutoGUI (para simular que se presionan teclas reales)

Cómo usarlo
1. Asegúrate de tener Python instalado.
2. Instala las dependencias (solo una vez):
  pip install opencv-python mediapipe pyautogui
3. Abre tu terminal en la carpeta donde guardaste el archivo teclado_ia.py.
4. Ejecuta el programa:
    python teclado_ia.py
5. La cámara se abrirá. Usa tu dedo índice para moverte por el teclado.
6. Si juntas el dedo índice y el pulgar, se borra todo el texto.
