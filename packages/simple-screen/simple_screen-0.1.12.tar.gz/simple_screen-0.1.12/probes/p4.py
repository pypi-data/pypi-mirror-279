import curses

def main(stdscr):
    curses.curs_set(1)  # Mostrar el cursor
    stdscr.nodelay(0)   # Bloquear esperando la entrada
    stdscr.timeout(-1)  # Esperar indefinidamente por la entrada

    stdscr.clear()
    stdscr.addstr(0, 0, "Texto normal")
    
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(1, 0, "Texto en negrita")
    stdscr.attroff(curses.A_BOLD)
    
    stdscr.attron(curses.A_UNDERLINE)
    stdscr.addstr(2, 0, "Texto subrayado")
    stdscr.attroff(curses.A_UNDERLINE)
    
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(3, 0, "Texto en video inverso")
    stdscr.attroff(curses.A_REVERSE)
    
    stdscr.attron(curses.A_BLINK)
    stdscr.addstr(4, 0, "Texto parpadeante")
    stdscr.attroff(curses.A_BLINK)
    
    stdscr.refresh()
    stdscr.getch()  # Esperar a que el usuario presione una tecla para salir

if __name__ == "__main__":
    curses.wrapper(main)
