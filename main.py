import tkinter as tk
import ellipsoid as el
import math
import program_vise2
import program_vise1

def program(self):

    #Naredba za gašenje programa
    def exit():
        self.destroy()

    #Podešavanje GUI-ja za prvi geodetski zadatak
    def prvigeodzad():
        global PrviisClicked
        PrviisClicked = True
        global DrugiisClicked
        DrugiisClicked = False

        orig_color = prvi_zad.cget("background")
        prvi_zad.config(bg='lightgreen')
        drugi_zad.config(bg=orig_color)

        #Podešavanje boje slova za ulazne (zelena boja) i izlazne parametre (crvena boja)
        labela1.config(fg='green')
        labela2.config(fg='green')
        labela3.config(fg='green')
        labela4.config(fg='red')

        labela5.config(fg='green')
        labela6.config(fg='green')
        labela7.config(fg='red')

        calculate.config(state=tk.NORMAL)

    #Podešavanje GUI-ja za drugi geodetski zadatak
    def drugigeodzad():
        global PrviisClicked
        global DrugiisClicked
        DrugiisClicked = True
        PrviisClicked = False

        orig_color = drugi_zad.cget("background")

        drugi_zad.config(bg='lightgreen')
        prvi_zad.config(bg=orig_color)

        labela1.config(fg='green')
        labela2.config(fg='green')
        labela3.config(fg='green')
        labela4.config(fg='green')

        labela5.config(fg='red')
        labela6.config(fg='red')
        labela7.config(fg='red')

        calculate.config(state=tk.NORMAL)
    def is_float_try(str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    #Funkcija za konverziju iz forme [° ' "] u decimalni zapis uz postavljanje adekvatnih uslova
    def dms2dd(degrees, minutes, seconds):

        if is_float_try(degrees) == False:
            raise ValueError("Nije unijeta ispravna vrijednost stepena geografske širine!")
            return
        elif is_float_try(minutes) == False:
            raise ValueError("Nije unijeta ispravna vrijednost minuta geografske širine!")
            return
        elif is_float_try(seconds) == False:
            raise ValueError("Nije unijeta ispravna vrijednost sekundi geografske širine!")
            return

        degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
        if degrees < -90 or degrees > 90:
            raise ValueError('Geografska širina \nmora biti u rasponu od \n-90 do 90 stepeni!')
        elif minutes >= 60:
            raise ValueError('Minuti moraju \nbiti manji od 60!')
        elif seconds >= 60:
            raise ValueError('Sekundi moraju \nbiti manji od 60!')
        dd = math.radians(abs(degrees) + minutes / 60 + seconds / 3600)
        return dd if degrees >= 0 else -dd

    def dms2dd2(degrees, minutes, seconds):  # geog. duzina
        if is_float_try(degrees) == False:
            raise ValueError("Nije unijeta ispravna vrijednost stepena geografske dužine!")
            return
        elif is_float_try(minutes) == False:
            raise ValueError("Nije unijeta ispravna vrijednost minuta geografske dužine!")
            return
        elif is_float_try(seconds) == False:
            raise ValueError("Nije unijeta ispravna vrijednost sekundi geografske dužine!")
            return

        degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
        if degrees < -180 or degrees > 180:
            raise ValueError('Geografska dužina \nmora biti u rasponu od \n-180 do 180 stepeni!')
        elif minutes >= 60:
            raise ValueError('Minuti moraju \nbiti manji od 60!')
        elif seconds >= 60:
            raise ValueError('Sekundi moraju \nbiti manji od 60!')
        dd = math.radians(abs(degrees) + minutes / 60 + seconds / 3600)
        return dd if degrees >= 0 else -dd

    def dms2dd3(degrees, minutes, seconds):  # azimut

        if is_float_try(degrees) == False:
            raise ValueError("Nije unijeta ispravna vrijednost stepena pravog azimuta!")
            return
        elif is_float_try(minutes) == False:
            raise ValueError("Nije unijeta ispravna vrijednost minuta pravog azimuta!")
            return
        elif is_float_try(seconds) == False:
            raise ValueError("Nije unijeta ispravna vrijednost sekundi pravog azimuta!")
            return

        degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
        if minutes >= 60:
            raise ValueError('Minuti moraju \nbiti manji od 60!')
        elif seconds >= 60:
            raise ValueError('Sekundi moraju \nbiti manji od 60!')
        dd = math.radians(abs(degrees) + minutes / 60 + seconds / 3600)
        return dd if degrees >= 0 else -dd

        #Računica vezana za dugme "Računaj" - oba geodetska zadatka
    def calculate():

        if PrviisClicked:
            unos_fi2_step.delete(0, 'end')
            unos_fi2_min.delete(0, 'end')
            unos_fi2_sek.delete(0, 'end')

            unos_l2_step.delete(0, 'end')
            unos_l2_min.delete(0, 'end')
            unos_l2_sek.delete(0, 'end')

            unos_obaz_step.delete(0, 'end')
            unos_obaz_min.delete(0, 'end')
            unos_obaz_sek.delete(0, 'end')
            ispis_label.config(text='')

            #Konverzija unijetih vrijednosti i hvatanje greške, ukoliko postoji
            try:
                f1 = dms2dd(unos_fi1_step.get(), unos_fi1_min.get(), unos_fi1_sek.get())
                l1 = dms2dd2(unos_l1_step.get(), unos_l1_min.get(), unos_l1_sek.get())
                if is_float_try(unos_s.get()) == False:
                    ispis_label.config(text="Tekstualna vrijednost u polju za geodetsku liniju!", fg='#f00')
                    unos_s.focus()
                    return
                else:
                    s = float(unos_s.get())

                alfa1 = dms2dd3(unos_az_step.get(), unos_az_min.get(), unos_az_sek.get())

            except ValueError as the_error:
                ispis_label.config(text=the_error, fg='#f00')

            beta1 = math.atan((1 - ellipsoid.f) * math.tan(f1))
            sigma1 = math.atan(math.tan(beta1) / math.cos(alfa1))
            beta_n = math.acos(math.cos(beta1) * math.sin(alfa1))
            t = 1 / 4 * ellipsoid.e * math.pow(math.sin(beta_n), 2)
            v = 1 / 4 * ellipsoid.f * math.pow(math.sin(beta_n), 2)

            k1 = 1 + t * (1 - (t * (3 - t * (5 - 11 * t))) / 4)
            k2 = t * (1 - t * (2 - t * (37 - 94 * t) / 8))
            k3 = v * (1 + ellipsoid.f + math.pow(ellipsoid.f, 2) - v * (3 + 7 * ellipsoid.f - 13 * v))

            dSigma = 0.0
            dSs = 1.0
            raz = dSs - dSigma

            while raz > 0.000000000001:
                sigma = s / (k1 * ellipsoid.b) + dSigma
                sigma_m = 2 * sigma1 + sigma
                dSigma = k2 * math.sin(sigma) * (math.cos(sigma_m) + 1 / 4 * k2 * (
                            math.cos(sigma) * math.cos(2 * sigma_m) + 1 / 6 * k2 * (
                                1 + 2 * math.cos(2 * sigma)) * math.cos(3 * sigma_m)))
                apsolut = dSs - dSigma
                raz = abs(apsolut)
                dSs = dSigma

            beta2 = math.atan(
                (math.sin(beta1) * math.cos(sigma) + math.cos(beta1) * math.sin(sigma) * math.cos(alfa1)) / math.sqrt(
                    1 - math.pow(math.sin(beta_n), 2) * math.pow(math.sin(sigma1 + sigma), 2)))
            f2 = math.atan(math.tan(beta2) / (1 - ellipsoid.f))

            dW = (1 - k3) * ellipsoid.f * math.cos(beta_n) * (sigma + k3 * math.sin(sigma) * (
                        math.cos(sigma_m) + k3 * math.cos(sigma) * math.cos(2 * sigma_m)))
            w = math.atan((math.sin(sigma) * math.sin(alfa1)) / (
                        math.cos(beta1) * math.cos(sigma) - math.sin(beta1) * math.sin(sigma) * math.cos(alfa1)))

            l2 = l1 + w + dW

            #Provjera kvadranta za obrnuti azimut - alfa2
            P2 = math.cos(beta1) * math.sin(alfa1)
            Q2 = math.cos(beta1) * math.cos(sigma) * math.cos(alfa1) - math.sin(beta1) * math.sin(sigma)

            if P2 >= 0 and Q2 > 0:
                alfa2 = math.atan(P2 / Q2)
            elif P2 > 0 and Q2 <= 0:
                alfa2 = math.atan(Q2 / P2) + math.radians(90)
            elif P2 <= 0 and Q2 < 0:
                alfa2 = math.atan(P2 / Q2) + math.radians(180)
            else:
                alfa2 = math.atan(Q2 / P2) + math.radians(270)

            #Konverzija iz radijana u decimalni zapis
            alfa2 = math.degrees(alfa2)
            f22 = math.degrees(f2)
            l22 = math.degrees(l2)

            #Konverzija iz decimalnog zapisa u zapis [° ' "]
            mntf, secf = divmod(f22 * 3600, 60)
            degf, mntf = divmod(mntf, 60)
            f22 = int(degf), int(mntf), round(secf, 4)

            #Proslijeđivanje rješenja polju - ispis rezultata u GUI-ju
            unos_fi2_step.insert(0, f22[0])
            unos_fi2_min.insert(0, f22[1])
            unos_fi2_sek.insert(0, f22[2])

            mntl, secl = divmod(l22 * 3600, 60)
            degl, mntl = divmod(mntl, 60)
            l22 = int(degl), int(mntl), round(secl, 4)

            unos_l2_step.insert(0, l22[0])
            unos_l2_min.insert(0, l22[1])
            unos_l2_sek.insert(0, l22[2])

            mnt22, sec22 = divmod(alfa2 * 3600, 60)
            deg22, mnt22 = divmod(mnt22, 60)
            alfa22 = int(deg22), int(mnt22), round(sec22, 4)

            unos_obaz_step.insert(0, alfa22[0])
            unos_obaz_min.insert(0, alfa22[1])
            unos_obaz_sek.insert(0, alfa22[2])

        elif DrugiisClicked:

            unos_s.delete(0, 'end')

            unos_az_step.delete(0, 'end')
            unos_az_min.delete(0, 'end')
            unos_az_sek.delete(0, 'end')

            unos_obaz_step.delete(0, 'end')
            unos_obaz_min.delete(0, 'end')
            unos_obaz_sek.delete(0, 'end')
            ispis_label.config(text='')

            #Konverzija unijetih vrijednosti i hvatanje greške, ukoliko postoji
            try:
                f1 = dms2dd(unos_fi1_step.get(), unos_fi1_min.get(), unos_fi1_sek.get())
                l1 = dms2dd2(unos_l1_step.get(), unos_l1_min.get(), unos_l1_sek.get())
                f2 = dms2dd(unos_fi2_step.get(), unos_fi2_min.get(), unos_fi2_sek.get())
                l2 = dms2dd2(unos_l2_step.get(), unos_l2_min.get(), unos_l2_sek.get())

            except ValueError as the_error:

                ispis_label.config(text=the_error, fg='#f00')

            beta1 = math.atan((1 - ellipsoid.f) * math.tan(f1))
            beta2 = math.atan((1 - ellipsoid.f) * math.tan(f2))
            dW = 0.0
            dWw = 1.0
            raz = dWw - dW

            while raz > 0.000000000001:
                W = l2 - l1 + dW
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

                apsolut = dWw - dW #Pomoćna promjenljiva za apsolutnu vrijednost
                raz = abs(apsolut)
                dW = dWw

            k1 = 1 + t * (1 - (t * (3 - t * (5 - 11 * t))) / 4)
            k2 = t * (1 - t * (2 - t * (37 - 94 * t) / 8))
            dSig = k2 * math.sin(sigma) * (math.cos(sigma_m) + k2 * (1 / 4) * (
                        math.cos(sigma) * math.cos(2 * sigma_m) + k2 * (1 / 6) * (
                            1 + 2 * math.cos(2 * sigma) * math.cos(3 * sigma_m))))
            s = k1 * ellipsoid.b * (sigma - dSig)

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

            #Konverzija iz radijana u decimalni zapis
            alfa1 = math.degrees(alfa1)
            alfa2 = math.degrees(alfa2)

            #Konverzija iz decimalnog zapisa u zapis [° ' "]
            mnt1, sec1 = divmod(alfa1 * 3600, 60)
            deg1, mnt1 = divmod(mnt1, 60)
            alfa11 = int(deg1), int(mnt1), round(sec1, 4)

            mnt22, sec22 = divmod(alfa2 * 3600, 60)
            deg22, mnt22 = divmod(mnt22, 60)
            alfa22 = int(deg22), int(mnt22), round(sec22, 4)

            #Proslijeđivanje rješenja polju - ispis rezultata u GUI-ju
            unos_s.insert(0, round(s, 4))
            unos_az_step.insert(0, alfa11[0])
            unos_az_min.insert(0, alfa11[1])
            unos_az_sek.insert(0, alfa11[2])

            unos_obaz_step.insert(0, alfa22[0])
            unos_obaz_min.insert(0, alfa22[1])
            unos_obaz_sek.insert(0, alfa22[2])

    #Dugme "Resetuj" - briše sva polja
    def reset():
        unos_fi1_step.delete(0, 'end')
        unos_fi1_min.delete(0, 'end')
        unos_fi1_sek.delete(0, 'end')

        unos_fi2_step.delete(0, 'end')
        unos_fi2_min.delete(0, 'end')
        unos_fi2_sek.delete(0, 'end')

        unos_l1_step.delete(0, 'end')
        unos_l1_min.delete(0, 'end')
        unos_l1_sek.delete(0, 'end')

        unos_l2_step.delete(0, 'end')
        unos_l2_min.delete(0, 'end')
        unos_l2_sek.delete(0, 'end')

        unos_s.delete(0, 'end')

        unos_az_step.delete(0, 'end')
        unos_az_min.delete(0, 'end')
        unos_az_sek.delete(0, 'end')

        unos_obaz_step.delete(0, 'end')
        unos_obaz_min.delete(0, 'end')
        unos_obaz_sek.delete(0, 'end')


    #Kreiranje GUI funkcionalnosti - paneli, dugmad, labele, polja, padajući meniji
    self.title("Viša geodezija™")
    #Panel u koji se skladište ostali paneli
    frame = tk.Frame(self)
    frame.pack(fill=tk.BOTH, expand=True)

    panel_1 = tk.Frame(frame)
    panel_1.grid(row=0, column=0, pady = 10)
    panel_2 = tk.Frame(frame)
    panel_2.grid(row=1, column=0, pady = 10)
    panel_3 = tk.Frame(frame)
    panel_3.grid(row=2, column=0, pady = 10)
    panel_4 = tk.Frame(frame)
    panel_4.grid(row=3, column=0, pady = 10)

    prvi_zad = tk.Button(panel_1, text="I geodetski zadatak", pady=5, command=prvigeodzad)
    prvi_zad.grid(row=0, column=0)
    drugi_zad = tk.Button(panel_1, text="II geodetski zadatak", pady=5, command=drugigeodzad)
    drugi_zad.grid(row=0, column=3)

    labela1 = tk.Label(panel_2, text='Prva tačka')
    labela2 = tk.Label(panel_2, text='''Geografska širina [° ' "]''')
    labela3 = tk.Label(panel_2, text='''Geografska dužina [° ' "]''')
    labela4 = tk.Label(panel_2, text='Druga tačka')

    labela1.grid(row=1, column=1)
    labela2.grid(row=2, column=0)
    labela3.grid(row=3, column=0)
    labela4.grid(row=1, column=2)

    panel_fi1 = tk.Frame(panel_2)
    panel_fi1.grid(row = 2, column = 1)
    unos_fi1_step = tk.Entry(panel_fi1, state=tk.NORMAL, width = 5)
    unos_fi1_step.grid(row = 0, column = 0)
    unos_fi1_min = tk.Entry(panel_fi1, state=tk.NORMAL, width = 5)
    unos_fi1_min.grid(row = 0, column = 1, padx = 5)
    unos_fi1_sek = tk.Entry(panel_fi1, state=tk.NORMAL, width=7)
    unos_fi1_sek.grid(row=0, column=2)

    panel_fi2 = tk.Frame(panel_2)
    panel_fi2.grid(row=2, column=2, padx= 5)
    unos_fi2_step = tk.Entry(panel_fi2, state=tk.NORMAL, width=5)
    unos_fi2_step.grid(row=0, column=0)
    unos_fi2_min = tk.Entry(panel_fi2, state=tk.NORMAL, width=5)
    unos_fi2_min.grid(row=0, column=1, padx=5)
    unos_fi2_sek = tk.Entry(panel_fi2, state=tk.NORMAL, width=7)
    unos_fi2_sek.grid(row=0, column=2)

    panel_l1 = tk.Frame(panel_2)
    panel_l1.grid(row=3, column=1, padx=5)
    unos_l1_step = tk.Entry(panel_l1, state=tk.NORMAL, width=5)
    unos_l1_step.grid(row=0, column=0)
    unos_l1_min = tk.Entry(panel_l1, state=tk.NORMAL, width=5)
    unos_l1_min.grid(row=0, column=1, padx=5)
    unos_l1_sek = tk.Entry(panel_l1, state=tk.NORMAL, width=7)
    unos_l1_sek.grid(row=0, column=2)

    panel_l2 = tk.Frame(panel_2)
    panel_l2.grid(row=3, column=2, padx=5)
    unos_l2_step = tk.Entry(panel_l2, state=tk.NORMAL, width=5)
    unos_l2_step.grid(row=0, column=0)
    unos_l2_min = tk.Entry(panel_l2, state=tk.NORMAL, width=5)
    unos_l2_min.grid(row=0, column=1, padx=5)
    unos_l2_sek = tk.Entry(panel_l2, state=tk.NORMAL, width=7)
    unos_l2_sek.grid(row=0, column=2)

    labela5 = tk.Label(panel_3, text='Geodetska linija [m]')
    labela5.grid(row=0, column=0)
    labela6 = tk.Label(panel_3, text='''Pravi azimut [° ' "]''')
    labela7 = tk.Label(panel_3, text='''Obrnuti azimut [° ' "]''')
    labela6.grid(row=1, column=0)
    labela7.grid(row=2, column=0)

    unos_s = tk.Entry(panel_3, state = tk.NORMAL, width=22)
    unos_s.grid(row =0, column = 1)

    panel_az = tk.Frame(panel_3)
    panel_az.grid(row=1, column=1, padx=5)
    unos_az_step = tk.Entry(panel_az, state=tk.NORMAL, width=5)
    unos_az_step.grid(row=0, column=0, padx=5, pady = 5)
    unos_az_min = tk.Entry(panel_az, state=tk.NORMAL, width=5)
    unos_az_min.grid(row=0, column=1, padx=5, pady = 5)
    unos_az_sek = tk.Entry(panel_az, state=tk.NORMAL, width=7)
    unos_az_sek.grid(row=0, column=2, padx=5, pady = 5)

    panel_obaz = tk.Frame(panel_3)
    panel_obaz.grid(row=2, column=1, padx=5)
    unos_obaz_step = tk.Entry(panel_obaz, state=tk.NORMAL, width=5)
    unos_obaz_step.grid(row=0, column=0, padx=5, pady = 5)
    unos_obaz_min = tk.Entry(panel_obaz, state=tk.NORMAL, width=5)
    unos_obaz_min.grid(row=0, column=1, padx=5, pady = 5)
    unos_obaz_sek = tk.Entry(panel_obaz, state=tk.NORMAL, width=7)
    unos_obaz_sek.grid(row=0, column=2, padx=5, pady = 5)

    ispis_label = tk.Label(panel_4, justify=tk.CENTER)
    ispis_label.grid(row = 0, column = 0, columnspan = 3, sticky=tk.S)


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
        if i==0:
            ellipsoid.grs80()
            active_elip()
        elif i==1:
            ellipsoid.bessel1841()
            active_elip()
        elif i==2:
            ellipsoid.hajford()
            active_elip()
        elif i==3:
            ellipsoid.wgs84()
            active_elip()
        elif i==4:
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

    opt = tk.OptionMenu(panel_4, variable, *OptionList)
    opt.grid(row=1, column=2, padx=10)

    #Zadavanje komandi dugmadima i njihovo gridovanje
    inform = tk.Button(panel_4, state=tk.NORMAL, text="Elipsoid: " + ellipsoid.name, command=ellipsoid.elip_window)
    inform.grid(row=1, column=1, padx=10)
    
    cust = tk.Button(panel_4, state=tk.NORMAL, text="Unesi elipsoid", command=ellipsoid.custom)
    cust.grid(row=1, column=0, padx=10)

    labela8 = tk.Label(panel_4, text='Osnovni račun:')
    labela8.grid(row=1, column=0, pady=(100, 10))

    calculate = tk.Button(panel_4, state=tk.DISABLED, text="Računaj", command=calculate)
    calculate.grid(row=1, column=1, pady=(100,10))

    reset = tk.Button(panel_4, state=tk.NORMAL, text="Resetuj", command=reset)
    reset.grid(row=1, column=2, pady=(100, 10), padx=10)

    labela9 = tk.Label(panel_4, text='Unos više podataka:')
    labela9.grid(row=2, column=0, pady=10)

    ucitaj_vise = tk.Button(panel_4, state=tk.NORMAL, text="I zadatak", command=program_vise1.Program_vise1)
    ucitaj_vise.grid(row=2, column=1, pady=10, padx=10)

    ucitaj_vise2 = tk.Button(panel_4, state=tk.NORMAL, text="II zadatak", command=program_vise2.Program_vise2)
    ucitaj_vise2.grid(row=2, column=2, pady=10, padx=10)

    #Kreiranje i podešavanje menija
    menubar = tk.Menu(self)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_cascade(label="Izađi", command=exit)

    elipsoidmenu = tk.Menu(menubar, tearoff=0)
    elipsoidmenu.add_cascade(label="GRS80", command=lambda: [ellipsoid.grs80(), active_elip()])
    elipsoidmenu.add_cascade(label="Bessel 1841", command=lambda: [ellipsoid.bessel1841(), active_elip()])
    elipsoidmenu.add_cascade(label="Hayford", command=lambda: [ellipsoid.hajford(), active_elip()])
    elipsoidmenu.add_cascade(label="WGS84", command=lambda: [ellipsoid.wgs84(), active_elip()])
    elipsoidmenu.add_cascade(label="Krasowski", command=lambda: [ellipsoid.krasovski(), active_elip()])
    elipsoidmenu.add_cascade(label="Proizvoljni elipsoid...", command=lambda: [ellipsoid.custom(), active_elip()])
    elipsoidmenu.add_cascade(label="Informacije", command=ellipsoid.elip_window)

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Elipsoid", menu=elipsoidmenu)

    self.config(menu=menubar)
    self.mainloop()

ellipsoid = el.Ellipsoid()
ellipsoid.grs80()

window = tk.Tk()
window.resizable(False, False)
program(window)
