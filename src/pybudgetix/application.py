#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion du modèle.
"""
import sqlite3
# import gettext
# gettext.install('application', '../../langue')


def cree_base(connexion):
    """
    Fonction pour créer une base vide .
    Cette base permettra d' enregistrer les données sur le disque dur.
    """
    cur = connexion.cursor()
    cur.executescript("""
CREATE TABLE GROUPE(
    id_groupe   		INTEGER NOT NULL,
    nom_groupe  		TEXT,

    PRIMARY KEY (id_groupe)
);

CREATE TABLE M_PAIEMENT(
    id_m_paiement 		INTEGER NOT NULL,
    nom_m_paiement 		TEXT,

    PRIMARY KEY (id_m_paiement)
);


CREATE TABLE BUDGET(
    id_budget           INTEGER NOT NULL ,
    id_groupe           INTEGER NOT NULL,
    nom_budget          TEXT ,

    PRIMARY KEY (id_budget),
    FOREIGN KEY (id_groupe)         REFERENCES GROUPE       (id_groupe)
);


CREATE TABLE PERIODICITE(
    id_periodicite		INTEGER NOT NULL ,
    nom_periodicite		TEXT ,
    taille_periodicite	INTEGER ,

    PRIMARY KEY (id_periodicite)
);


CREATE TABLE payer(
    id_budget           INTEGER NOT NULL ,
    id_m_paiement       INTEGER NOT NULL ,
    id_periodicite      INTEGER NOT NULL ,
    montant             INTEGER ,

    PRIMARY KEY (id_budget, id_m_paiement) ,

    FOREIGN KEY (id_budget)         REFERENCES BUDGET       (id_budget),
    FOREIGN KEY (id_m_paiement)     REFERENCES M_PAIEMENT   (id_m_paiement),
    FOREIGN KEY (id_periodicite)    REFERENCES PERIODICITE  (id_periodicite)
);

""")


def sql_inserer_groupe(connexion, nom_groupe):
    """Cette fonction permet d'insérer un groupe dans la base de données."""
    cur = connexion.cursor()
    cur.execute("INSERT INTO GROUPE(nom_groupe)VALUES(?)", (nom_groupe, ))
    # print(cur.fetchone())


def sql_inserer_m_paiement(connexion, nom_m_paiement):
    """Cette fonction permet d'insérer un moyen de paiement dans la BDD."""
    cur = connexion.cursor()
    cur.execute("INSERT INTO M_PAIEMENT(nom_m_paiement)" +
                "VALUES(?)", (nom_m_paiement))
    print(cur.fetchone())


def sql_inserer_budget(connexion, nom_budget):
    """Cette fonction permet d'insérer un budget dans la BDD."""
    cur = connexion.cursor()
    cur.execute("INSERT INTO BUDGET(nom_budget)VALUES(?)", (nom_budget, ))
    print(cur.fetchone())


def sql_inserer_periodicite(connexion, nom_periode, taile_periode):
    """

    """
    cur = connexion.cursor()
    cur.execute("INSERT INTO PERIODICITE(nom_perio,taille_perio)VALUES(?)",
                (nom_periode, taile_periode))
    print(cur.fetchone())


def sql_inserer_paiement(connexion, instance_paiement):
    """

    """
    cur = connexion.cursor()
    cur.execute("INSERT INTO payer" +
                "(id_budget,id_m_paiement,id_periodicite,montant)VALUES(?)",
                (instance_paiement.get_id_budget(),
                 instance_paiement.get_m_paiement(),
                 instance_paiement.get_id_periodicite(),
                 instance_paiement.get_montant()
                 ))
    print(cur.fetchone())


def sql_lire_groupe(connexion):
    """

    """
    cur = connexion.cursor()
    cur.execute("SELECT * FROM GROUPE")
    return(cur.fetchall())


def sql_to_budget(connexion):
    """

    """
    cur = connexion.cursor()
    cur.execute("SELECT nom_groupe,nom_budget, ... FROM GROUPE")


class Budget(object):
    """Un budget regroupe plusieurs lignes de budget."""

    def __init__(self):
        """Constructeur par défaut du budget."""
        self._lignes_budget = []
        self._nom = ""

    def get_bilan(self, date_du_jour):
        """
        Permet d'obtenir le bilan du budget.

        @Param date_du_jour: Date du jour dont on veut le bilan.
        @Retrun Montant économisé à la date du jour.
        """
        somme = 0
        for elmnt in self._lignes_budget:
            somme = somme + elmnt.get_montant_deja_economise(date_du_jour)
        return somme

    def get_bilan_quotidien(self):
        """Le bilan quotidien est la somme économisée chaque jour."""
        somme = 0
        for elmnt in self._lignes_budget:
            somme = somme + elmnt.get_bilan_quotidien()
        return somme


class LigneBudget(object):
    """
        La classe LigneBudget permet d'enregistrer une ligne du budget.

        Chaque ligne est définie par un identifiant, un nom,
        un début de période, une périodicité, un groupe, un montant
        des échéances et un moyen de paiement.
    """

    def __init__(self):
        """Constructeur par défaut."""
        self._id_budget = -1
        self._nom_budget = ""
        self._date_debut_periode = -1
        self._periodicite = -1
        self._id_groupe = -1
        self._montant_echeances = -1
        self._moyen_de_paiement = -1

    def get_bilan_quotidien(self):
        """

        """
        return self._montant_echeances/self._periodicite

    def get_montant_deja_economise(self, date_du_jour):
        """

        """
        return self.get_bilan_quotidien*(date_du_jour-self._date_debut_periode)


def exportcsv(connexion):
    """Exporte le contenu de la base en fichier csv."""
    pass


def main():
    """Permet d'intéragir avec la base de données en console."""
    import argparse

    NOM_BASE = "example.db"
    parser = argparse.ArgumentParser()

    parser.add_argument('-init', help="Crée un nouveau fichier de données",
                        required=False, action='store_true')
    parser.add_argument('-ig', help="Insérer un groupe", required=False)
    parser.add_argument('-id', help="Insérer un poste de dépense",
                        required=False)
    parser.add_argument('-im', help="Insérer un moyen de paiement",
                        required=False)
    parser.add_argument('-lb', help="Lire le bilan du budget à la date",
                        required=False)
    parser.add_argument('-importcsv', help="""Importer les données depuis un ficher csv.
                        la première colonne donne le nom du budget,
                        la seconde le groupe,
                        la troisième le montant du budget,
                        la quatrième le moyen de paiement
                        la cinquième la périodicité,
                        la sixième la date de début """,
                        required=False)
    parser.add_argument('-exportcsv', help="""Exporter les données vers un ficher csv.
                        la première colonne donne le nom du budget,
                        la seconde le groupe,
                        la troisième le montant du budget,
                        la quatrième le moyen de paiement
                        la cinquième la périodicité,
                        la sixième la date de début """,
                        required=False)
    args = parser.parse_args()
    print("Initialisation...")
    conn = sqlite3.connect(NOM_BASE)
    if args.init:
        cree_base(conn)
        conn.commit()

    if args.ig:
        sql_inserer_groupe(conn, args.ig)
        conn.commit()

    if args.im:
        sql_inserer_m_paiement(conn, args.im)
        conn.commit()

    if args.lb:
        pass

    if args.importcsv:
        pass

    if args.exportcsv:
        pass

    conn.close()
    #   conn = sqlite3.connect('example.db')
    #   sql_inserer_groupe(conn,"Voiture")
    #   sql_lire_groupe(conn)
    #   conn.commit()
    #   conn.close()

if __name__ == '__main__':
    main()
