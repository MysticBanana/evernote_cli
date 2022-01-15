import unittest
import main

# todo check for more than one run -> create user -> change something -> run download
class EvernoteTest(unittest.TestCase):
    '''
    def delete_user(self):
        tmp_user_name = "mneuhaus"
        tmp_user_password = "passwd123"
        controller = main.Evernote("-u {user_name} -p {password} -rm".format(user_name=tmp_user_name,
                                                                             password=tmp_user_password).split(" "))
        controller.global_data_manager.remove_user(tmp_user_name)

        tmp_user_name = "test"
        tmp_user_password = "test"
        controller = main.Evernote("-u {user_name} -p {password} -rm".format(user_name=tmp_user_name,
                                                                             password=tmp_user_password).split(" "))
        controller.global_data_manager.remove_user(tmp_user_name)
    '''

    def test_create(self):
        tmp_user_name = "mneuhaus"
        tmp_user_password = "passwd123"
        token = "S=s1:U=96801:E=1845cafec40:C=17d04fec040:P=185:A=mneuhaus:V=2:H=ce322afcd49b909aadff4e59c4354924"

        controller = main.Evernote("-u {user_name} -n {token} {password}".format(user_name=tmp_user_name,
                                                                                 password=tmp_user_password,
                                                                                 token=token).split(" "))
        self.assertEqual(controller.user.user_token, token)

        # check if files exists

        # testing with different user_names and passwords
        tmp_user_nam = "test"
        tmp_user_password = "test"
        token = "S=s1:U=96801:E=1845cafec40:C=17d04fec040:P=185:A=test:V=2:H=ce322afcd49b909aadff4e59c435"

        del controller
        controller = main.Evernote("-u {user_name} -n {token} {password}".format(user_name=tmp_user_nam,
                                                                                 password=tmp_user_password,
                                                                                 token=token).split(" "))
        self.assertEqual(controller.user.user_token, token)

    def normal(self):
        tmp_user_name = "mneuhaus"
        tmp_user_password = "passwd123"

        controller = main.Evernote("-u {user_name} -p {password} -c -e 2".format(user_name=tmp_user_name,
                                                                                 password=tmp_user_password).split(" "))

        self.assertEqual(controller.global_data_manager.check_user_hash(controller.username, controller.passwd_hash), True)
        self.assertIsNotNone(controller.user.user_token)
        self.assertIsNotNone(controller.user.user_name)
        self.assertIsNotNone(controller.user.user_password)





if __name__ == '__main__':
    unittest.main()



