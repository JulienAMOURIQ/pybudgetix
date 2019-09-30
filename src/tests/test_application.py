#!/usr/bin/env python3
# -*- coding: utf-8 -*-²
"""
module test Pytest.
"""

from pybudgetix import application
import os


class TestDefaultSuite():
    def setup_method(self, method):
        self.conn = application.sqlite3.connect('test.db')
        application.cree_base(self.conn)

    def teardown_method(self, method):
        self.conn.close()
        os.remove('test.db')

    def test_inserer_groupe(self):
        """
        Un premier test.
        """
        application.sql_inserer_groupe(self.conn, "Voiture")
        application.sql_inserer_groupe(self.conn, "Logement")
        self.conn.commit()
        res = application.sql_lire_groupe(self.conn)
        assert res[0][1] == 'Voiture'
        assert res[1][1] == 'Logement'

    def test_sql_inserer_m_paiement(self):
        """Deuxième test"""
        application.sql_inserer_m_paiement(self.conn, "espèces")
        self.conn.commit()
        res = application.sql_lire_m_paiement(self.conn)
        assert res[0][1] == 'espèces'

    def test_sql_inserer_periodicite(self):
        """Troisième test"""
        application.sql_inserer_periodicite(self.conn, "mensuel", 30)
        self.conn.commit()
        res = application.sql_lire_periodicite(self.conn)
        assert res[0][1] == 'mensuel'
        assert res[0][2] == 30
