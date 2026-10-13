from operator import attrgetter

class Strumenti:
    """Rappresenta un strumento presente nel deposito"""

    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        """Inizializza gli attributi"""
        self.__codice = codice
        self.__tipo = tipo
        self.__marca = marca
        self.__anno_acquisto = anno_acquisto
        self.__valore = valore

    @property
    def codice(self):
        return self.__codice

    @property
    def marca(self):
        return self.__marca

    def __str__(self):
        """Necessario per la rappresentazione testuale dello strumento"""
        return f"{self.__codice}, {self.__tipo}, {self.__marca}, {self.__anno_acquisto}, {self.__valore:.2f}  "


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.__responsabile = responsabile
        self.__strumenti = dict()  # Dizionario codice - strumento
        self.__prestiti = dict()  # Dizionario per i prestiti
        self.__strumenti_in_prestito = set()  # Insieme dei codici in prestito
        self.__contatore_prestiti = 1

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, "r") as file:
                for riga in file:
                    campi = riga.split(",")
                    if len(campi) != 5:
                        raise IndexError("Il formato della riga non è corretto")
                    else:
                        codice = campi[0]
                        tipo_strumento = campi[1]
                        marca = campi[2]
                        # Mi assicuro che il formato dell'anno sia corretto
                        try:
                            anno = int(campi[3])
                            if anno < 0:
                                raise ValueError(f"{campi[3]} non è un intero positivo")
                        except ValueError:
                            raise ValueError(f"{campi[3]} non è un intero positivo")
                        # Mi assicuro che il formato del costo sia corretto
                        try:
                            costo = float(campi[4])
                            if costo < 0:
                                raise ValueError(f"{campi[4]} non è un float positivo")
                        except ValueError:
                            raise ValueError(f"{campi[4]} non è un float positivo")
                        # Creo l'oggetto strumento e lo salvo nel dizionario "strumenti"
                        strumento = Strumenti(codice, tipo_strumento, marca, anno, costo)
                        self.__strumenti[codice] = strumento

        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: {file_path} non è stato trovato")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        numero_strumenti = len(self.__strumenti) + 1
        while f"S{numero_strumenti}" in self.__strumenti:
            numero_strumenti += 1
        codice = f"S{numero_strumenti}"
        nuovo_oggetto_strumenti = Strumenti(codice, tipo, marca, anno_acquisto, valore)
        self.__strumenti[codice] = nuovo_oggetto_strumenti
        return nuovo_oggetto_strumenti

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.__strumenti.values(), key = attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # Verifico che il codice esista
        if id_strumento not in self.__strumenti:
            raise Exception(f"Lo strumento {id_strumento} non esiste")
        # Verifico che lo strumento non sia già stato prestato
        if id_strumento in self.__strumenti_in_prestito:
            raise Exception(f"Lo strumento {id_strumento} è già in prestito")
        id_prestito = f"P{self.__contatore_prestiti}"
        self.__contatore_prestiti += 1
        # Strutturo il dizionario dei prestiti
        prestito = {"id_prestito": id_prestito, "data_prestito": data,
                    "strumento_prestato": self.__strumenti[id_strumento], "allievo": cognome_allievo}
        # Registro il prestito
        self.__prestiti[id_prestito] = prestito
        self.__strumenti_in_prestito.add(id_strumento)
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # Verifico che il codice all'interno dei prestiti sia presente
        if id_prestito not in self.__prestiti:
            raise Exception(f"Il codice {id_prestito} non esiste")
        #  Trovo e tolgo lo strumento dai prestiti
        prestito = self.__prestiti[id_prestito]
        id_strumento = prestito["strumento_prestato"].codice
        self.__strumenti_in_prestito.remove(id_strumento)
        del self.__prestiti[id_prestito]
        return prestito
