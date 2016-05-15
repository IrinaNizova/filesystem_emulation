from filesystem import *

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
        with self.assertRaises(NotValidPathError):
            self.filesystem.create_dir(fake_dir, home)

    def test13_create_not_root_dir(self):
        self.filesystem.create_dir(root_dir, home)
        self.assertIsNone(self.filesystem.create_dir(home_dir, user), "File not create")
        self.assertIsInstance(self.filesystem.filesystem[home][user], Directory, 'Directory is not detected')

    def test14_create_empty_name_dir(self):
        with self.assertRaises(EmptyNameError):
            self.filesystem.create_dir(home_dir, '')


    def test15_slash_in_name_dir(self):
        with self.assertRaises(SlashExistsError):
            self.filesystem.create_dir(home_dir, '/')

    def test16_create_exist_name_dir(self):
        self.filesystem.create_dir(root_dir, home)
        with self.assertRaises(AlreadyExists):
            self.filesystem.create_dir(root_dir, home)


class Test2CreateFiles(unittest.TestCase):

    def setUp(self):
        self.filesystem = Filesystem()
        self.filesystem.create_dir(root_dir, home)
        self.filesystem.create_dir(home_dir, user)

    def test1_create_root_file(self):
        self.assertIsNone(self.filesystem.create_file(root_dir, file), "File not create")
        self.assertIsInstance(self.filesystem.filesystem[file], File, 'File is not detected')

    def test2_create_not_root_file(self):
        self.assertIsNone(self.filesystem.create_file(user_dir, file), "File not create")
        self.assertIsInstance(self.filesystem.filesystem[home][user][file], File, 'File is not detected')

    def test3_create_file_wrong_path(self):
        with self.assertRaises(NotValidPathError):
            self.filesystem.create_file(fake_dir, file)

    def test4_create_empty_name_file(self):
        with self.assertRaises(EmptyNameError):
            self.filesystem.create_file(home_dir, '')

    def test5_slash_in_name_file(self):
        with self.assertRaises(SlashExistsError):
            self.filesystem.create_file(home_dir, '/')

    def test6_create_exist_name_file(self):
        self.filesystem.create_file(root_dir, file)
        with self.assertRaises(AlreadyExists):
            self.filesystem.create_dir(root_dir, file)


class Test3GetDirsList(unittest.TestCase):

    def setUp(self):
        self.filesystem = Filesystem()
        self.filesystem.create_dir(root_dir, home)
        self.filesystem.create_dir(home_dir, user)
        self.filesystem.create_file(root_dir, file)
        self.filesystem.create_file(user_dir, file)

    def test1_list_root_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(root_dir)),
                         [file, home], 'List of directories from root dir wasnt received')

    def test2_list_home_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(home_dir)),
                         [user], 'List of directories from home dir wasnt received')

    def test3_list_user_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(user_dir)),
                         [file], 'List of directories from root dir wasnt received')

    def test4_list_not_exist_dir(self):
        with self.assertRaises(NotValidPathError):
            self.filesystem.get_list_dir(fake_dir)

    def test5_try_list_from_file(self):
        with self.assertRaises(TypeError):
            self.filesystem.get_list_dir(user_file)


class Test4FindFiles(unittest.TestCase):
    file1 = 'file1'
    file2 = 'file2'
    text1 = 'text1'

    def setUp(self):
        self.filesystem = Filesystem()
        self.filesystem.create_dir(root_dir, home)
        self.filesystem.create_file(home_dir, self.file1)
        self.filesystem.create_file(home_dir, self.file2)
        self.filesystem.create_file(home_dir, self.text1)

    def test1_find_full_name(self):
        self.assertEqual(self.filesystem.find_files_for_pattern(home_dir, self.file1), [self.file1])

    def test2_find_start_name(self):
        self.assertEqual(sorted(self.filesystem.find_files_for_pattern(home_dir, 'file*')),
                         [self.file1, self.file2])

    def test3_find_end_name(self):
        self.assertEqual(sorted(self.filesystem.find_files_for_pattern(home_dir, '*1')),
                         [self.file1, self.text1])

    def test4_find_not_exist_name(self):
        self.assertFalse(self.filesystem.find_files_for_pattern(home_dir, 'file3'))

    def test5_find_not_exist_mask(self):
        self.assertFalse(self.filesystem.find_files_for_pattern(home_dir, 'filing*'))

    def test6_find_start_end_name(self):
        self.assertEqual(self.filesystem.find_files_for_pattern(home_dir, 't*1'), [self.text1])

    def test7_find_not_exist_path(self):
        with self.assertRaises(NotValidPathError):
            self.filesystem.find_files_for_pattern(user_dir, 'file')

    def test8_find_not_valid_path(self):
        with self.assertRaises(TypeError):
            self.filesystem.find_files_for_pattern("/".join((home_dir, self.text1)), 'file')


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
        with self.assertRaises(NotExistsError):
            self.filesystem.delete_file(home_dir, file)

    def test4_del_faked_dir_file(self):
        with self.assertRaises(NotValidPathError):
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
        with self.assertRaises(NotValidPathError):
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
        with self.assertRaises(NotExistsError):
            self.filesystem.delete_dir(root_dir, user)


if __name__ == '__main__':
    unittest.main()
