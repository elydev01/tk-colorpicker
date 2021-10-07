import time, pickle, random, sys, tkinter as tk
from tkinter import ttk, colorchooser

from ttkwidgets.color import askcolor

from manager import rgb_to_hex, hex_to_rgb, get_absolut_path

HEX = True
RGB = False

FACE = True
FONT = False

FG = "BLACK"
BG = "WHITE"


class WidgetColor(tk.Frame):
    """
        Classe de recherche et/ou de modification de couleur en Hexadecimal ou RGB
    """

    def __init__(self, master=None, *args, **kw):
        super().__init__(master=master, bg="#ccc", *args, **kw)

        self.pack(expand=1, fill="both")

        self.master.resizable(0, 0)
        self.master.title("** PALETTE DE COULEUR **")
        self.master.geometry("+{}+{}".format(int(self.winfo_screenwidth() -590), 20))
        self.master.option_add("*Label*font" , 'Arial 16 bold')

        if (sys.platform.startswith('win')): 
            self.master.iconbitmap(get_absolut_path("ico.ico"))
        else:
            logo = tk.PhotoImage(file=get_absolut_path("ico.gif"))
            self.master.call('wm', 'iconphoto', self.master._w, logo)

        self.__proposition = ''

        with open(get_absolut_path("colorlist"), "rb") as file:
            self.colorList = pickle.load(file)

        frm = tk.LabelFrame(self)
        frm.pack(pady="10 5", padx=10)

        self.var_boitDeListe = tk.StringVar()

        # Creation de la boite de liste qui contiendra les couleurs
        combo = ttk.Combobox(frm, font="Arial 15", textvariable=self.var_boitDeListe, values=self.colorList, justify="center")
        combo.pack(expand=1, fill="x", padx=5, pady=5, side="left")
        self.var_boitDeListe.set(FG)
        self.var_boitDeListe.trace("w", self.changeColor)

        self.boutonPlus = tk.Button(frm, text="Plus de couleurs", font="Verdana 13", overrelief="groove",
                                                     relief="flat", bg="#ddd", command=self.plus_de_couleur)
        self.boutonPlus.pack(expand=1, fill="both", padx=5, pady=5, side="right")
        
        self.boutonPlus.bind("<Enter>", self.changeStyle)
        self.boutonPlus.bind("<Leave>", self.changeStyle)

        cd2 = tk.Frame(frm)
        cd2.pack(expand=1, fill="both", padx=5, pady=5, side="right")
        
        self.var_HexOrRgb = tk.BooleanVar()
        
        ttk.Radiobutton(cd2, text="HEX", value=1, variable=self.var_HexOrRgb).pack()
        ttk.Radiobutton(cd2, text="RGB", value=0, variable=self.var_HexOrRgb).pack()
        
        self.var_HexOrRgb.set(HEX)  # Par defaut le choix est (true <=> HEX)
        self.var_HexOrRgb.trace("w", self.convertion)

        cd = tk.Frame(frm)
        cd.pack(expand=1, fill="both", padx=5, pady=5, side="right")
        self.var = tk.BooleanVar()
        ttk.Radiobutton(cd, text="Face", value=1, variable=self.var).pack()
        ttk.Radiobutton(cd, text="Font", value=0, variable=self.var).pack()
        self.var.set(FACE)  # Par defaut le choix est le (true <=> FACE)
        self.var.trace("w", self.changeOption)

        ex_text = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n\na b c d e f g h i j k l m n o p q r s t u v w x " \
              "y z\n\n0 1 2 3 4 5 6 7 8 9\n\n ( { [ '. , ; : ! ? \" & € $ £ @ / % § # "

        # Cadre permetent la visualisation des differentes modifications
        self.echantillon = tk.Label(self, font="Arial 16 bold", text=ex_text, bg=BG, fg=FG, relief="groove", bd=2)
        self.echantillon.pack(pady=5, padx=10, ipadx=10, ipady=10)
        self.echantillon.bind("<1>", self.clickEchant)


        self.cadreApercu = tk.Frame(self, bd=1, relief="sunken")
        self.cadreApercu.pack(expand=1, fill="x", padx=10, pady="0 10")

        self.apercuCode = tk.Label(self.cadreApercu, font="Arial 16 bold", bg="#fff", fg="#888",
                                                    text="", relief="raised", bd=1, width=5)
        self.apercuCode.pack(ipady=10, side="left", ipadx=5)
        self.apercuCode.bind("<1>", self.clickApercu)

        self.apercuColor = tk.Label(self.cadreApercu, font="Arial 16 bold", relief="raised", bd=1)
        self.apercuColor.pack(expand=1, fill="x", ipady=10, side="left")
        self.apercuColor.bind("<1>", self.clickApercu)

        with open(get_absolut_path("colorfile"), "rb") as file:
            self.liste_couleurs = pickle.load(file)

        self.proposition()

    def changeColor(self, *_):
        try:
            color = self.var_boitDeListe.get()
            # si  FACE est resté coché...
            if self.var.get():
                self.echantillon.config(fg=color)
            else:
                self.echantillon.config(bg=color)
        except Exception:
            self.ConvertRGB(color)


    def ConvertRGB(self, color):
        listeValeur = []
        try:
            color = color.strip("()").split(",")
            for i in color:
                listeValeur.append(int(i))
            color = tuple(listeValeur)
            assert len(color) == 3
            valeur = rgb_to_hex(color)
            if valeur:
                if self.var.get():
                    self.echantillon.config(fg=valeur)
                else:
                    self.echantillon.config(bg=valeur)
        except Exception:
            pass

    def changeOption(self, *_):
        choix = self.var.get()
        if choix == FACE:
            c = self.echantillon["fg"]
        else:
            c = self.echantillon["bg"]
        self.var_boitDeListe.set(c.upper())
        self.convertion()

    def convertion(self, *_):
        color = self.var_boitDeListe.get()
        c = color
        if self.var_HexOrRgb.get() == RGB:

            valeur = hex_to_rgb(f'#{c[1]*2}{c[2]*2}{c[3]*2}') if len(c) == 4 else hex_to_rgb(c)

            if valeur:
                valeurs = list(valeur)
                valeur = f"({valeurs[0]},{valeurs[1]},{valeurs[2]})"
                self.var_boitDeListe.set(valeur)
        else:
            try:
                color = color.strip("()").split(",")
                listeValeur = [int(i) for i in color]
                color = tuple(listeValeur)
            except Exception:
                pass

            valeur = rgb_to_hex(color)
            if valeur:
                self.var_boitDeListe.set(valeur)


    def plus_de_couleur(self, alpha=False):
        if self.var.get():
            iniCol = self.echantillon["fg"]
        else:
            iniCol = self.echantillon["bg"]
        res = askcolor(iniCol, parent=self.master, title='Plus de couleurs', alpha=alpha)
        if res[0]:
            if self.var_HexOrRgb.get():
                couleur = res[1]
            else:
                couleur = str(res[0])
            self.var_boitDeListe.set(couleur[1])
            self.var_boitDeListe.set(couleur)


    def PlusDeCouleur(self):
        choix = self.var.get()
        if choix:
            iniCol = self.echantillon["fg"]
        else:
            iniCol = self.echantillon["bg"]
        couleur = colorchooser.askcolor(title="Plus de couleurs", initialcolor=iniCol)
        if couleur[0]:
            if self.var_HexOrRgb.get():
                couleur = couleur[1]
            else:
                couleur = str(couleur[0])
            self.var_boitDeListe.set(couleur[1])
            self.var_boitDeListe.set(couleur)


    def changeStyle(self, event=None):
        if str(event.type) == "Enter":
            self.boutonPlus.config(bg="#eee")
        elif str(event.type) == "Leave":
            self.boutonPlus.config(bg="#ddd")


    def proposition(self):
        choix = random.choice(self.liste_couleurs).upper()
        self.apercuCode.config(text=choix)
        self.apercuColor.config(bg=choix)
        self.__proposition = choix
        self.master.after(1500, self.proposition)


    def clickEchant(self, _):
        self.master.clipboard_clear()
        _fg, _bg = self.echantillon["fg"], self.echantillon["bg"]
        string = "({0} - {1})".format(_bg, _fg)
        self.master.clipboard_append(string)


    def clickApercu(self, _):
        self.var_boitDeListe.set(self.__proposition)



# https://github.com/mattrobenolt/colors.py