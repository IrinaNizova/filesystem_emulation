import re

class File:
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']

    def __str__(self):
        return 'file ' + self.name

    @staticmethod
    def print_class():
        return 'file'


class Directory(dict):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = kwargs['name']

    def __str__(self):
        return 'directory ' + self.name

    @staticmethod
    def print_class():
        return 'directory'


class Filesystem:

    def __init__(self):
        self.filesystem = {}

    def print_type(self, obj):
        return obj.print_class()

    def _create_element(self, path, name, el_type):
        if not name:
            raise EmptyNameError('{} name is empty'.format(self.print_type(el_type)))
        if '/' in name:
            raise SlashExistsError('/ is forbidden symbol in {} name'.format(self.print_type(el_type)))
        parent_dir = self._get_reference_for_el(path)
        if parent_dir is None:
            raise NotValidPathError('Path is not valid')
        if name in parent_dir.keys():
            raise AlreadyExists('This {} has already exists'.format(self.print_type(el_type)))
        parent_dir[name] = Directory(name=name) if el_type == Directory else File(name=name)

    def create_dir(self, path, name):
        return self._create_element(path, name, Directory)

    def create_file(self, path, name):
        return self._create_element(path, name, File)

    def get_list_dir(self, path):
        current_dir = self._get_reference_for_el(path)
        if current_dir is None:
            raise NotValidPathError('Path is not valid')
        if not isinstance(current_dir, dict):
            raise TypeError('This is file, not directory')
        return list(self._get_reference_for_el(path).keys())

    def find_files_for_pattern(self, path, pattern):
        pattern = "^" + pattern.replace('*', '.*') + "$"
        finded_files = []
        for el in self.get_list_dir(path):
            if re.search(pattern, el):
                finded_files.append(el)
        return finded_files

    def _delete_element(self, path, name, el_type):
        parent_dir = self._get_reference_for_el(path)
        if parent_dir is None:
            raise NotValidPathError('Path is not valid')
        if name not in parent_dir.keys():
            raise NotExistsError('This {} does not exist'.format(self.print_type(el_type)))
        if not isinstance(parent_dir[name], el_type):
            raise TypeError('This is not {}'.format(self.print_type(el_type)))
        if el_type == Directory and len(parent_dir[name]) > 0:
            raise ValueError('This {} does not empty'.format(self.print_type(el_type)))
        del parent_dir[name]

    def delete_file(self, path, name):
        return self._delete_element(path, name, File)

    def delete_dir(self, path, name):
        return self._delete_element(path, name, Directory)

    def _get_reference_for_el(self, path):
        filesystem = self.filesystem
        path = path.strip('/')
        path = path.split('/') if len(path) > 0 else ''
        for directory in path:
            try:
                filesystem = filesystem[directory]
            except KeyError:
                return None
        return filesystem


class EmptyNameError(NameError):
    pass


class SlashExistsError(ValueError):
    pass


class NotValidPathError(ValueError):
    pass


class AlreadyExists(KeyError):
    pass


class NotExistsError(KeyError):
    pass
