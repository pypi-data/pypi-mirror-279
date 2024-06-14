import os
import numpy as np
import gzip

from pydmsp._dmspexeptions import FilePathError
from pydmsp._dmspexeptions import EmptyFileError
from pydmsp._dmspexeptions import FileNameError
from pydmsp._dmspexeptions import FileExtensionError
from pydmsp._dmspexeptions import ModeStrError
from pydmsp._dmspexeptions import ModeNameError
from pydmsp._dmspexeptions import MaxGzipSizeError


_LEN_FILENAME = 13
_MAX_GZIP_SIZE = 2147483648


def _get_gzip_size(filename):
    '''
        Возвращает размер gzip-архива в байтах

        :param filename: (string) имя архива

        :return: (int) размер архива в байтах
    '''
    with open(filename, 'rb') as f:
        f.seek(-4, 2)
        size = int.from_bytes(f.read(), 'little')

    return size


def _check_gzip_size(filename):
    '''
        Проверяет не превышает ли размер gzip-архива 2 ГБ

        :param filename: (string) имя архива

        :return: None
    '''
    size = _get_gzip_size(filename)

    if size > _MAX_GZIP_SIZE:
        raise MaxGzipSizeError()


def _unzip_to_bytes(filename):
    '''
        Выполняет распаковку gzip-архива

        :param filename: (string) имя архива

        :return: (bytes) набор байт
    '''
    _is_filename_correct(filename)
    _check_gzip_size(filename)

    with gzip.open(filename, 'rb') as f:
        file_content = f.read()

    return file_content


def _unzip_to_file(filename, file_content):
    '''
        Выполняет распаковку gzip-архива в бинарный файл

        :param filename: (string) имя архива
        :param file_content: (bytes) набор байт из файла архива, после работы функции "_unzip_to_bytes()"

        :return: None
    '''
    filename = filename.replace('.gz', '')
    with open(filename, 'wb') as f:
        f.write(file_content)


def _unzip_to_RAM(file_content):
    '''
        Выполняет распаковку gzip-архива в оперативную память

        :param file_content: (bytes) набор байт из файла архива, после работы функции "_unzip_to_bytes()"

        :return: (numpy.uint16): numpy-массив содержимого gzip-архива
    '''
    return np.frombuffer(file_content, dtype='>u2')


def _get_filename(filepath):
    '''
        Возвращает имя файла из переданного пути

        :param filepath: (string) путь к файлу

        :return: (string) имя файла
    '''
    _is_filepath_correct(filepath)
    head, tail = os.path.split(os.path.abspath(filepath))
    return tail


def _is_filepath_correct(filepath):
    '''
        Выполняет проверку корректности пути к файлу gzip-архива

        :param filepath: (string) путь к файлу gzip-архива

        :return: None или исключения одного из типов: FilePathError(), FileNotFoundError()
    '''
    if type(filepath) is not str:
        raise FilePathError()
    if os.path.exists(filepath) is False:
        raise FileNotFoundError()
    elif os.path.isfile(filepath) is False:
        raise FileNotFoundError(f'"{filepath}" is not a file')


def _is_filename_correct(filename):
    '''
        Выполняет проверку корректности имени файла gzip-архива

        :param filename: (string) имя файла gzip-архива

        :return: None или исключения одного из типов: EmptyFileError(), FileNameError(), FileExtensionError()
    '''
    if os.stat(filename).st_size == 0:
        raise EmptyFileError()
    elif len(filename) != _LEN_FILENAME or filename[0] != 'j' or filename[2] != 'f':
        raise FileNameError()
    elif filename[-3:] != '.gz':
        raise FileExtensionError()


def _check_unzip_mode(mode):
    '''
        Выполняет проверку переданного режима распаковки файла gzip-архива

        :param mode: (string) режим распаковки файла gzip-архива

        :return: None или исключения одного из типов: ModeStrError(), ModeNameError()
    '''
    if type(mode) is not str:
        raise ModeStrError()
    elif mode != 'to_file' and mode != 'to_ram':
        raise ModeNameError()


def unzip(filepath, mode='to_file'):
    r'''
    Выполняет распаковку gz-архива DMSP в бинарный файл (по умолчанию) или в оперативную память

            :param filepath: (string) путь к архиву (используйте два обратных слеша)

            :param mode: (string) режим распаковки
                to_file (по умолчанию): сохранение в бинарный файл с именем архива или
                to_ram: сохранение в оперативную память

            :return:
                None (по умолчанию) или
                content (numpy.ndarray): бинарные данные DMSP при распаковке в оперативную память
    '''
    filename = _get_filename(filepath)
    file_content = _unzip_to_bytes(filename)
    _check_unzip_mode(mode)

    if mode == 'to_file':
        _unzip_to_file(filename, file_content)
        return None
    elif mode == 'to_ram':
        content = _unzip_to_RAM(file_content)
        return content


unzip('j5f1607276.gz')