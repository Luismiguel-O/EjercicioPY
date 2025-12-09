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
