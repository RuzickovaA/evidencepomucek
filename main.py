import tkinter as tk
from tkinter import ttk
from database import create_tables, connect
from pomucky import PomuckyFrame
from studenti import StudentiFrame
from vypujcky import VypujckyFrame
from datetime import datetime

create_tables()

root = tk.Tk()
root.title("Evidence školních pomůcek")
root.geometry("1100x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

pomucky = PomuckyFrame(notebook)
studenti = StudentiFrame(notebook)
vypujcky = VypujckyFrame(notebook)

notebook.add(pomucky.frame, text="Pomůcky")
notebook.add(studenti.frame, text="Studenti")
notebook.add(vypujcky.frame, text="Aktuální výpůjčky")

def create_vypujcka():
    selected_p = pomucky.tree.selection()
    selected_s = studenti.tree.selection()
    if not selected_p or not selected_s:
        return
    pomucka_id = pomucky.tree.item(selected_p)["values"][0]
    student_id = studenti.tree.item(selected_s)["values"][0]
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vypujcky WHERE pomucka_id=? AND datum_vraceni IS NULL", (pomucka_id,))
    if cursor.fetchone():
        conn.close()
        return
    cursor.execute("INSERT INTO vypujcky (pomucka_id, student_id, datum_vypujcky) VALUES (?, ?, ?)",
                   (pomucka_id, student_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    vypujcky.refresh()

btn = ttk.Button(root, text="Potvrdit výpůjčku (vybraná pomůcka + student)", command=create_vypujcka)
btn.pack()

root.mainloop()
