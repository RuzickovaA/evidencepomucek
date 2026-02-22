from tkinter import ttk, messagebox
from database import connect
from datetime import datetime

class VypujckyFrame:

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        ttk.Button(self.frame, text="Vytvořit výpůjčku", command=self.create).pack()
        ttk.Button(self.frame, text="Vrátit pomůcku", command=self.return_item).pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID","Pomucka","Student","Datum"), show="headings")
        for col in ("ID","Pomucka","Student","Datum"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

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

    def create(self):
        messagebox.showinfo("Info", "Pro vytvoření výpůjčky vyberte studenta a pomůcku v jejich záložkách")

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
