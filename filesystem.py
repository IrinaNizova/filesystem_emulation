import unittest


class File:
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']

    def __str__(self):
        return self.name


class Filesystem:

    types = {dict: 'directory', File: 'file'}

    def __init__(self):
        self.filesystem = {}

    def _create_element(self, path, name, type):
        if not name:
            return NameError(self.types[type] + ' name is empty')
        if '/' in name:
            return ValueError('/ is forbidden symbol in {} name'.format(self.types[type]))
        parent_dir = self._get_reference(path)
        if parent_dir == False:
            return ValueError('Path is not valid')
        if name in parent_dir.keys():
            return KeyError('This {} has already exists'.format(self.types[type]))
        parent_dir[name] = {} if type == dict else File(name=name)

    def create_dir(self, path, name):
        return self._create_element(path, name, dict)

    def create_file(self, path, name):
        return self._create_element(path, name, File)

    def get_list_dir(self, path):
        p = self._get_reference(path)
        if p == False:
            return KeyError('Path is not valid')
        if not isinstance(p, dict):
            return TypeError('This is file, not directory')
        return list(self._get_reference(path).keys())

    def find_files_for_pattern(self, path, pattern):
        pass

    def _delete_element(self, path, name, type):
        p = self._get_reference(path)
        if p == False:
            return KeyError('Path is not valid')
        if name not in p.keys():
            return ValueError('This {} does not exist'.format(self.types[type]))
        if not isinstance(p[name], type):
            return TypeError('This is not {}'.format(self.types[type]))
        if type == dict and len(p[name]) > 0:
            return ValueError('This {} does not empty'.format(self.types[type]))
        del p[name]

    def delete_file(self, path, name):
        return self._delete_element(path, name, File)

    def delete_dir(self, path, name):
        return self._delete_element(path, name, dict)

    def _get_reference(self, path):
        p = self.filesystem
        path = path.strip('/')
        path = path.split('/') if len(path) > 0 else ''
        for dir in path:
            try:
                p = p[dir]
            except KeyError:
                return False
        return p


class TestFilesystem(unittest.TestCase):
    root_dir = '/'
    home_dir = '/home'
    fake_dir = '/home/fake'
    user_dir = '/home/user'
    user_file = '/home/user/file'
    filesystem = Filesystem()

    def test11FilesystemExists(self):
        filesystem = Filesystem()
        self.assertTrue(isinstance(filesystem.filesystem, dict), 'Filesystem not inicialize')

    def test12CreateRootDir(self):
        self.assertEqual(self.filesystem.create_dir(self.root_dir, 'home'), None, "File not create")
        self.assertEqual(self.filesystem.filesystem['home'], {}, 'Directory is not detected')

    def test13CreateDirWrongPath(self):
        self.assertTrue(isinstance(self.filesystem.create_dir(self.fake_dir, 'home'),
                                        ValueError), "Directory not create")

    def test14CreateNotRootDir(self):
        self.assertEqual(self.filesystem.create_dir(self.home_dir, 'user'), None, "File not create")
        self.assertEqual(self.filesystem.filesystem['home']['user'], {}, 'Directory is not detected')

    def test15CreateEmptyNameDir(self):
        self.assertTrue(isinstance(self.filesystem.create_dir(self.home_dir, ''),
            NameError), "File is created should not be at not exception is not correct")

    def test16SlashInNameDir(self):
        self.assertTrue(isinstance(self.filesystem.create_dir(self.home_dir, '/'),
            ValueError), "File is created should not be at not exception is not correct")

    def test17CreateExistNameDir(self):
        self.assertTrue(isinstance(self.filesystem.create_dir(self.root_dir, 'home'),
            KeyError), "File is created should not be at not exception is not correct")

    def test21CreateRootFile(self):
        self.assertEqual(self.filesystem.create_file(self.root_dir, 'file'), None, "File not create")
        self.assertTrue(isinstance(self.filesystem.filesystem['file'], File), 'File is not detected')

    def test22CreateNotRootFile(self):
        self.assertEqual(self.filesystem.create_file(self.user_dir, 'file'), None, "File not create")
        self.assertTrue(isinstance(self.filesystem.filesystem['home']['user']['file'], File), 'File is not detected')

    def test23CreateFileWrongPath(self):
        self.assertTrue(isinstance(self.filesystem.create_file(self.fake_dir, 'file'),
                                        ValueError), "File not create")
    def test24CreateEmptyNameFile(self):
        self.assertTrue(isinstance(self.filesystem.create_file(self.home_dir, ''),
            NameError), "File is created should not be at not exception is not correct")

    def test25SlashInNameFile(self):
        self.assertTrue(isinstance(self.filesystem.create_file(self.home_dir, '/'),
            ValueError), "File is created should not be at not exception is not correct")

    def test26CreateExistNameFile(self):
        self.assertTrue(isinstance(self.filesystem.create_dir(self.root_dir, 'file'),
            KeyError), "File is created should not be at not exception is not correct")

    def test31ListRootDir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(self.root_dir)),
                         ['file', 'home'], 'List of directories from root dir wasnt received')

    def test32ListHomeDir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(self.home_dir)),
                         ['user'], 'List of directories from home dir wasnt received')

    def test33ListUserDir(self):
        self.assertEqual(sorted(self.filesystem.get_list_dir(self.user_dir)),
                         ['file'], 'List of directories from root dir wasnt received')

    def test34ListNotExistDir(self):
        self.assertTrue(isinstance(self.filesystem.get_list_dir(self.fake_dir),
                         KeyError), 'List of directories from not existed dir was received')

    def test35TryListFromFile(self):
        self.assertTrue(isinstance(self.filesystem.get_list_dir(self.user_file),
                         TypeError), 'List of directories from file was received')

    def test51DelHomeFile(self):
        self.assertEqual(self.filesystem.delete_file(self.user_dir, 'file'), None, "File not delete")
        self.assertFalse('file' in list(self.filesystem.filesystem['home']['user'].keys()),
                         'File was not deleted')

    def test52DelAlreadyDeletingFile(self):
        self.assertTrue(isinstance(self.filesystem.delete_file(self.home_dir, 'file'),ValueError),
            "File was deleted successfully, although it is not should or exception is unexpected")

    def test53DelFakeDirFile(self):
        self.assertTrue(isinstance(self.filesystem.delete_file(self.fake_dir, 'file'), KeyError),
            "File was deleted successfully, although it is not should or exception is unexpected")

    def test54TryDelDirInsteadFile(self):
        self.assertTrue(isinstance(self.filesystem.delete_file(self.root_dir, 'home'), TypeError),
            "File was deleted successfully, although it is not should or exception is unexpected")

    def test61DelDirNotExistPath(self):
        self.assertTrue(isinstance(self.filesystem.delete_dir(self.fake_dir, 'user'), KeyError),
            "Dir was deleted successfully, although it is not should or exception is unexpected")

    def test62DelFileInsteadDir(self):
        self.assertTrue(isinstance(self.filesystem.delete_dir(self.root_dir, 'file'), TypeError),
            "Dir was deleted successfully, although it is not should or exception is unexpected")

    def test63DelNotEmptyDir(self):
        self.assertTrue(isinstance(self.filesystem.delete_dir(self.root_dir, 'home'), ValueError),
            "Dir was deleted successfully, although it is not should or exception is unexpected")

    def test64DelUserDir(self):
        self.assertEqual(self.filesystem.delete_dir(self.home_dir, 'user'), None, "Dir was not deleted")
        self.assertFalse('user' in list(self.filesystem.filesystem['home'].keys()),
                         'Dir is detected')

    def test65DelNotExistDir(self):
        self.assertTrue(isinstance(self.filesystem.delete_dir(self.home_dir, 'user'), ValueError),
            "Dir was deleted successfully, although it is not should or exception is unexpected")

if __name__ == '__main__':
    unittest.main()