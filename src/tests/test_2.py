# coding=utf-8
import unittest
import src.evernote_cli
import os
from src.helper import krypto_manager


class CreateUserEvernoteTest(unittest.TestCase):
    def setUp(self):
        self.tmp_user_name = "test"
        self.tmp_user_password = "test"
        self.token = "S=s1:U=96801:E=1845cafec40:C=17d04fec040:P=185:A=mneuhaus:V=2:H=ce322afcd49b909aadff4e59c4354924"
        self.controller = src.evernote_cli.Evernote(
            "-u {user_name} -n {password} {token}".format(user_name=self.tmp_user_name, password=self.tmp_user_password,
                                                          token=self.token).split(" "))
        self.user = self.controller.global_data_manager.get_user(self.tmp_user_name, self.tmp_user_password)

    def test_user_credentials(self):
        password_hash = self.controller.global_data_manager._credentials.get(self.tmp_user_name)
        self.assertIsNotNone(password_hash)
        self.assertEqual(password_hash, krypto_manager.hash_str(self.tmp_user_password))

    def test_user_file_path(self):
        file_path = self.user.user_config.get("file_path")
        self.assertEqual(file_path, "user_data/{username}/files/".format(username=self.tmp_user_name))

    def test_user_token(self):
        token = self.user.user_config.get("key")
        km = krypto_manager.CryptoManager(key=self.tmp_user_password, salt="user",
                                          logger=self.controller.create_logger("Krypto"))
        self.assertEqual(km.decrypt_str(token), km.decrypt_str(km.encrypt_str(self.token)))

    def test_user_encryption_level(self):
        encryption_lvl = self.user.user_config.get("encrypt_level")
        self.assertEqual(encryption_lvl, self.user.encryption_level)

    def test_folder_structure(self):
        self.assertTrue(os.path.isdir("user_data/{username}".format(username=self.tmp_user_name)))
        self.assertTrue(os.path.isfile("user_data/{username}/.user_info.json".format(username=self.tmp_user_name)))
        self.assertTrue(os.path.isdir("user_data/{username}/files".format(username=self.tmp_user_name)))

    def tearDown(self):
        src.evernote_cli.Evernote("-u {user_name} -p {password} -rm".format(user_name=self.tmp_user_name,
                                                                            password=self.tmp_user_password).split(" "))


class RemoveUserEvernoteTest(unittest.TestCase):
    def setUp(self):
        self.tmp_user_name = "test"
        self.tmp_user_password = "test"
        self.token = "S=s1:U=96801:E=1845cafec40:C=17d04fec040:P=185:A=mneuhaus:V=2:H=ce322afcd49b909aadff4e59c4354924"
        self.controller = src.evernote_cli.Evernote(
            "-u {user_name} -n {password} {token}".format(user_name=self.tmp_user_name, password=self.tmp_user_password,
                                                          token=self.token).split(" "))
        self.user = self.controller.global_data_manager.get_user(self.tmp_user_name, self.tmp_user_password)

    def test_rm_user(self):
        self.controller = src.evernote_cli.Evernote("-u {username} -p {password} -rm".format(username=self.tmp_user_name,
                                                                                             password=self.tmp_user_password).split(
            " "))
        self.assertFalse(self.controller.global_data_manager.is_user(self.tmp_user_name))
        self.assertIsNone(self.controller.global_data_manager._credentials.get(self.tmp_user_name, None))
        self.assertFalse(os.path.isdir("user_data/{username}".format(username=self.tmp_user_name)))


class DownloadTest(unittest.TestCase):
    def setUp(self):
        self.tmp_user_name = "test"
        self.tmp_user_password = "test"
        self.token = "S=s1:U=96801:E=1845cafec40:C=17d04fec040:P=185:A=mneuhaus:V=2:H=ce322afcd49b909aadff4e59c4354924"
        self.controller = src.evernote_cli.Evernote(
            "-u {user_name} -n {password} {token}".format(user_name=self.tmp_user_name,
                                                          password=self.tmp_user_password,
                                                          token=self.token).split(" ")
        )

    def test_download(self):
        self.controller = src.evernote_cli.Evernote("-u {username} -p {password} -d".format(username=self.tmp_user_name,
                                                                                            password=self.tmp_user_password).split(" "))
        user = self.controller.global_data_manager.get_user(self.tmp_user_name, self.tmp_user_password)

        self.assertIsNotNone(user.user_config.get(self.tmp_user_name))

    def tearDown(self):
        src.evernote_cli.Evernote("-u {user_name} -p {password} -rm".format(user_name=self.tmp_user_name,
                                                                            password=self.tmp_user_password).split(" "))
class AutoriserungTest(unittest.TestCase):
    def setUp(self):
        self.tmp_user_name = "test"
        self.tmp_user_password = "test"
        self.token = "S=s1:U=96801:E=1845cafec40:C=17d04fec040:P=185:A=mneuhaus:V=2:H=ce322afcd49b909aadff4e59c4354924"
        self.controller = src.evernote_cli.Evernote(
            "-u {user_name} -n {password} {token}".format(user_name=self.tmp_user_name,
                                                          password=self.tmp_user_password,
                                                          token=self.token).split(" ")
        )

    def test_false_autorisierung(self):
        false_password = "falsepassword"
        self.controller = src.evernote_cli.Evernote(
            "-u {user_name} -p {password} -d".format(user_name=self.tmp_user_name,
                                                          password=false_password,
                                                          token=self.token).split(" ")
        )
        params = self.controller.par.params
        correct_param = {'err_types': ["Authentication failed! Check if password and username are correct. If you are using the program for the first time, create a new user with:    '-u <username> -n <passwd>'  Tried [test, falsepassword]"],
                         'func': 'input_error'}
        self.assertDictEqual(params, correct_param)

        password_hash = krypto_manager.hash_str(false_password)
        print password_hash
        self.assertFalse(self.controller.global_data_manager.check_user_hash(self.tmp_user_name, password_hash))

    def tearDown(self):
        src.evernote_cli.Evernote("-u {user_name} -p {password} -rm".format(user_name=self.tmp_user_name,
                                                                            password=self.tmp_user_password).split(" "))
if __name__ == '__main__':
    unittest.main(verbosity=2)
