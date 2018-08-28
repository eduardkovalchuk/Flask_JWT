import unittest
import os
import sqlite3
from datab import DataBase as dbase

class TestDB(unittest.TestCase):
    def setUp(self):
        print('\n')
        print('===============')
        print('Created database and insert some data')
        dbase.created_database()
        dbase.insert_data('Denys Kryvak', '12345')
    
    def test_db_query(self):
        self.assertEqual(dbase.select_data(1), 'Denys Kryvak')
    
    
    def tearDown(self):
        dbase.drop_database()
        print("Drop database")
        print('===============')
    
