import tkinter as tk
import math
import traceback

import numpy as np
import pandas as pd
import tkintertable as tkt
from tkinter import filedialog
import ellipsoid as el

class Program_vise2:

    global ellipsoid
    ellipsoid = el.Ellipsoid()
    ellipsoid.grs80()


    def __init__(self):

        #Funkcija koja vrši učitavanje CSV datoteke u tabele
        def loadfile():
            file = filedialog.askopenfilename()
            if file is None:
                return
            else:
                ulaz_table.importCSV(file)
                podaci1 = ulaz_table.model.getAllCells()
                if bool(podaci1) == False:
                    tk.messagebox.showinfo("Operacija", "Greška! Tabela je prazna!")
                    return

        #Funkcija koja vrši eksport dobijenih rezultata u CSV formatu
        def savefile():
            try:
                rezultati_table.exportTable()
                tk.messagebox.showinfo("Operacija", "Eksport uspješan")
            except:
                tk.messagebox.showinfo("Operacija", "Eksport neuspješan")

        #Funkcija koja ispituje da li je tip podatka float (vraća True ili False)
        def is_float_try(str):
            try:
                float(str)
                return True
            except ValueError:
                return False

        # Funkcija za računanje drugog zadatka za više ulaznih podataka
        def racunaj2():

            try:
                podaci = ulaz_table.model.getAllCells()

                for i in range(0, len(podaci)):
                    for j in range (1, 11):
                        if podaci[i][j] == "":
                            tk.messagebox.showinfo("Operacija", "Prazna vrijednost na redu " + str(i+1) + "\n i koloni " + str(j+1))
                            return
                        else:
                            if is_float_try(podaci[i][j]) == False:
                                tk.messagebox.showinfo("Operacija",
                                                       "Tekstualna vrijednost na redu " + str(i+1) + "\n i koloni " + str(j+1))
                                return

                global rastojanje
                global f1
                global l1
                global f2
                global l2

                rastojanja = []
                f1 = np.zeros((len(podaci), 1))
                l1 = np.zeros((len(podaci), 1))
                f2 = np.zeros((len(podaci), 1))
                l2 = np.zeros((len(podaci), 1))

                s = np.zeros((len(podaci)))

                alfa11a = np.zeros(len(podaci)) #stepeni
                alfa11b = np.zeros(len(podaci)) #minute
                alfa11c = np.zeros(len(podaci)) #sekunde

                alfa22a = np.zeros(len(podaci))
                alfa22b = np.zeros(len(podaci))
                alfa22c = np.zeros(len(podaci))

                rezultati2 = pd.DataFrame({'Rastojanje': [],
                                           'S[m]': [],
                                           'A1[°]': [],
                                            "A1[']": [],
                                           'A1["]': [],
                                           'A2[°]': [],
                                           "A2[']": [],
                                           'A2["]': []})

                for i in range(0, len(podaci)):
                    rastojanja.append(podaci[i][0])
                    f1[i][0] = math.radians(float(podaci[i][1]) + (float(podaci[i][2]) / 60) + (float(podaci[i][3]) / 3600))
                    l1[i][0] = math.radians(float(podaci[i][4]) + (float(podaci[i][5]) / 60) + (float(podaci[i][6]) / 3600))
                    f2[i][0] = math.radians(float(podaci[i][7]) + (float(podaci[i][8]) / 60) + (float(podaci[i][9]) / 3600))
                    l2[i][0] = math.radians(float(podaci[i][10]) + (float(podaci[i][11]) / 60) + (float(podaci[i][12]) / 3600))

                print('Učitavanje podataka izvršeno!')

            except Exception:
                traceback.print_exc()

            #Prilagođena računica za drugi geodetski zadatak
            for i in range(0, len(podaci)):

                beta1 = math.atan((1 - ellipsoid.f) * math.tan(f1[i][0]))
                beta2 = math.atan((1 - ellipsoid.f) * math.tan(f2[i][0]))
                dW = 0.0
                dWw = 1.0
                raz = dWw - dW

                while raz > 0.000000000001:
                    W = l2[i][0] - l1[i][0] + dW
                    sigma = math.atan(math.sqrt(math.pow(math.cos(beta2) * math.sin(W), 2) + math.pow(
                        math.cos(beta1) * math.sin(beta2) - math.sin(beta1) * math.cos(beta2) * math.cos(W), 2)) / (
                                              math.sin(beta1) * math.sin(beta2) + math.cos(beta1) * math.cos(
                                          beta2) * math.cos(W)))

                    beta_n = math.acos(math.cos(beta1) * math.cos(beta2) * math.sin(W) / math.sin(sigma))
                    sigma_m = math.acos(
                        math.cos(sigma) - 2 * math.sin(beta1) * math.sin(beta2) / math.pow(math.sin(beta_n), 2))
                    t = (ellipsoid.eprim * math.pow(math.sin(beta_n), 2)) / 4
                    v = (ellipsoid.f * math.pow(math.sin(beta_n), 2)) / 4
                    k3 = v * (1 + ellipsoid.f + math.pow(ellipsoid.f, 2) - v * (3 + 7 * ellipsoid.f - 13 * v))
                    dWw = (1 - k3) * ellipsoid.f * math.cos(beta_n) * (sigma + k3 * math.sin(sigma) * (
                            math.cos(sigma_m) + k3 * math.cos(sigma) * math.cos(2 * sigma_m)))
                    # promjenljiva za abs - ne moze izraz
                    apsolut = dWw - dW
                    raz = abs(apsolut)
                    dW = dWw

                k1 = 1 + t * (1 - (t * (3 - t * (5 - 11 * t))) / 4)
                k2 = t * (1 - t * (2 - t * (37 - 94 * t) / 8))
                dSig = k2 * math.sin(sigma) * (math.cos(sigma_m) + k2 * (1 / 4) * (
                        math.cos(sigma) * math.cos(2 * sigma_m) + k2 * (1 / 6) * (
                        1 + 2 * math.cos(2 * sigma) * math.cos(3 * sigma_m))))
                s[i] = k1 * ellipsoid.b * (sigma - dSig)

                #Provjera kvadranta za pravi azimut - alfa1
                P1 = math.cos(beta2) * math.sin(W)
                Q1 = math.cos(beta1) * math.sin(beta2) - math.sin(beta1) * math.cos(beta2) * math.cos(W)

                if P1 >= 0 and Q1 > 0:
                    alfa1 = math.atan(P1 / Q1)
                elif P1 > 0 and Q1 <= 0:
                    alfa1 = math.atan(Q1 / P1) + math.radians(90)
                elif P1 <= 0 and Q1 < 0:
                    alfa1 = math.atan(P1 / Q1) + math.radians(180)
                else:
                    alfa1 = math.atan(Q1 / P1) + math.radians(270)

                #Provjera kvadranta za obrnuti azimut - alfa2
                P2 = math.cos(beta1) * math.sin(W)
                Q2 = math.cos(beta1) * math.sin(beta2) * math.cos(W) - math.sin(beta1) * math.cos(beta2)
                if P2 >= 0 and Q2 > 0:
                    alfa2 = math.atan(P2 / Q2)
                elif P2 > 0 and Q2 <= 0:
                    alfa2 = math.atan(Q2 / P2) + math.radians(90)
                elif P2 <= 0 and Q2 < 0:
                    alfa2 = math.atan(P2 / Q2) + math.radians(180)
                else:
                    alfa2 = math.atan(Q2 / P2) + math.radians(270)

                alfa1 = math.degrees(alfa1)
                alfa2 = math.degrees(alfa2)

                mnt1, sec1 = divmod(alfa1 * 3600, 60)
                deg1, mnt1 = divmod(mnt1, 60)
                alfa11a[i] = int(deg1)
                alfa11b[i] = int(mnt1)
                alfa11c[i] = round(sec1, 4)

                mnt22, sec22 = divmod(alfa2 * 3600, 60)
                deg22, mnt22 = divmod(mnt22, 60)
                alfa22a[i] = int(deg22)
                alfa22b[i] = int(mnt22)
                alfa22c[i] = round(sec22, 4)

                rezultati2['Rastojanje'] = rastojanja
                rezultati2['S[m]'] = s.tolist()
                rezultati2['A1[°]'] = alfa11a.tolist()
                rezultati2["A1[']"] = alfa11b.tolist()
                rezultati2['A1["]'] = alfa11c.tolist()
                rezultati2['A2[°]'] = alfa22a.tolist()
                rezultati2["A2[']"] = alfa22b.tolist()
                rezultati2['A2["]'] = alfa22c.tolist()

            print(rezultati2)

            rezultati2.to_csv('rezultati2.csv', sep=',')
            rezultati_table.importCSV('rezultati2.csv')

            button_save.config(state=tk.NORMAL)

        #Podešavanje prozora, panela, dugmadi, labela,...
        self = tk.Tk()
        self.title("Drugi geodetski zadatak™")
        self.resizable(False, False)

        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        gornji_frame = tk.Frame(frame, width=860, bg='lightgray')
        gornji_frame.columnconfigure(3, weight=1)

        ulazni_podaci = tk.Label(gornji_frame, text="CSV podaci", padx=205, pady=5)
        ulazni_podaci.grid(row=0, column=0, columnspan=2)

        ulaz_frame = tk.Frame(frame, width=430, pady=5)
        rezultati_frame = tk.Frame(frame, width=430, pady=5)
        labela_frame = tk.Frame(frame, width=860, bg='lightgrey')
        donji_frame = tk.Frame(frame , height = 50, width = 860, pady = 5)

        labela_rez = tk.Label(labela_frame, text="Rezultati", padx=205, pady=5)
        labela_rez.grid(row=0, column=0, columnspan=2)

        gornji_frame.grid(row=0, column=0, columnspan=3)
        ulaz_frame.grid(row=1, column=0)
        labela_frame.grid(row=2, column=0)
        rezultati_frame.grid(row=3, column=0)
        donji_frame.grid(row=4, column=0, columnspan=3, pady=5)

        #Definisanje ulazne tabele kao TableCanvas instance
        ulaz_table = tkt.TableCanvas(ulaz_frame, width=1000, height=200, rows=15, cols=10, pady=5, editable = True)
        ulaz_table.model.columnlabels['1'] = 'Rastojanje'
        ulaz_table.model.columnlabels['2'] = 'f1 [°]'
        ulaz_table.model.columnlabels['3'] = "f1 [']"
        ulaz_table.model.columnlabels['4'] = 'f1 ["]'
        ulaz_table.model.columnlabels['5'] = 'l1 [°]'
        ulaz_table.model.columnlabels['6'] = "l1 [']"
        ulaz_table.model.columnlabels['7'] = 'l1 ["]'
        ulaz_table.model.columnlabels['8'] = 'f2 [°]'
        ulaz_table.model.columnlabels['9'] = "f2 [']"
        ulaz_table.model.columnlabels['10'] = 'f2 ["]'
        ulaz_table.model.columnlabels['11'] = 'l2 [°]'
        ulaz_table.model.columnlabels['12'] = "l2 [']"
        ulaz_table.model.columnlabels['13'] = 'l2 ["]'

        ulaz_table.createTableFrame()  #Konkretno "Excel like" tabela
        ulaz_table.addRows(num=5) #Dodavanje 5 redova na tabelu sa ulaznim podacima
        ulaz_table.model.columnlabels['alignement'] = tk.CENTER

        #Definisanje tabele rezultata kao TableCanvas instance
        rezultati_table = tkt.TableCanvas(rezultati_frame, width=1000, height=200, rows=15, cols=8, pady=5)
        rezultati_table.model.columnlabels['1'] = 'Rastojanje'
        rezultati_table.model.columnlabels['2'] = 's'
        rezultati_table.model.columnlabels['3'] = 'a1 [°]'
        rezultati_table.model.columnlabels['4'] = "a1 [']"
        rezultati_table.model.columnlabels['5'] = 'a1 ["]'
        rezultati_table.model.columnlabels['6'] = 'a2 [°]'
        rezultati_table.model.columnlabels['7'] = "a2 [']"
        rezultati_table.model.columnlabels['8'] = 'a2 ["]'
        rezultati_table.createTableFrame()

        # Definisanje dugmeta za računanje
        button_load = tk.Button(donji_frame, text="Računaj", pady=5, padx=10,
                                command=racunaj2)
        button_load.grid(row=0, column=0)

        #Kreiranje liste sa ponuđenim elipsoidima
        OptionList = [
            "GRS80",
            "Bessel1841",
            "Hayford",
            "WGS84",
            "Krasowski"
        ]

        def callback(*args):
            i = OptionList.index(variable.get())
            if i == 0:
                ellipsoid.grs80()
                active_elip()
            elif i == 1:
                ellipsoid.bessel1841()
                active_elip()
            elif i == 2:
                ellipsoid.hajford()
                active_elip()
            elif i == 3:
                ellipsoid.wgs84()
                active_elip()
            elif i == 4:
                ellipsoid.krasovski()
                active_elip()

        #Za ispis informacija o trenutno odabranom elipsoidu
        def active_elip():
            inform["text"] = "Elipsoid: " + ellipsoid.name

            if ellipsoid.name == "GRS80":
                variable.set(OptionList[0])
            elif ellipsoid.name == "Bessel 1841":
                variable.set(OptionList[1])
            elif ellipsoid.name == "Hayford":
                variable.set(OptionList[2])
            elif ellipsoid.name == "WGS84":
                variable.set(OptionList[3])
            elif ellipsoid.name == "Krasowski":
                variable.set(OptionList[4])

        variable = tk.StringVar()
        variable.set(OptionList[0])
        variable.trace("w", callback)

        opt = tk.OptionMenu(donji_frame, variable, *OptionList)
        opt.grid(row=0, column=1, padx=10)

        #Podešavanje dugmadi i menija
        inform = tk.Button(donji_frame, state=tk.NORMAL, text="Elipsoid: " + ellipsoid.name, command=ellipsoid.elip_window)
        inform.grid(row=0, column=2, padx=10)

        cust = tk.Button(donji_frame, state=tk.NORMAL, text="Unesi elipsoid", command=ellipsoid.custom)
        cust.grid(row=0, column=3, padx=10)

        button_save = tk.Button(donji_frame, text="Eksport rezultata", pady=5, state=tk.DISABLED, command=savefile)
        button_save.grid(row=0, column=4)

        menu_import = tk.Menu(self)
        filemenu = tk.Menu(menu_import, tearoff=0)
        filemenu.add_cascade(label="Učitaj podatke", command=loadfile)
        filemenu.add_cascade(label="Izađi", command=exit)

        menu_import.add_cascade(label="File", menu=filemenu)

        self.config(menu=menu_import)

        loadfile()
        return self.mainloop()




