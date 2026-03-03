import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

selected_tool = None
prev_selected_tool = None
color_idx = 0
grosor = 10
click_cooldown = 0
ui_buttons = []
drawing_start = None
HIDE = False
prev_HIDE = False


colores = [
    (0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0),
    (0, 255, 255), (255, 255, 0), (255, 0, 255),
    (0, 165, 255), (128, 0, 128), (180, 105, 255),
    (128, 128, 128), (200, 200, 200), (50, 50, 50),
    (19, 69, 139), (32, 0, 128), (208, 224, 64),
    (235, 206, 135), (127, 255, 0), (0, 215, 255)
]


def save_image(Lienzo):
    saved = False
    i = 0
    while saved == False:
        trying = cv2.imread("Lienzo"+str(i)+".jpg")
        if trying is None:
            cv2.imwrite("Lienzo"+str(i)+".jpg",Lienzo)
            saved = True
            print("SE HA GUARDADO")
        else:
            i += 1

def calc_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    ba = a - b
    bc = c - b
    cosang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosang = np.clip(cosang, -1, 1)
    return np.degrees(np.arccos(cosang))

def pulgar_extendido(hand):
    return calc_angle(hand.landmark[1], hand.landmark[2], hand.landmark[4]) > 150

def dedo_extendido(hand, id_base, id_middle, id_tip):
    return hand.landmark[id_tip].y < hand.landmark[id_base].y and hand.landmark[id_tip].y < hand.landmark[id_middle].y

def fingers_state(hand):
    return {
        "pulgar":   pulgar_extendido(hand),
        "indice":   dedo_extendido(hand, 5, 6, 8),
        "medio":    dedo_extendido(hand, 9, 10, 12),
        "anular":   dedo_extendido(hand, 13, 14, 16),
        "meñique":  dedo_extendido(hand, 17, 18, 20)
    }

def point_from_landmark(hand, w, h, id_tip=8):
    x = int(hand.landmark[id_tip].x * w)
    y = int(hand.landmark[id_tip].y * h)
    return max(0, min(x, w - 1)), max(0, min(y, h - 1))

def bucket_fill(Fondo, x, y, color, states):
    global selected_tool

    is_pointed=(
            states["indice"] and 
            not states["pulgar"] and 
            not states["medio"] and 
            not states["anular"] and 
            states["meñique"]
        )
    
    if is_pointed:
        gray = cv2.cvtColor(Fondo, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
        flood = mask.copy()
        h, w = flood.shape
        m = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(flood, m, (x, y), 255)
        Fondo[flood == 255] = color
        selected_tool = None

def setup_ui():
    global ui_buttons, HIDE
    ui_buttons = []
    margin = 10
    bw = 100
    x0 = margin
    y = margin
    if HIDE == False:
        ui_buttons.append({"rect": (x0, y, bw, 30), "label": "PINTAR", "action": "PINTAR"})
        ui_buttons.append({"rect": (x0+550, y, bw, 30), "label": "HIDEUI", "action": "HIDE"})
        ui_buttons.append({"rect": (x0+110, y, bw, 30), "label": "LINEA", "action": "LINEA"})
        y += 35
        ui_buttons.append({"rect": (x0, y, bw, 30), "label": "BORRAR", "action": "BORRAR"})
        ui_buttons.append({"rect": (x0+550, y, bw, 30), "label": "CLEAR", "action": "CLEAR"})
        ui_buttons.append({"rect": (x0+110, y, bw, 30), "label": "CIRCLE", "action": "CIRCULO"})
        y += 35
        ui_buttons.append({"rect": (x0, y, bw, 30), "label": "BUCKET", "action": "BUCKET"})
        ui_buttons.append({"rect": (x0+550, y, bw, 30), "label": "SAVE", "action": "SAVE"})
        ui_buttons.append({"rect": (x0+110, y, bw, 30), "label": "RECTAN", "action": "RECT"})
        y += 35
        ui_buttons.append({"rect": (x0, y, bw, 30), "label": "GROSOR+", "action": "GROSOR+"})
        y += 35
        ui_buttons.append({"rect": (x0, y, bw, 30), "label": "GROSOR-", "action": "GROSOR-"})
        y += 35
        cw = 30
        cols_per_col = 7
        cx = x0 + 10
        cy = y
        for i, col in enumerate(colores):
            if i != 0 and i % cols_per_col == 0:
                cx += cw + 10
                cy = y
            ui_buttons.append({"rect": (cx, cy, cw, cw), "label": f"C{i}", "action": "COLOR", "index": i})
            cy += cw + 6
    else:
        ui_buttons.append({"rect": (x0+550, y, bw, 30), "label": "UNHIDE", "action": "UNHIDE"})
    
def draw_ui(output):
    global ui_buttons, selected_tool, color_idx, grosor
    overlay = output.copy()
    for b in ui_buttons:
        x, y, w, h = b["rect"]
        if b["action"] == "COLOR":
            idx = b["index"]
            cv2.rectangle(overlay, (x, y), (x + w, y + h), colores[idx], -1)
            if idx == color_idx:
                cv2.rectangle(overlay, (x - 3, y - 3), (x + w + 3, y + h + 3), (123, 123, 123), 2)
        else:
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (50, 50, 50), -1)
            cv2.putText(overlay, b["label"], (x + 8, y + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            if selected_tool == b["action"]:
                cv2.rectangle(overlay, (x - 3, y - 3), (x + w + 3, y + h + 3), (0, 255, 0), 2)
    cv2.addWeighted(overlay, 0.9, output, 0.1, 0, output)
    return output

def handle_click(x, y, Fondo):
    global selected_tool, color_idx, grosor, drawing_start, HIDE, prev_selected_tool
    for b in ui_buttons:
        bx, by, bw, bh = b["rect"]
        if bx <= x <= bx + bw and by <= y <= by + bh:
            act = b["action"]
            if act == "HIDE":
                if prev_selected_tool not in ["HIDE", "UNHIDE"]:
                    selected_tool = prev_selected_tool
                HIDE = True
                break
            if act == "UNHIDE":
                HIDE = False
                selected_tool = prev_selected_tool
                break
            if act == "SAVE":
                save_image(Fondo)
                print("SE HA GUARDADO EL ARCHIVO")

            if act in ["PINTAR", "BORRAR", "BUCKET", "LINEA", "RECT", "CIRCULO"]:
                selected_tool = act
                drawing_start = None
            elif act == "CLEAR":
                Fondo[:] = 255
            elif act == "GROSOR+":
                if grosor < 50: grosor += 5
            elif act == "GROSOR-":
                if grosor > 5: grosor -= 5
            elif act == "COLOR":
                color_idx = b["index"]
            break

def draw_in(aux, x0, y0, ix, iy):
    global grosor, colores, color_idx, selected_tool
    if selected_tool == "LINEA":
        cv2.line(aux, (x0, y0), (ix, iy), colores[color_idx], grosor)
    elif selected_tool == "RECT":
        cv2.rectangle(aux, (x0, y0), (ix, iy), colores[color_idx], grosor)
    elif selected_tool == "CIRCULO":
        r = int(np.sqrt((ix - x0)**2 + (iy - y0)**2))
        cv2.circle(aux, (x0, y0), r, colores[color_idx], grosor)


def draw_shapes(Fondo, ix, iy, states, output):
    global drawing_start, selected_tool
    is_pointed=(
            states["indice"] and 
            not states["pulgar"] and 
            not states["medio"] and 
            not states["anular"] and 
            states["meñique"]
        )
    if drawing_start is None and is_pointed:
        drawing_start = (ix, iy)
        return
    elif drawing_start is not None:
        x0, y0 = drawing_start
        draw_in(output, x0, y0, ix, iy)
        if states["indice"] and not states["meñique"]:
            draw_in(Fondo, x0, y0, ix, iy)
            drawing_start = None

def gestos_ui(Fondo, hands, imagen):
    global click_cooldown, selected_tool, drawing_start, HIDE, prev_HIDE, prev_selected_tool
    h, w, _ = imagen.shape
    if not ui_buttons or prev_HIDE != HIDE:
        setup_ui()
        prev_HIDE = HIDE
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    results = hands.process(imagen_rgb)
    if click_cooldown > 0:
        click_cooldown -= 1
    output = Fondo.copy()
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        states = fingers_state(hand)
        ix, iy = point_from_landmark(hand, w, h)
        is_click = (
                states["indice"] and 
                states["pulgar"] and 
                not states["medio"] and 
                not states["anular"] and 
                not states["meñique"]
            )
        hold = sum(states.values()) == 5
        if sum(states.values()) == 0:
            selected_tool = None
            drawing_start = None
        if is_click and click_cooldown == 0:
            handle_click(ix, iy, Fondo)
            click_cooldown = 20
        if states["indice"] and not is_click and not hold and selected_tool:
            if selected_tool == "PINTAR":
                cv2.circle(Fondo, (ix, iy), grosor, colores[color_idx], -1)
            elif selected_tool == "BORRAR":
                cv2.circle(Fondo, (ix, iy), grosor, (255, 255, 255), -1)
            elif selected_tool == "BUCKET":
                bucket_fill(Fondo, ix, iy, colores[color_idx], states)
            elif selected_tool in ["LINEA", "RECT", "CIRCULO"]:
                draw_shapes(Fondo, ix, iy, states, output)
        mp_drawing.draw_landmarks(output, hand, mp_hands.HAND_CONNECTIONS)
        cv2.circle(output, (ix, iy), grosor, (0, 0, 255), 1)
    prev_selected_tool = selected_tool
    output = draw_ui(output)
    return output

def fondo():
    cap = cv2.VideoCapture(0)
    Fondo = np.ones((480, 640, 3), dtype=np.uint8) * 255
    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5) as hands:
        while cap.isOpened():
            ret, img = cap.read()
            cv2.imshow("Camara", img)
            if not ret:
                continue
            img = cv2.flip(img, 1)
            #Descomentar lineas si quiere usar una imagen que se carga en vez del fondo
            #Fondo = cv2.imread("Fondo.jpg")
            # h, w, _ = imagen.shape
            #if Fondo is not None:
                #Fondo = cv2.resize(Fondo, (h, w))
            #else:
                #print("No se pudo cargar la imagen")
            out = gestos_ui(Fondo, hands, img)
            cv2.imshow("Paint", out)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    cap.release()
    cv2.destroyAllWindows()

def main():
    fondo()

if __name__ == "__main__":
    main() 
