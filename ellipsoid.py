import tkinter as tk
import math

class Ellipsoid:

    name = None
    a = 0
    b = 0
    f = 0
    e = 0
    eprim = 0

    def __init__(self):  #Podrazumijevani konstruktor
        self.name = None
        self.a = 0
        self.b = 0
        self.f = 0
        self.e = 0
        self.eprim = 0

    def __init__1(self, name, a, b, f, e, eprim):  #Konstruktor sa ulaznim parametrima
        self.name = name
        self.a = a
        self.b = b
        self.f = f
        self.e = e
        self.eprim = eprim
        print(self.__str__())

    #Predefinisani, postojeći elipsoidi koji se nalaze u listi za izbor
    def grs80(self):  #GRS80
        self.__init__1('GRS80', 6378137.000, 6356752.3141, 0.00335281068184, 0.00669438002290, 0.00673949677548)

    def bessel1841(self):  #Bessel1841
        self.__init__1('Bessel 1841', 6377397.155, 6356078.963, 0.00334277321346, 0.00667437229375, 0.00671921886196)

    def hajford(self):
        self.__init__1('Hayford', 6378388.000, 6336911.94613, 0.003367003367, 0.006722670022, 0.006768170197)

    def wgs84(self):
        self.__init__1('WGS84', 6378137.000, 6356752.314245, 0.0033528106647, 0.00669437999014, 0.00673949674228)

    def krasovski(self):
        self.__init__1('Krasowski', 6378245.000, 6356863.01877, 0.003352329869, 0.006693421623, 0.006738525415)

    #Definisanje prozora za ispis parametara elipsoida
    def elip_window(self):
        ellipsoid_window = tk.Tk()
        ellipsoid_window.title("Elipsoid")
        ellipsoid_frame = tk.Frame(ellipsoid_window)
        ellipsoid_frame.grid(sticky='nesw')

        #Definisanje panela
        panel_naslov = tk.Frame(ellipsoid_window, width=310, height=50, pady=3)
        panel_naslov.grid(row=0, columnspan=2)

        naslov = tk.Label(panel_naslov, text='Parametri ' + self.name + ' elipsoida')
        naslov.grid(row=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        panel_container = tk.Frame(ellipsoid_window, bg="lightgrey", width=280, height=180, pady=3, padx=3)
        panel_container_left = tk.Frame(panel_container, width=150, height=320, pady=2)
        panel_container_right = tk.Frame(panel_container, width=150, height=320, pady=7, padx=6)
        panel_container.grid(row=1, columnspan=2)
        panel_container_left.grid(row=0, column=0, sticky=tk.E)
        panel_container_right.grid(row=0, column=1, sticky=tk.W)

        #Definisanje labela i polja za ispis parametara
        a_label = tk.Label(panel_container_left, text="a: ")
        a_unos = tk.Entry(panel_container_right)
        b_label = tk.Label(panel_container_left, text="b: ")
        b_unos = tk.Entry(panel_container_right)
        f_label = tk.Label(panel_container_left, text="f:  ")
        f_unos = tk.Entry(panel_container_right)
        e_label = tk.Label(panel_container_left, text="prvi ekscentricitet:  ")
        e_unos = tk.Entry(panel_container_right)
        eprim_label = tk.Label(panel_container_left, text="drugi ekscentricitet: ")
        eprim_unos = tk.Entry(panel_container_right)

        a_label.grid(row=0, column=0)
        b_label.grid(row=1, column=0)
        f_label.grid(row=2, column=0)
        e_label.grid(row=3, column=0)
        eprim_label.grid(row=4, column=0)

        a_unos.insert(0, str(self.a))
        a_unos.config(state='readonly', justify=tk.CENTER)
        b_unos.insert(0, str(self.b))
        b_unos.config(state='readonly', justify=tk.CENTER)
        f_unos.insert(0, str(self.e))
        f_unos.config(state='readonly', justify=tk.CENTER)
        e_unos.insert(0, str(self.e))
        e_unos.config(state='readonly', justify=tk.CENTER)
        eprim_unos.insert(0, str(self.eprim))
        eprim_unos.config(state='readonly', justify=tk.CENTER)

        a_unos.grid(row=0, column=0)
        b_unos.grid(row=1, column=0)
        f_unos.grid(row=2, column=0)
        e_unos.grid(row=3, column=0)
        eprim_unos.grid(row=4, column=0)

    #Funkcija koja kao rezultat vraća string za ispis parametara elipsoida
    def __str__(self):
        return "Aktivan elipsoid: " + str(self.name) + "\n\nParametri:\na: " + str(self.a) + "\nb: " +\
               str(self.b) + "\nf: " + str(self.f) +  "\nprvi ekscentricitet: " + str(self.e) \
               +  "\ndrugi ekscentricitet: " + str(self.eprim)

    #Funkcija za kreiranje proizvoljnog elipsoida
    def custom(self):
        # Funkcija koja poništava unijete parametre - dugme "Reset"
        def ponisti():
            a_unos.delete(0,'end')
            b_unos.delete(0,'end')
            f_unos.delete(0,'end')

            ispis['text'] = "Parametri resetovani!"
            ispis['fg'] = 'red'
            a_unos.focus()

        #Funkcija koja ispituje da li je tip podatka float (vraća True ili False)
        def is_float_try(str):
            try:
                float(str)
                return True
            except ValueError:
                return False

        #Funkcija koja ispituje da li je sve dobro unijeto, ako jeste, računa preostale parametre i
        #proslijeđuje parametre elipsoidu - dugme "Potrvdi"
        def potvrdi():
            if a_unos.index('end') == 0:  # Ispituje se da li je nesto unijeto u neko od polja
                ispis['text'] = "Velika poluosa nije definisana!"
                ispis['fg'] = "red"
                a_unos.focus()
                return

            elif b_unos.index("end") == 0 and f_unos.index("end") == 0:
                ispis['text'] = "Obavezan unos b ili f!!!"
                ispis['fg'] = "red"
                b_unos.focus()
                return

            elif b_unos.index("end") == 0:
                a = a_unos.get()
                f = f_unos.get()
                if is_float_try(a) == False:
                    ispis['text'] = "Velika poluosa nije dobro definisana!"
                    ispis['fg'] = "red"
                    a_unos.focus()
                    return
                elif is_float_try(f) == False:
                    ispis['text'] = "Spljoštenost nije dobro definisana!"
                    ispis['fg'] = "red"
                    f_unos.focus()
                    return
                a = float(a)
                f = float(f)

                b = a*(1-f)
                e = (math.pow(a, 2) - math.pow(b, 2))/math.pow(a, 2)
                e_prim = (math.pow(a, 2) - math.pow(b, 2))/math.pow(b, 2)

                self.__init__1("Proizvoljni elipsoid", a, b, f, e, e_prim)
                ispis['text'] = "Elipsoid je prihvaćen!"
                ispis['fg'] = "green"

            elif f_unos.index("end") == 0:
                a = a_unos.get()
                b = b_unos.get()
                if is_float_try(a) == False:
                    ispis['text'] = "Velika poluosa nije dobro definisana!"
                    ispis['fg'] = "red"
                    a_unos.focus()
                    return
                elif is_float_try(b) == False:
                    ispis['text'] = "Mala poluosa nije dobro definisana!"
                    ispis['fg'] = "red"
                    b_unos.focus()
                    return

                a = float(a)
                b = float(b)

                f = (a-b)/a
                e = (math.pow(a, 2) - math.pow(b, 2)) / math.pow(a, 2)
                e_prim = (math.pow(a, 2) - math.pow(b, 2)) / math.pow(b, 2)
                self.__init__1("Proizvoljni elipsoid", a, b, f, e, e_prim)
                ispis['text'] = "Elipsoid je prihvaćen!"
                ispis['fg'] = "green"

            elif b_unos.index("end") != 0 and f_unos.index("end") != 0:
                a = a_unos.get()
                b = b_unos.get()
                f = f_unos.get()
                if is_float_try(a) == False:
                    ispis['text'] = "Velika poluosa nije dobro definisana!"
                    ispis['fg'] = "red"
                    a_unos.focus()
                    return
                elif is_float_try(b) == False:
                    ispis['text'] = "Mala poluosa nije dobro definisana!"
                    ispis['fg'] = "red"
                    b_unos.focus()
                    return
                elif is_float_try(f) == False:
                    ispis['text'] = "Spljoštenost nije dobro definisana!"
                    ispis['fg'] = "red"
                    f_unos.focus()
                    return
                a = float(a)
                b = float(b)
                f = float(f)
                f_provera = (a-b)/a

                if round(f, 10) == round(f_provera, 10):
                    e = (math.pow(a, 2) - math.pow(b, 2)) / math.pow(a, 2)
                    e_prim = (math.pow(a, 2) - math.pow(b, 2)) / math.pow(b, 2)
                    self.__init__1("Proizvoljni elipsoid", a, b, f, e, e_prim)
                    ispis['text'] = "Elipsoid je prihvaćen!"
                    ispis['fg'] = "green"
                else:
                    ispis['text'] = "Unijeta i sračunata spljoštenost se ne podudaraju! "
                    ispis['fg'] = "red"
                    return

        #Podešavanje prozora, panela, naslova
        custom_window = tk.Tk()
        custom_window.resizable(False, False)  #Otklanjanje mogućnosti korisniku da podešava prozor
        custom_window.title("Proizvoljni elipsoid")
        panel_naslov = tk.Frame(custom_window, width=310, height=50, pady=3)
        panel_naslov.grid(row=0, columnspan=2)
        naslov = tk.Label(panel_naslov, text='Kreiranje proizvoljnog elipsoida')
        naslov.grid(row=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        panel_container = tk.Frame(custom_window, bg="lightgrey", width=300, height=330, pady=3, padx=3)
        panel_container_left = tk.Frame(panel_container, bg="lightgrey", width=150, height=320, pady=2)
        panel_container_right = tk.Frame(panel_container, bg="lightgrey", width=150, height=320, pady=7, padx=6)
        panel_container.grid(row=1, columnspan=2)
        panel_container_left.grid(row=0, column=0, sticky=tk.E)
        panel_container_right.grid(row=0, column=1, sticky=tk.W)

        #Definisanje labela i polja za unos i gridovanje
        a_label = tk.Label(panel_container_left, text="            a:     ", bg="lightgrey")
        a_unos = tk.Entry(panel_container_right)
        b_label = tk.Label(panel_container_left, text="             b:      ", bg="lightgrey")
        b_unos = tk.Entry(panel_container_right)
        f_label = tk.Label(panel_container_left, text="             f:      ", bg="lightgrey")
        f_unos = tk.Entry(panel_container_right)

        a_label.grid(row=0, column=0)
        b_label.grid(row=1, column=0)
        f_label.grid(row=2, column=0)

        a_unos.grid(row=0, column=0)
        b_unos.grid(row=1, column=0)
        f_unos.grid(row=2, column=0)

        #Definisanje i podešavanje položaja dugmadi
        panel_dugmad = tk.Frame(custom_window, width=300, height=100)
        dugme_ok = tk.Button(panel_dugmad, text="Potvrdi", command=potvrdi)
        dugme_ponisti = tk.Button(panel_dugmad, text="Poništi", command=ponisti)
        ispis = tk.Label(panel_dugmad, text="")
        panel_dugmad.grid(row=2, column=0, columnspan=2)
        ispis.grid(row=0, column=0, columnspan=2)
        dugme_ok.grid(row=1, column=0, padx=10, pady=5)
        dugme_ponisti.grid(row=1, column=1, pady=5, padx=10)