#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3


def cree_base(connexion):
    cur=connexion.cursor()
    cur.executescript("""
CREATE TABLE GROUPE(
	id_groupe   		INTEGER NOT NULL,
	nom_groupe  		TEXT ,
	
	PRIMARY KEY (id_groupe)
);

CREATE TABLE M_PAIEMENT(
	id_m_paiement 		INTEGER NOT NULL,
	nom_m_paiement 		TEXT,
	PRIMARY KEY (id_m_paiement)
);


CREATE TABLE BUDGET(
	id_budget   		INTEGER NOT NULL ,
	id_groupe 		INTEGER NOT NULL,
	nom_budget  		TEXT ,
	PRIMARY KEY (id_budget),
	FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe)
);


CREATE TABLE PERIODICITE(
	id_periodicite		INTEGER NOT NULL ,
	nom_periodicite		TEXT ,
	taille_periodicite	INTEGER ,
	PRIMARY KEY (id_perio)
);


CREATE TABLE payer(
	date_debutINTEGER NOT NULL ,
	id_budgetINTEGER NOT NULL ,
	id_groupeINTEGER NOT NULL ,
	
	date_finINTEGER ,
	PRIMARY KEY (date_debut,id_budget) ,
	
	FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe),
	FOREIGN KEY (id_budget) REFERENCES BUDGET(id_budget)
);

""")

def sql_inserer_groupe(connexion,nomGroupe):
	cur=connexion.cursor()
	cur.execute("INSERT INTO GROUPE(nom_groupe)VALUES(?)",(nomGroupe,))
	#print(cur.fetchone())

def sql_inserer_budget(connexion,nomBudget):
	cur=connexion.cursor()
	cur.execute("INSERT INTO BUDGET(nom_budget)VALUES(?)",(nomBudget,))
	print(cur.fetchone())

def sql_inserer_periodicite(connexion,nomPerio,taillePerio):
	cur=connexion.cursor()
	cur.execute("INSERT INTO PERIODICITE(nom_perio,taille_perio)VALUES(?)",(nomPerio,taillePerio))
	print(cur.fetchone())

def sql_inserer_intervenir(connexion,instanceIntervention):
	cur=connexion.cursor()
	cur.execute("INSERT INTO INTERVENIR(date_debut,id_budget,id_groupe,date_fin)VALUES(?)",(instanceIntervention.get_dateDebut(),instanceIntervention.get_idBudget(),instanceIntervention.get_idGroupe(),instanceIntervention.get_dateFin()))
	print(cur.fetchone())

def sql_inserer_appliquer(connexio,instanceApplication):
	cur=connexion.cursor()
	#cur.execute("INSERT INTO PERIODICITE(nom_perio,taille_perio)VALUES(?)",(nomPerio,taillePerio))
	print(cur.fetchone())

def sql_lire_groupe(connexion):
	cur=connexion.cursor()
	cur.execute("SELECT * FROM GROUPE")
	print(cur.fetchall())

def sql_to_budget(connexion):
	cur=connexion.cursor()
	cur.execute("SELECT nom_groupe,nom_budget, ... FROM GROUPE")


class Budget:
	def __init__(self):
		self._lignesBudget=[]
		self._nom=""

	def get_bilan(self,dateDuJour):
		somme=0
		for e in self._lignesBudget:
			somme=somme + e.get_montant_deja_economise(dateDuJour)
		return somme

	def get_bilan_quotidien(self):
		somme=0
		for e in self._lignesBudget:
			somme=somme + e.get_bilan_quotidien()
		return somme

class LigneBudget:
	def __init__(self):
		self._idBudget=-1
		self._nomBudet=""
		self._dateDebutPeriode=-1
		self._periodicite=-1
		self._id_groupe=-1
		self._montantEcheances=-1
		self.moyenDePaiement=-1

	def get_bilan_quotidien(self):
		return self._montantEcheances/self._periodicite

	def get_montant_deja_economise(self,dateDuJour):
		return self.get_cout_journalier*(dateDuJour-self._dateDebutPeriode)


def main():
	import argparse
	parser = argparse.ArgumentParser()
	#parser.add_argument('-init', help="le chemin vers le fichier de regles (format texte ou format .sql d'oracle datamodeler, à noter que l'importation des fichiers sql est plus lente et se base sur les lignes 'ALTER TABLE xx ADD CONSTRAINT xxx PRIMARY KEY' et 'ALTER TABLE xx ADD CONSTRAINT xxx FOREIGN KEY (xxx) REFERENCES xxx(xxx)'  pour déterminer les dépendances fonctionnelles dont est issue le modèle de données )",required=True)
	#parser.add_argument('-init', help="ifiables, ie si une clé multi-valuée peut être simplifiée)",required=False)
	parser.add_argument('-init', help="Crée un nouveau fichier de données",required=False, action='store_true')
	parser.add_argument('-ig', help="Insérer un groupe",required=False)
	parser.add_argument('-id',help="Insérer un poste de dépense",required=False)
	args = parser.parse_args()
	print("Initialisation...")
	if args.init :
		conn = sqlite3.connect('example.db')
		cree_base(conn)
		conn.commit()
		conn.close()
	
	if args.ig :
		conn = sqlite3.connect('example.db')
		sql_inserer_groupe(conn,args.ig)
	
	#	conn = sqlite3.connect('example.db')
	#	sql_inserer_groupe(conn,"Voiture")
	#	sql_lire_groupe(conn)
	#	conn.commit()
	#	conn.close()
		
if __name__ == '__main__':
	main()
