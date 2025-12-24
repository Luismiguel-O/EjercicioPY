JUEGO DE LA SERPIENTE (SNAKE)
OBJETIVO DEL PROYECTO
  Desarrollar el juego de la serpiente utilizando el lenguaje de programación Python y la librería curses, con el fin de fortalecer el aprendizaje de los fundamentos de la programación, 
  tales como el uso de estructuras de datos (listas, tuplas y diccionarios), funciones, control de flujo y manejo de errores, aplicando estos conceptos de manera práctica en un entorno interactivo y didáctico.
ALCANCE DEL PROYECTO 
  El proyecto comprende el desarrollo de un juego básico en Python con fines educativos y formativos, orientado a la aplicación práctica de los fundamentos de programación y al fortalecimiento de habilidades 
  técnicas y profesionales propias del área informática, limitándose a un entorno de ejecución en consola.

VERSION AUTONOMO 2

import curses
import random

def main(stdscr):
    # Inicializar pantalla
    curses.curs_set(0)  # Ocultar cursor
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)  # Crear ventana
    w.keypad(1)
    w.timeout(100)  # velocidad del juego (ms)

    # Posición inicial de la serpiente
    snake = [
        [sh//2, sw//2],
        [sh//2, sw//2 - 1],
        [sh//2, sw//2 - 2]
    ]

    # Comida inicial
    food = [random.randint(1, sh-2), random.randint(1, sw-2)]
    w.addch(food[0], food[1], curses.ACS_PI)

    # Dirección inicial (derecha)
    key = curses.KEY_RIGHT

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        # Calcular nueva posición de la cabeza
        head = snake[0].copy()

        if key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1

        # Game over si golpea pared
        if head[0] in [0, sh] or head[1] in [0, sw] or head in snake:
            msg = " GAME OVER "
            w.addstr(sh//2, sw//2 - len(msg)//2, msg)
            w.refresh()
            w.getch()
            break

        # Insertar nueva cabeza
        snake.insert(0, head)

        # Si come comida
        if snake[0] == food:
            food = [random.randint(1, sh-2), random.randint(1, sw-2)]
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Mover cuerpo (eliminar cola)
            tail = snake.pop()
            w.addch(tail[0], tail[1], " ")

        # Dibujar serpiente
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

if __name__ == "__main__":
    curses.wrapper(main)


VERSION MODIFICADA(FINAL)

import curses
import random

# -------------------------
# ESTRUCTURAS DE DATOS (diccionarios + tuplas + listas)
# -------------------------

CONFIG = {
    "speed_ms": 100,
    "snake_char": "█",   # funciona en macOS
    "food_char": "●",    # funciona en macOS
    "wall_char": "#",
    "game_over_msg": " GAME OVER ",
}

# Direcciones como diccionario: tecla -> (dy, dx) (tupla)
DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}

# Evitar reversa inmediata
OPPOSITE = {
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
    curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_RIGHT: curses.KEY_LEFT,
}


# -------------------------
# FUNCIONES (helpers)
# -------------------------

def safe_addch(w, y: int, x: int, ch) -> None:
    """Escribe un carácter sin romper el programa si el terminal es pequeño."""
    try:
        w.addch(y, x, ch)
    except curses.error:
        pass


def safe_addstr(w, y: int, x: int, s: str) -> None:
    """Escribe texto sin romper el programa si el terminal es pequeño."""
    try:
        w.addstr(y, x, s)
    except curses.error:
        pass


def init_window(stdscr) -> tuple:
    """Configura la pantalla y devuelve (window, sh, sw)."""
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(True)
    w.timeout(CONFIG["speed_ms"])
    return w, sh, sw


def create_initial_snake(sh: int, sw: int) -> list:
    """Crea la serpiente inicial como LISTA de TUPLAS (y, x)."""
    y = sh // 2
    x = sw // 2
    return [(y, x), (y, x - 1), (y, x - 2)]


def draw_border(w, sh: int, sw: int) -> None:
    """
    Dibuja el borde de forma compatible con macOS evitando errores en bordes.
    Ojo: en algunos terminales escribir en la última celda puede dar ERR.
    """
    wall = CONFIG["wall_char"]

    # Arriba y abajo (evita última columna en el loop)
    for x in range(sw - 1):
        safe_addch(w, 0, x, wall)
        safe_addch(w, sh - 1, x, wall)

    # Izquierda y derecha (evita última fila en el loop)
    for y in range(sh - 1):
        safe_addch(w, y, 0, wall)
        safe_addch(w, y, sw - 1, wall)


def random_food_position(sh: int, sw: int, snake: list) -> tuple:
    """Genera comida (tupla) que no caiga sobre la serpiente."""
    while True:
        pos = (random.randint(1, sh - 2), random.randint(1, sw - 2))
        if pos not in snake:
            return pos


def get_next_direction(w, current_key: int) -> int:
    """
    Lee teclado y decide la dirección:
    - Si no hay tecla (-1), mantiene la actual
    - Solo acepta flechas
    - No permite ir a la dirección opuesta inmediata
    """
    next_key = w.getch()
    if next_key == -1:
        return current_key

    if next_key in DIRECTIONS:
        if OPPOSITE.get(next_key) != current_key:
            return next_key

    return current_key


def compute_new_head(head: tuple, direction_key: int) -> tuple:
    """Calcula la nueva cabeza con (dy, dx)."""
    dy, dx = DIRECTIONS[direction_key]
    return (head[0] + dy, head[1] + dx)


def is_collision(new_head: tuple, snake: list, sh: int, sw: int) -> bool:
    """Colisión con pared o con el cuerpo."""
    y, x = new_head
    hit_wall = (y <= 0 or y >= sh - 1 or x <= 0 or x >= sw - 1)
    hit_self = new_head in snake
    return hit_wall or hit_self


def render(w, sh: int, sw: int, snake: list, food: tuple, state: dict) -> None:
    """Dibuja todo."""
    w.clear()
    draw_border(w, sh, sw)

    # HUD
    hud = f" Score: {state['score']}  Length: {len(snake)} "
    safe_addstr(w, 0, 2, hud)

    # Comida
    safe_addch(w, food[0], food[1], CONFIG["food_char"])

    # Serpiente (cabeza diferente al cuerpo)
    for i, (y, x) in enumerate(snake):
        ch = CONFIG["snake_char"] if i == 0 else "o"
        safe_addch(w, y, x, ch)

    w.refresh()


def show_game_over(w, sh: int, sw: int, state: dict) -> None:
    """Pantalla final."""
    msg = f"{CONFIG['game_over_msg']} Score: {state['score']} "
    safe_addstr(w, sh // 2, max(0, sw // 2 - len(msg) // 2), msg)
    safe_addstr(w, sh // 2 + 1, max(0, sw // 2 - 12), "Presiona una tecla...")
    w.refresh()
    w.getch()


# -------------------------
# LOOP PRINCIPAL
# -------------------------

def game_loop(stdscr) -> None:
    w, sh, sw = init_window(stdscr)

    # Evitar errores si el terminal es muy pequeño
    if sh < 10 or sw < 30:
        stdscr.clear()
        stdscr.addstr(0, 0, "Aumenta el tamaño de la terminal y vuelve a ejecutar.")
        stdscr.refresh()
        stdscr.getch()
        return

    # Estado del juego (diccionario)
    state = {"score": 0, "running": True}

    snake = create_initial_snake(sh, sw)  # lista de tuplas
    food = random_food_position(sh, sw, snake)
    direction = curses.KEY_RIGHT

    while state["running"]:
        render(w, sh, sw, snake, food, state)

        direction = get_next_direction(w, direction)
        new_head = compute_new_head(snake[0], direction)

        if is_collision(new_head, snake, sh, sw):
            state["running"] = False
            break

        # Mover: insertar nueva cabeza
        snake.insert(0, new_head)

        # Comer o avanzar
        if new_head == food:
            state["score"] += 10
            food = random_food_position(sh, sw, snake)
        else:
            snake.pop()

    show_game_over(w, sh, sw, state)


def main():
    curses.wrapper(game_loop)


if __name__ == "__main__":
    main()
