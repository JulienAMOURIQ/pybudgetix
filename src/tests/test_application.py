#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

    def test_inserer_group(self):
        """
        Un premier test.
        """
        application.sql_inserer_groupe(self.conn, "Voiture")
        application.sql_inserer_groupe(self.conn, "Logement")
        self.conn.commit()
        res = application.sql_lire_groupe(self.conn)
        assert res[0][1] == 'Voiture'
        assert res[1][1] == 'Logement'
        
