# client_2.py
from socket import *
from threading import Thread
import tkinter as tk
import tkinter.scrolledtext as st
import sys, time
import RSA

def receive():
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Welcome! {NAME}\n", "system")
    chat_display.insert(tk.END, "You are online!\n", "system")
    chat_display.config(state=tk.DISABLED)
    while True:
        try:
            encrypted_msg = CLIENT.recv(BUFFER_SIZE).decode("utf8")
            msg = RSA.decrypt_string(encrypted_msg, private_key)
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, msg + "\n", "received")
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    if msg.strip():
        my_msg.set("")
        formatted_msg = f"{NAME}: {msg}"
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, formatted_msg + "\n", "sent")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)
        encrypted_msg = RSA.encrypt_string(formatted_msg, public_key_other)
        CLIENT.send(encrypted_msg.encode('utf8'))

def on_closing(event=None):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Going offline...\n", "system")
    chat_display.config(state=tk.DISABLED)
    time.sleep(2)
    CLIENT.close()
    root.quit()
    sys.exit()

root = tk.Tk()
root.title("RSA Encrypted Chat - Client 2")
root.geometry("400x550")
root.configure(bg="#1E1E1E")

chat_display = st.ScrolledText(root, height=20, width=50, wrap=tk.WORD, font=("Arial", 12), bg="#2C3E50", fg="#ECF0F1", padx=10, pady=5, borderwidth=0)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.tag_config("sent", foreground="#00A6FF", font=("Arial", 12, "bold"))
chat_display.tag_config("received", foreground="#2ECC71", font=("Arial", 12))
chat_display.tag_config("system", foreground="#95A5A6", font=("Arial", 11, "italic"))
chat_display.config(state=tk.DISABLED)

input_frame = tk.Frame(root, bg="#1E1E1E")
input_frame.pack(fill=tk.X, padx=10, pady=5)

my_msg = tk.StringVar()
entry_field = tk.Entry(input_frame, textvariable=my_msg, font=("Arial", 12), bg="#34495E", fg="#ECF0F1", insertbackground="white", relief=tk.FLAT)
entry_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
entry_field.bind("<Return>", send)

send_button = tk.Button(input_frame, text="Send", command=send, font=("Arial", 12, "bold"), bg="#00A6FF", fg="white", relief=tk.FLAT, padx=10, pady=5)
send_button.pack(side=tk.RIGHT)

root.protocol("WM_DELETE_WINDOW", on_closing)

BUFFER_SIZE = 1024
HOST = input('Enter host: ')
PORT = int(input('Enter port: '))
ADDRESS = (HOST, PORT)
NAME = input('Enter your name: ')

CLIENT = socket(AF_INET, SOCK_STREAM)
CLIENT.connect(ADDRESS)

public_key, private_key = RSA.key_generator()
msg = f"{public_key[0]}*{public_key[1]}"
CLIENT.send(bytes(msg, "utf8"))
m = CLIENT.recv(BUFFER_SIZE).decode('utf8')
public_key_other = [int(x) for x in m.split('*')]

receive_thread = Thread(target=receive)
receive_thread.start()
root.mainloop()