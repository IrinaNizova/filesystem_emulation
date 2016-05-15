from filesystem import Filesystem, File

import unittest

class TestFilesystem(unittest.TestCase):
    root_dir = '/'
    home_dir = '/home'
    fake_dir = '/home/fake'
    user_dir = '/home/user'
    user_file = '/home/user/file'
    filesystem = Filesystem()

    def test01_filesystem_exists(self):
        filesystem = Filesystem()
        self.assertTrue(isinstance(filesystem.filesystem, dict), 'Filesystem is no initialize')

    def test11_create_root_dir(self):
        self.assertEqual(self.filesystem.create_dir(self.root_dir, 'home'), None, "File not create")
        self.assertEqual(self.filesystem.filesystem['home'], {}, 'Directory is not detected')

    def test12_create_dir_wrong_path(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_dir(self.fake_dir, 'home')

    def test13_create_not_root_dir(self):
        self.assertEqual(self.filesystem.create_dir(self.home_dir, 'user'), None, "File not create")
        self.assertEqual(self.filesystem.filesystem['home']['user'], {}, 'Directory is not detected')

    def test14_create_empty_name_dir(self):
        with self.assertRaises(NameError):
            self.filesystem.create_dir(self.home_dir, '')


    def test15_slash_in_name_dir(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_dir(self.home_dir, '/')

    def test16_create_exist_name_dir(self):
        with self.assertRaises(KeyError):
            self.filesystem.create_dir(self.root_dir, 'home')

    def test21_create_root_file(self):
        self.assertEqual(self.filesystem.create_file(self.root_dir, 'file'), None, "File not create")
        self.assertTrue(isinstance(self.filesystem.filesystem['file'], File), 'File is not detected')

    def test22_create_not_root_file(self):
        self.assertEqual(self.filesystem.create_file(self.user_dir, 'file'), None, "File not create")
        self.assertTrue(isinstance(self.filesystem.filesystem['home']['user']['file'], File), 'File is not detected')

    def test23_create_file_wrong_path(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_file(self.fake_dir, 'file')

    def test24_create_empty_name_file(self):
        with self.assertRaises(NameError):
            self.filesystem.create_file(self.home_dir, '')

    def test25_slash_in_name_file(self):
        with self.assertRaises(ValueError):
            self.filesystem.create_file(self.home_dir, '/')

    def test26_create_exist_name_file(self):
        with self.assertRaises(KeyError):
            self.filesystem.create_dir(self.root_dir, 'file')

    def test31_list_root_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(self.root_dir)),
                         ['file', 'home'], 'List of directories from root dir wasnt received')

    def test32_list_home_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(self.home_dir)),
                         ['user'], 'List of directories from home dir wasnt received')

    def test33_list_user_dir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(self.user_dir)),
                         ['file'], 'List of directories from root dir wasnt received')

    def test34_list_not_exist_dir(self):
        with self.assertRaises(KeyError):
            self.filesystem.get_list_dir(self.fake_dir)

    def test35_try_list_from_file(self):
        with self.assertRaises(TypeError):
            self.filesystem.get_list_dir(self.user_file)

    def test51_del_home_file(self):
        self.assertEqual(self.filesystem.delete_file(self.user_dir, 'file'), None, "File not delete")
        self.assertFalse('file' in list(self.filesystem.filesystem['home']['user'].keys()),
                         'File was not deleted')

    def test52_del_already_deleting_file(self):
        with self.assertRaises(ValueError):
            self.filesystem.delete_file(self.home_dir, 'file')

    def test53_del_faked_dir_file(self):
        with self.assertRaises(KeyError):
            self.filesystem.delete_file(self.fake_dir, 'file')

    def test54_try_del_dir_instead_file(self):
        with self.assertRaises(TypeError):
            self.filesystem.delete_file(self.root_dir, 'home')

    def test61_del_dir_not_exist_path(self):
        with self.assertRaises(KeyError):
            self.filesystem.delete_dir(self.fake_dir, 'user')

    def test62_del_file_instead_dir(self):
        with self.assertRaises(TypeError):
            self.filesystem.delete_dir(self.root_dir, 'file')

    def test63_del_not_empty_dir(self):
        with self.assertRaises(ValueError):
            self.filesystem.delete_dir(self.root_dir, 'home')

    def test64_del_user_dir(self):
        self.assertEqual(self.filesystem.delete_dir(self.home_dir, 'user'), None, "Dir was not deleted")
        self.assertFalse('user' in list(self.filesystem.filesystem['home'].keys()),
                         'Dir is detected')

    def test65_del_not_exist_dir(self):
        with self.assertRaises(ValueError):
            self.filesystem.delete_dir(self.home_dir, 'user')

if __name__ == '__main__':
    unittest.main()
