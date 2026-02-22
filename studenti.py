from tkinter import ttk, messagebox
from database import connect

class StudentiFrame:

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        self.jmeno = ttk.Entry(self.frame)
        self.prijmeni = ttk.Entry(self.frame)
        self.trida = ttk.Entry(self.frame)

        self.jmeno.pack()
        self.prijmeni.pack()
        self.trida.pack()

        ttk.Button(self.frame, text="Přidat", command=self.add).pack()
        ttk.Button(self.frame, text="Upravit", command=self.update).pack()
        ttk.Button(self.frame, text="Smazat", command=self.delete).pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID","Jmeno","Prijmeni","Trida"), show="headings")
        for col in ("ID","Jmeno","Prijmeni","Trida"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM studenti")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def add(self):
        if not self.jmeno.get() or not self.prijmeni.get() or not self.trida.get():
            messagebox.showerror("Chyba", "Vyplňte všechna pole")
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO studenti (jmeno, prijmeni, trida) VALUES (?, ?, ?)",
                       (self.jmeno.get(), self.prijmeni.get(), self.trida.get()))
        conn.commit()
        conn.close()
        self.refresh()

    def update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Chyba", "Vyberte položku")
            return
        if not self.jmeno.get() or not self.prijmeni.get() or not self.trida.get():
            messagebox.showerror("Chyba", "Vyplňte všechna pole")
            return
        item = self.tree.item(selected)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE studenti SET jmeno=?, prijmeni=?, trida=? WHERE id=?",
                       (self.jmeno.get(), self.prijmeni.get(), self.trida.get(), item["values"][0]))
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
        cursor.execute("DELETE FROM studenti WHERE id=?", (item["values"][0],))
        conn.commit()
        conn.close()
        self.refresh()
