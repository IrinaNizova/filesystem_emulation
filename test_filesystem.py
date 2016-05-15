from filesystem import Filesystem, File, Directory

import unittest

root_dir = '/'
home_dir = '/home'
fake_dir = '/home/fake'
user_dir = '/home/user'
user_file = '/home/user/file'

home = 'home'
user = 'user'
file = 'file'

class Test0InitializeFilesystem(unittest.TestCase):

    def test01_filesystem_exists(self):
        filesystem = Filesystem()
        self.assertIsInstance(filesystem.filesystem, dict, 'Filesystem is no initialize')


class Test1CreateDirs(unittest.TestCase):

    def setUp(self):
        self.filesystem = Filesystem()

    def test11_create_root_dir(self):
        self.assertIsNone(self.filesystem.create_dir(root_dir, home), "File not create")
        self.assertIsInstance(self.filesystem.filesystem[home], Directory, 'Directory is not detected')

    def test12_create_dir_wrong_path(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_dir(fake_dir, home)

    def test13_create_not_root_dir(self):
        self.filesystem.create_dir(root_dir, home)
        self.assertIsNone(self.filesystem.create_dir(home_dir, user), "File not create")
        self.assertIsInstance(self.filesystem.filesystem[home][user], Directory, 'Directory is not detected')

    def test14_create_empty_name_dir(self):
        with self.assertRaises(NameError):
            self.filesystem.create_dir(home_dir, '')


    def test15_slash_in_name_dir(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_dir(home_dir, '/')

    def test16_create_exist_name_dir(self):
        self.filesystem.create_dir(root_dir, home)
        with self.assertRaises(KeyError):
            self.filesystem.create_dir(root_dir, home)


class Test2CreateFiles(unittest.TestCase):

    def setUp(self):
        self.filesystem = Filesystem()
        self.filesystem.create_dir(root_dir, home)
        self.filesystem.create_dir(home_dir, user)

    def test21_create_root_file(self):
        self.assertIsNone(self.filesystem.create_file(root_dir, file), "File not create")
        self.assertIsInstance(self.filesystem.filesystem[file], File, 'File is not detected')

    def test22_create_not_root_file(self):
        self.assertIsNone(self.filesystem.create_file(user_dir, file), "File not create")
        self.assertIsInstance(self.filesystem.filesystem[home][user][file], File, 'File is not detected')

    def test23_create_file_wrong_path(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_file(fake_dir, file)

    def test24_create_empty_name_file(self):
        with self.assertRaises(NameError):
            self.filesystem.create_file(home_dir, '')

    def test25_slash_in_name_file(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_file(home_dir, '/')

    def test26_create_exist_name_file(self):
        self.filesystem.create_file(root_dir, file)
        with self.assertRaises(KeyError):
            self.filesystem.create_dir(root_dir, file)


class Test3GetDirsList(unittest.TestCase):

    def setUp(self):
        self.filesystem = Filesystem()
        self.filesystem.create_dir(root_dir, home)
        self.filesystem.create_dir(home_dir, user)
        self.filesystem.create_file(root_dir, file)
        self.filesystem.create_file(user_dir, file)

    def test31_list_root_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(root_dir)),
                         [file, home], 'List of directories from root dir wasnt received')

    def test32_list_home_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(home_dir)),
                         [user], 'List of directories from home dir wasnt received')

    def test33_list_user_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(user_dir)),
                         [file], 'List of directories from root dir wasnt received')

    def test34_list_not_exist_dir(self):
        with self.assertRaises(KeyError):
            self.filesystem.get_list_dir(fake_dir)

    def test35_try_list_from_file(self):
        with self.assertRaises(TypeError):
            self.filesystem.get_list_dir(user_file)

class Test5DeleteFiles(unittest.TestCase):

    def setUp(self):
        self.filesystem = Filesystem()
        self.filesystem.create_dir(root_dir, home)
        self.filesystem.create_dir(home_dir, user)
        self.filesystem.create_file(root_dir, file)
        self.filesystem.create_file(user_dir, file)

    def test1_del_home_file(self):
        self.assertIsNone(self.filesystem.delete_file(user_dir, file), "File not delete")
        self.assertFalse(file in list(self.filesystem.filesystem['home']['user'].keys()),
                         'File was not deleted')

    def test2_del_root_file(self):
        self.assertIsNone(self.filesystem.delete_file(root_dir, file), "File not delete")
        self.assertFalse(file in list(self.filesystem.filesystem.keys()),
                         'File was not deleted')

    def test3_del_already_deleting_file(self):
        with self.assertRaises(ValueError):
            self.filesystem.delete_file(home_dir, file)

    def test4_del_faked_dir_file(self):
        with self.assertRaises(KeyError):
            self.filesystem.delete_file(fake_dir, file)

    def test5_try_del_dir_instead_file(self):
        with self.assertRaises(TypeError):
            self.filesystem.delete_file(root_dir, home)


class Test6DeleteDirs(unittest.TestCase):

    def setUp(self):
        self.filesystem = Filesystem()
        self.filesystem.create_dir(root_dir, home)
        self.filesystem.create_dir(home_dir, user)
        self.filesystem.create_file(root_dir, file)

    def test1_del_dir_not_exist_path(self):
        with self.assertRaises(KeyError):
            self.filesystem.delete_dir(fake_dir, user)

    def test2_del_file_instead_dir(self):
        with self.assertRaises(TypeError):
            self.filesystem.delete_dir(root_dir, file)

    def test3_del_not_empty_dir(self):
        with self.assertRaises(ValueError):
            self.filesystem.delete_dir(root_dir, home)

    def test4_del_user_dir(self):
        self.assertIsNone(self.filesystem.delete_dir(home_dir, 'user'), "Dir was not deleted")
        self.assertFalse(user in list(self.filesystem.filesystem['home'].keys()),
                         'Dir is detected')

    def test5_del_not_exist_dir(self):
        with self.assertRaises(ValueError):
            self.filesystem.delete_dir(root_dir, user)


if __name__ == '__main__':
    unittest.main()
