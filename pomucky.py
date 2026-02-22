from tkinter import ttk, messagebox
from database import connect

class PomuckyFrame:

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        self.nazev = ttk.Entry(self.frame)
        self.typ = ttk.Entry(self.frame)
        self.stav = ttk.Entry(self.frame)

        self.nazev.pack()
        self.typ.pack()
        self.stav.pack()

        ttk.Button(self.frame, text="Přidat", command=self.add).pack()
        ttk.Button(self.frame, text="Upravit", command=self.update).pack()
        ttk.Button(self.frame, text="Smazat", command=self.delete).pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID","Nazev","Typ","Stav"), show="headings")
        for col in ("ID","Nazev","Typ","Stav"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pomucky")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def add(self):
        if not self.nazev.get() or not self.typ.get() or not self.stav.get():
            messagebox.showerror("Chyba", "Vyplňte všechna pole")
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pomucky (nazev, typ, stav) VALUES (?, ?, ?)",
                       (self.nazev.get(), self.typ.get(), self.stav.get()))
        conn.commit()
        conn.close()
        self.refresh()

    def update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Chyba", "Vyberte položku")
            return
        if not self.nazev.get() or not self.typ.get() or not self.stav.get():
            messagebox.showerror("Chyba", "Vyplňte všechna pole")
            return
        item = self.tree.item(selected)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE pomucky SET nazev=?, typ=?, stav=? WHERE id=?",
                       (self.nazev.get(), self.typ.get(), self.stav.get(), item["values"][0]))
        conn.commit()
        conn.close()
        self.refresh()

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Chyba", "Vyberte položku")
            return
        item = self.tree.item(selected)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pomucky WHERE id=?", (item["values"][0],))
        conn.commit()
        conn.close()
        self.refresh()
