from tkinter import ttk, messagebox
from database import connect
from datetime import datetime

class VypujckyFrame:

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.refresh_combobox()
        self.refresh()

    def create_widgets(self):
        self.pomucka_cb = ttk.Combobox(self.frame, state="readonly")
        self.student_cb = ttk.Combobox(self.frame, state="readonly")
        self.pomucka_cb.pack()
        self.student_cb.pack()

        ttk.Button(self.frame, text="Vytvořit výpůjčku", command=self.create).pack()
        ttk.Button(self.frame, text="Vrátit pomůcku", command=self.return_item).pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID","Pomucka","Student","Datum"), show="headings")
        for col in ("ID","Pomucka","Student","Datum"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

    def refresh_combobox(self):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nazev FROM pomucky")
        pomucky = cursor.fetchall()
        self.pomucka_map = {f"{row[1]} (ID:{row[0]})": row[0] for row in pomucky}
        self.pomucka_cb["values"] = list(self.pomucka_map.keys())

        cursor.execute("SELECT id, jmeno || ' ' || prijmeni FROM studenti")
        studenti = cursor.fetchall()
        self.student_map = {f"{row[1]} (ID:{row[0]})": row[0] for row in studenti}
        self.student_cb["values"] = list(self.student_map.keys())

        conn.close()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT vypujcky.id, pomucky.nazev, studenti.jmeno || ' ' || studenti.prijmeni, datum_vypujcky
        FROM vypujcky
        JOIN pomucky ON vypujcky.pomucka_id = pomucky.id
        JOIN studenti ON vypujcky.student_id = studenti.id
        WHERE datum_vraceni IS NULL
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
        self.refresh_combobox()

    def create(self):
        if not self.pomucka_cb.get() or not self.student_cb.get():
            messagebox.showerror("Chyba", "Vyberte pomůcku i studenta")
            return

        pomucka_id = self.pomucka_map[self.pomucka_cb.get()]
        student_id = self.student_map[self.student_cb.get()]

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM vypujcky WHERE pomucka_id=? AND datum_vraceni IS NULL", (pomucka_id,))
        if cursor.fetchone():
            messagebox.showerror("Chyba", "Pomůcka je již vypůjčená")
            conn.close()
            return

        cursor.execute("INSERT INTO vypujcky (pomucka_id, student_id, datum_vypujcky) VALUES (?, ?, ?)",
                       (pomucka_id, student_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()
        self.refresh()

    def return_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Chyba", "Vyberte výpůjčku")
            return

        item = self.tree.item(selected)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE vypujcky SET datum_vraceni=? WHERE id=?",
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item["values"][0]))
        conn.commit()
        conn.close()
        self.refresh()
