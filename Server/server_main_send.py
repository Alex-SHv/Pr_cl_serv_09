import socket
import threading
import tkinter as tk
from tkinter import ttk


class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - Clients Monitor")

        self.tree = ttk.Treeview(root, columns=("IP", "Status"), show='headings')
        self.tree.heading("IP", text="IP Адрес")
        self.tree.heading("Status", text="Статус")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.clients = {}

        self.server_thread = threading.Thread(target=self.start_socket_server, daemon=True)
        self.server_thread.start()

    def start_socket_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 4000))
        server.listen(5)

        while True:
            client_sock, addr = server.accept()
            client_id = f"{addr[0]}:{addr[1]}"

            self.update_status(client_id, "В сети (Online)")

            threading.Thread(target=self.monitor_client, args=(client_sock, client_id), daemon=True).start()

    def monitor_client(self, sock, client_id):
        try:
            while True:
                if not sock.recv(1024):
                    break
        except:
            pass
        finally:
            self.update_status(client_id, "Оффлайн")
            sock.close()

    def _safe_update(self, client_id, status):
        if client_id in self.clients:
            self.tree.item(self.clients[client_id], values=(client_id, status))
        else:
            item_id = self.tree.insert("", tk.END, values=(client_id, status))
            self.clients[client_id] = item_id

    def update_status(self, ip, status):
        self.root.after(0, self._safe_update, ip, status)

    def _safe_update(self, ip, status):
        if ip in self.clients:
            self.tree.item(self.clients[ip], values=(ip, status))
        else:
            item_id = self.tree.insert("", tk.END, values=(ip, status))
            self.clients[ip] = item_id


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()