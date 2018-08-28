import unittest
from datab import DataBase as dbase

class TestDB(unittest.TestCase):
    def setUp(self):
        print('\n')
        print('===============')
        print('Created database and insert some data')
        dbase.created_database()
        dbase.insert_data('Denys Kryvak', '12345')
        dbase.insert_data('Kek Lol', '12345')
        dbase.insert_data('Dima Kruk', '12345')
    
    def test_db_query(self):
        self.assertEqual(dbase.select_data(1), 'Denys Kryvak')
        self.assertEqual(dbase.select_data(3), 'Dima Kruk')
    
    
    def tearDown(self):
        dbase.drop_database()
        print("Drop database")
        print('===============')
    
if __name__=="__main__":
    unittest.main()
