import unittest
from unittest_data import Volunteer
from data import  global_data_manager

class TestVolunteer(unittest.TestCase):

    def test_fullname(self):
        vol_1 = Volunteer('Max', 'Mustermann')

        self.assertEqual(vol_1.fullname, 'Max Mustermann')


    def test_userhash(self):
        gdm = global_data_manager.GlobalFileManager(None)
        gdm.check_user_hash()



if __name__ == '__main__':
    unittest.main()



