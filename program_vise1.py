import tkinter as tk
import math
import traceback

import numpy as np
import pandas as pd
import tkintertable as tkt
from tkinter import filedialog
import ellipsoid as el

class Program_vise1:

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

        #Funkcija za računanje prvog zadatka za više ulaznih podataka
        def racunaj1():

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
                global s
                global alfa1

                rastojanja = []
                f1 = np.zeros((len(podaci), 1))
                l1 = np.zeros((len(podaci), 1))
                s = np.zeros((len(podaci), 1))
                alfa1 = np.zeros((len(podaci), 1))

                f2a = np.zeros(len(podaci)) #stepeni
                f2b = np.zeros(len(podaci)) #minuti
                f2c = np.zeros(len(podaci)) #sekunde

                l2a = np.zeros(len(podaci))
                l2b = np.zeros(len(podaci))
                l2c = np.zeros(len(podaci))

                alfa22a = np.zeros(len(podaci))
                alfa22b = np.zeros(len(podaci))
                alfa22c = np.zeros(len(podaci))

                rezultati1 = pd.DataFrame({'Rastojanje': [],
                                           'f2[°]': [],
                                           "f2[']": [],
                                           'f2["]': [],
                                           'l2[°]': [],
                                           "l2[']": [],
                                           'l2["]': [],
                                           'A2[°]': [],
                                           "A2[']": [],
                                           'A2["]': []})

                for i in range(0, len(podaci)):
                    rastojanja.append(podaci[i][0])
                    f1[i][0] = math.radians(float(podaci[i][1]) + (float(podaci[i][2]) / 60) + (float(podaci[i][3]) / 3600))
                    l1[i][0] = math.radians(float(podaci[i][4]) + (float(podaci[i][5]) / 60) + (float(podaci[i][6]) / 3600))
                    s[i][0] = podaci[i][7]
                    alfa1[i][0] = math.radians(float(podaci[i][8]) + (float(podaci[i][9]) / 60) + (float(podaci[i][10]) / 3600))

                print('Učitavanje podataka izvršeno!')

            except Exception:
                traceback.print_exc()

            #Prilagođena računica za prvi geodetski zadatak
            for i in range(0, len(podaci)):

                beta1 = math.atan((1 - ellipsoid.f) * math.tan(f1[i][0]))
                sigma1 = math.atan(math.tan(beta1) / math.cos(alfa1[i][0]))
                beta_n = math.acos(math.cos(beta1) * math.sin(alfa1[i][0]))
                t = 1 / 4 * ellipsoid.e * math.pow(math.sin(beta_n), 2)
                v = 1 / 4 * ellipsoid.f * math.pow(math.sin(beta_n), 2)

                k1 = 1 + t * (1 - (t * (3 - t * (5 - 11 * t))) / 4)
                k2 = t * (1 - t * (2 - t * (37 - 94 * t) / 8))
                k3 = v * (1 + ellipsoid.f + math.pow(ellipsoid.f, 2) - v * (3 + 7 * ellipsoid.f - 13 * v))

                dSigma = 0.0
                dSs = 1.0
                raz = dSs - dSigma

                while raz > 0.000000000001:
                    sigma = s[i][0] / (k1 * ellipsoid.b) + dSigma
                    sigma_m = 2 * sigma1 + sigma
                    dSigma = k2 * math.sin(sigma) * (math.cos(sigma_m) + 1 / 4 * k2 * (
                            math.cos(sigma) * math.cos(2 * sigma_m) + 1 / 6 * k2 * (
                            1 + 2 * math.cos(2 * sigma)) * math.cos(3 * sigma_m)))
                    apsolut = dSs - dSigma
                    raz = abs(apsolut)
                    dSs = dSigma

                beta2 = math.atan(
                    (math.sin(beta1) * math.cos(sigma) + math.cos(beta1) * math.sin(sigma) * math.cos(
                        alfa1[i][0])) / math.sqrt(
                        1 - math.pow(math.sin(beta_n), 2) * math.pow(math.sin(sigma1 + sigma), 2)))
                f2 = math.atan(math.tan(beta2) / (1 - ellipsoid.f))

                dW = (1 - k3) * ellipsoid.f * math.cos(beta_n) * (sigma + k3 * math.sin(sigma) * (
                        math.cos(sigma_m) + k3 * math.cos(sigma) * math.cos(2 * sigma_m)))
                w = math.atan((math.sin(sigma) * math.sin(alfa1[i][0])) / (
                        math.cos(beta1) * math.cos(sigma) - math.sin(beta1) * math.sin(sigma) * math.cos(alfa1[i][0])))

                l2 = l1[i][0] + w + dW #l2 koji nije izlazni podatak - ne treba [i][0]

                #Provjera kvadranta za obrnuti azimut - alfa2
                P2 = math.cos(beta1) * math.sin(alfa1[i][0])
                Q2 = math.cos(beta1) * math.cos(sigma) * math.cos(alfa1[i][0]) - math.sin(beta1) * math.sin(sigma)

                if P2 >= 0 and Q2 > 0:
                    alfa2 = math.atan(P2 / Q2)
                elif P2 > 0 and Q2 <= 0:
                    alfa2 = math.atan(Q2 / P2) + math.radians(90)
                elif P2 <= 0 and Q2 < 0:
                    alfa2 = math.atan(P2 / Q2) + math.radians(180)
                else:
                    alfa2 = math.atan(Q2 / P2) + math.radians(270)

                alfa2 = math.degrees(alfa2) #alfa2 koji nije u izlaznom formatu - ne treba [i][0]
                f2_dec = math.degrees(f2) #važi isto kao i za alfa2
                l2_dec = math.degrees(l2) #važi isto kao i za alfa2

                mntf, secf = divmod(f2_dec * 3600, 60)
                degf, mntf = divmod(mntf, 60)

                f2a[i] = int(degf) #izlazni podaci - širina druge tačke - koji se smještaju u izlaznu matricu
                f2b[i] = int(mntf)
                f2c[i] = round(secf, 4)

                mntl, secl = divmod(l2_dec * 3600, 60)
                degl, mntl = divmod(mntl, 60)

                l2a[i] = int(degl) #izlazni podaci - dužina druge tačke - koji se smještaju u izlaznu matricu
                l2b[i] = int(mntl)
                l2c[i] = round(secl, 4)

                mnt22, sec22 = divmod(alfa2 * 3600, 60)
                deg22, mnt22 = divmod(mnt22, 60)

                alfa22a[i] = int(deg22) #izlazni podaci - obrnuti azimut - koji se smještaju u izlaznu matricu
                alfa22b[i] = int(mnt22)
                alfa22c[i] = round(sec22, 4)

                rezultati1['Rastojanje'] = rastojanja
                rezultati1['f2[°]'] = f2a.tolist()
                rezultati1["f2[']"] = f2b.tolist()
                rezultati1['f2["]'] = f2c.tolist()
                rezultati1['l2[°]'] = l2a.tolist()
                rezultati1["l2[']"] = l2b.tolist()
                rezultati1['l2["]'] = l2c.tolist()
                rezultati1['A2[°]'] = alfa22a.tolist()
                rezultati1["A2[']"] = alfa22b.tolist()
                rezultati1['A2["]'] = alfa22c.tolist()

            print(rezultati1)

            rezultati1.to_csv('rezultati1.csv', sep=',')
            rezultati_table.importCSV('rezultati1.csv')

            button_save.config(state=tk.NORMAL)

        #Podešavanje prozora, panela, dugmadi, labela,...
        self = tk.Tk()
        self.title("Prvi geodetski zadatak™")
        self.resizable(False, False)

        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        gornji_frame = tk.Frame(frame, width=860, bg='lightgray')
        gornji_frame.columnconfigure(3, weight=1)

        ulazni_podaci = tk.Label(gornji_frame, text="Excel (CSV) podaci", padx=205, pady=5)
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
        ulaz_table = tkt.TableCanvas(ulaz_frame, width=1000, bg='black', editable=True, rows=15, cols=10, pady=5)
        ulaz_table.model.columnlabels['1'] = 'Rastojanje'
        ulaz_table.model.columnlabels['2'] = 'f1 [°]'
        ulaz_table.model.columnlabels['3'] = "f1 [']"
        ulaz_table.model.columnlabels['4'] = 'f1 ["]'
        ulaz_table.model.columnlabels['5'] = 'l1 [°]'
        ulaz_table.model.columnlabels['6'] = "l1 [']"
        ulaz_table.model.columnlabels['7'] = 'l1 ["]'
        ulaz_table.model.columnlabels['8'] = 's [m]'
        ulaz_table.model.columnlabels['9'] = "alfa1 [°]"
        ulaz_table.model.columnlabels['10'] = "alfa1 [']"
        ulaz_table.model.columnlabels['11'] = 'alfa1 ["]'

        ulaz_table.createTableFrame()  #Konkretno "Excel like" tabela
        ulaz_table.addRows(num=5)  #Dodavanje 5 redova na tabelu sa ulaznim podacima
        ulaz_table.model.columnlabels['alignement'] = tk.CENTER

        #Definisanje tabele rezultata kao TableCanvas instance
        rezultati_table = tkt.TableCanvas(rezultati_frame, width=1000, height=200, rows=15, cols=10, pady=5)
        rezultati_table.model.columnlabels['1'] = 'Rastojanje'
        rezultati_table.model.columnlabels['2'] = 'f2 [°]'
        rezultati_table.model.columnlabels['3'] = "f2 [']"
        rezultati_table.model.columnlabels['4'] = 'f2 ["]'
        rezultati_table.model.columnlabels['5'] = 'l2 [°]'
        rezultati_table.model.columnlabels['6'] = "l2 [']"
        rezultati_table.model.columnlabels['7'] = 'l2 ["]'
        rezultati_table.model.columnlabels['8'] = 'a2 [°]'
        rezultati_table.model.columnlabels['9'] = "a2 [']"
        rezultati_table.model.columnlabels['10'] = 'a2 ["]'
        rezultati_table.createTableFrame()

        #Definisanje dugmeta za računanje
        button_load = tk.Button(donji_frame, text="Računaj", pady=5, padx=10,
                                command=racunaj1)
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


