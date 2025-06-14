import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Configuraciones generales
tecla_ancho, tecla_alto = 60, 60
espacio_entre_teclas = 10
inicio_y = 300
texto = ""
ultimo_tiempo = 0
retardo = 2.5  # segundos entre letras
ultimo_gesto = 0  # delay para gesto de borrar todo

# Teclas del teclado
teclado = [
    ['1','2','3','4','5','6','7','8','9','0'],
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M','SPA','DEL','ENT']
]

# Calcular posiciones
posiciones = []
for fila in range(len(teclado)):
    fila_pos = []
    total_teclas = len(teclado[fila])
    inicio_x = (1280 - (total_teclas * (tecla_ancho + espacio_entre_teclas))) // 2
    for col in range(total_teclas):
        x = inicio_x + col * (tecla_ancho + espacio_entre_teclas)
        y = inicio_y + fila * (tecla_alto + 10)
        fila_pos.append((x, y))
    posiciones.append(fila_pos)

# Función para dibujar el teclado
def dibujar_teclado(frame, seleccionada=None):
    for i, fila in enumerate(teclado):
        for j, tecla in enumerate(fila):
            x, y = posiciones[i][j]
            color = (200, 255, 255) if seleccionada == (i, j) else (102, 0, 0)
            cv2.rectangle(frame, (x, y), (x + tecla_ancho, y + tecla_alto), color, -1)
            cv2.rectangle(frame, (x, y), (x + tecla_ancho, y + tecla_alto), (255, 255, 255), 2)
            texto_dibujar = tecla if len(tecla) == 1 else tecla[:3]
            cv2.putText(frame, texto_dibujar, (x + 10, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255), 2)

# Función para detectar en qué tecla está el dedo
def detectar_tecla(x, y):
    for i, fila in enumerate(teclado):
        for j, tecla in enumerate(fila):
            tx, ty = posiciones[i][j]
            if tx < x < tx + tecla_ancho and ty < y < ty + tecla_alto:
                return (i, j)
    return None

# Iniciar cámara
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    seleccion = None

    if resultado.multi_hand_landmarks:
        for hand in resultado.multi_hand_landmarks:
            # Dedo índice
            dedo = hand.landmark[8]
            h, w, _ = frame.shape
            x = int(dedo.x * w)
            y = int(dedo.y * h)
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            seleccion = detectar_tecla(x, y)

            # Gesto: juntar índice y pulgar para borrar todo
            indice = hand.landmark[8]
            pulgar = hand.landmark[4]
            distancia = ((indice.x - pulgar.x) ** 2 + (indice.y - pulgar.y) ** 2) ** 0.5
            tiempo_actual = time.time()
            if distancia < 0.04 and tiempo_actual - ultimo_gesto > 2:
                print("🧼 Gesto detectado: BORRAR TODO")
                texto = ""
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                ultimo_gesto = tiempo_actual

    # Verificar si se presionó una tecla
    if seleccion:
        tiempo_actual = time.time()
        if tiempo_actual - ultimo_tiempo > retardo:
            i, j = seleccion
            tecla = teclado[i][j]
            if tecla == "SPA":
                texto += " "
                pyautogui.press("space")
            elif tecla == "DEL":
                texto = texto[:-1]
                pyautogui.press("backspace")
            elif tecla == "ENT":
                texto += "\n"
                pyautogui.press("enter")
            else:
                texto += tecla
                pyautogui.press(tecla.lower())
            ultimo_tiempo = tiempo_actual

    # Mostrar texto
    cv2.rectangle(frame, (50, 30), (1230, 110), (0, 0, 0), -1)
    cv2.putText(frame, texto[-60:], (60, 90), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (255, 255, 255), 3)

    # Dibujar teclado
    dibujar_teclado(frame, seleccion)

    cv2.imshow("Teclado con la Mano", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
