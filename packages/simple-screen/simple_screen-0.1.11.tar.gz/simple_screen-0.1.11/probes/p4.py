import curses

# Definir colores
YELLOW = 1
DARK_BLUE = 2

def main(stdscr):
    # Configurar curses
    curses.curs_set(1)  # Mostrar el cursor
    curses.start_color()  # Iniciar el modo de colores
    curses.init_pair(YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(DARK_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    stdscr.nodelay(0)  # Bloquear esperando la entrada
    stdscr.timeout(100)  # Esperar 100 ms por la entrada

    input_str = ""
    buffer = []

    stdscr.clear()
    stdscr.attron(curses.color_pair(YELLOW))
    stdscr.addstr(0, 0, "Escribe algo (pulsa ESC para salir): ")
    stdscr.attroff(curses.color_pair(YELLOW))
    stdscr.refresh()

    while True:
        try:
            key = stdscr.get_wch()
            if key == '\x1b':  # ESC para salir
                break
            elif key == '\n':  # Enter para terminar la entrada
                buffer.append('\n')
            elif key in ('\b', '\x7f'):  # Backspace
                if buffer:
                    buffer.pop()
            else:
                buffer.append(key)
            
            # Convertir el buffer a una cadena
            input_str = ''.join(buffer)

            # Actualizar la pantalla
            stdscr.clear()
            stdscr.attron(curses.color_pair(YELLOW))
            stdscr.addstr(0, 0, "Escribe algo (pulsa ESC para salir): ")
            stdscr.attroff(curses.color_pair(YELLOW))
            stdscr.attron(curses.color_pair(DARK_BLUE))
            stdscr.addstr(1, 0, input_str)
            stdscr.attroff(curses.color_pair(DARK_BLUE))
            stdscr.refresh()

        except curses.error:
            pass  # Ignorar errores de curses cuando no hay entrada

if __name__ == "__main__":
    curses.wrapper(main)
