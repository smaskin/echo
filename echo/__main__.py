import server
import client_gui
import client_console
from helpers import console

if __name__ == "__main__":
    console_params = console.args()
    if console_params.mode == 'server':
        server.main()
    elif console_params.mode == 'gui_client':
        client_gui.main()
    else:
        client_console.main()
