# Evidence školních pomůcek

## Popis aplikace
Aplikace pro evidenci školních pomůcek, studentů a jejich výpůjček.

## Funkce aplikace
: Evidence pomůcek (přidání, úprava, smazání, zobrazení)
: Evidence studentů (přidání, úprava, smazání, zobrazení)
: Vytváření výpůjček
: Vrácení pomůcky
: Kontrola dostupnosti pomůcky
: Přehled aktuálně vypůjčených položek

## Použité technologie
: Python 3
: SQLite
: Tkinter
: ttk.Treeview

## Databázová struktura

pomucky (id, nazev, typ, stav)
studenti (id, jmeno, prijmeni, trida)
vypujcky (id, pomucka_id, student_id, datum_vypujcky, datum_vraceni)

## Spuštění aplikace

1. Nainstalujte Python 3
2. Otevřete terminál ve složce projektu
3. Spusťte příkaz:
   python main.py

## Git

git init
git add .
git commit -m "Projekt Evidence pomucek"
git branch -M main
git remote add origin https://github.com/RuzickovaA/evidencepomucek.git
git push -u origin main
