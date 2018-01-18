#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion du modèle
"""
import sqlite3


def cree_base(connexion):
    """
    Fonction pour créer une base vide où enregistrer les données sur le
    disque dur
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

	PRIMARY KEY (id_perio)
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
    cur = connexion.cursor()
    cur.execute("INSERT INTO GROUPE(nom_groupe)VALUES(?)", (nom_groupe, ))
    #print(cur.fetchone())


def sql_inserer_m_paiement(connexion, id_m_paiement, nom_m_paiement):
    cur = connexion.cursor()
    cur.execute("INSERT INTO M_PAIEMENNT(id_m_paiement,nom_m_paiement)VALUES(?)",
                (id_m_paiement, nom_m_paiement))
    print(cur.fetchone())


def sql_inserer_budget(connexion, nomBudget):
    cur = connexion.cursor()
    cur.execute("INSERT INTO BUDGET(nom_budget)VALUES(?)", (nomBudget, ))
    print(cur.fetchone())


def sql_inserer_periodicite(connexion, nom_periode, taile_periode):
    cur = connexion.cursor()
    cur.execute("INSERT INTO PERIODICITE(nom_perio,taille_perio)VALUES(?)", (nom_periode, taile_periode))
    print(cur.fetchone())


def sql_inserer_paiement(connexion, instance_paiement):
    cur = connexion.cursor()
    cur.execute("INSERT INTO payer(id_budget,id_m_paiement,id_periodicite,montant)VALUES(?)",
                (instance_paiement.get_id_budget(),
                 instance_paiement.get_m_paiement(),
                 instance_paiement.get_id_periodicite(),
                 instance_paiement.get_montant()
                ))
    print(cur.fetchone())


def sql_lire_groupe(connexion):
    cur = connexion.cursor()
    cur.execute("SELECT * FROM GROUPE")
    print(cur.fetchall())


def sql_to_budget(connexion):
    cur = connexion.cursor()
    cur.execute("SELECT nom_groupe,nom_budget, ... FROM GROUPE")


class Budget(object):
    """

    """
    def __init__(self):
        self._lignesBudget = []
        self._nom = ""

    def get_bilan(self, date_du_jour):
        somme = 0
        for elmnt in self._lignesBudget:
            somme = somme + elmnt.get_montant_deja_economise(date_du_jour)
        return somme

    def get_bilan_quotidien(self):
        somme = 0
        for elmnt in self._lignesBudget:
            somme = somme + elmnt.get_bilan_quotidien()
        return somme


class LigneBudget(object):
    """

    """
    def __init__(self):
        self._id_budget = -1
        self._nom_budget = ""
        self._date_debut_periode = -1
        self._periodicite = -1
        self._id_groupe = -1
        self._montant_echeances = -1
        self._moyen_de_paiement = -1

    def get_bilan_quotidien(self):
        return self._montant_echeances/self._periodicite

    def get_montant_deja_economise(self, date_du_jour):
        return self.get_bilan_quotidien*(date_du_jour-self._date_debut_periode)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument('-init', help="le chemin vers le fichier de regles (format texte ou format .sql d'oracle datamodeler, à noter que l'importation des fichiers sql est plus lente et se base sur les lignes 'ALTER TABLE xx ADD CONSTRAINT xxx PRIMARY KEY' et 'ALTER TABLE xx ADD CONSTRAINT xxx FOREIGN KEY (xxx) REFERENCES xxx(xxx)'  pour déterminer les dépendances fonctionnelles dont est issue le modèle de données )",required=True)
    # parser.add_argument('-init', help="ifiables, ie si une clé multi-valuée peut être simplifiée)",required=False)
    parser.add_argument('-init', help="Crée un nouveau fichier de données",
                        required=False, action='store_true')
    parser.add_argument('-ig', help="Insérer un groupe", required=False)
    parser.add_argument('-id', help="Insérer un poste de dépense",
                        required=False)
    args = parser.parse_args()
    print("Initialisation...")
    if args.init:
        conn = sqlite3.connect('example.db')
        cree_base(conn)
        conn.commit()
        conn.close()

    if args.ig:
        conn = sqlite3.connect('example.db')
        sql_inserer_groupe(conn, args.ig)

    #   conn = sqlite3.connect('example.db')
    #   sql_inserer_groupe(conn,"Voiture")
    #   sql_lire_groupe(conn)
    #   conn.commit()
    #   conn.close()

if __name__ == '__main__':
    main()
