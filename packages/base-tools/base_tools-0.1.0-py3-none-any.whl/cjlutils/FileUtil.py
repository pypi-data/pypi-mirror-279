import os
import zipfile
import shutil


def create_dir(dir_path: str, create_parent: bool = True) -> bool:
    """
    创建目录
    :param dir_path: 目录路径
    :param create_parent: 是否创建父目录
    """
    if dir_path is None or dir_path == '':
        return False
    if create_parent:
        os.makedirs(dir_path, exist_ok=True)
        return True
    else:
        parent_dir = get_parent_dir(dir_path, 1)
        if not is_dir(parent_dir):
            return False
        os.mkdir(dir_path)
        return True


def create_file(file_path: str, content: str = None, create_parent: bool = True) -> bool:
    """
    创建文件
    :param file_path: 文件路径
    :param content: 文件内容
    :param create_parent: 是否创建父目录
    """
    if file_path is None or file_path == '':
        return False
    parent_dir = os.path.dirname(file_path)

    if create_parent:
        create_dir_result = create_dir(parent_dir, True)
        if not create_dir_result:
            return False
    if not is_dir(parent_dir):
        return False
    with open(file_path, 'w') as f:
        if content is not None:
            f.write(content)
    return True


def exists(path: str) -> bool:
    """
    判断路径是否存在
    :param path: 路径
    :return: 是否存在
    """
    if path is None or path == '':
        return False
    return os.path.exists(path)


def get_file_list(dir_path: str, suffix: str = None, recursive: bool = False) -> list[str]:
    """
    获取指定目录下的所有文件路径
    :param dir_path: 目录路径
    :param suffix: 文件后缀名
    :param recursive: 是否递归查找
    :return: 文件路径组成的列表
    """
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if suffix is not None and not file.endswith(suffix):
                continue
            file_list.append(os.path.join(root, file))
        if not recursive:
            break
    return file_list


def get_file_name(path: str) -> str:
    """
    获取文件名
    :param path: 文件路径
    :return: 文件名
    """
    if path is None or path == '':
        return ''
    return os.path.basename(path)


def get_parent_dir(path: str, level: int = 1) -> str:
    """
    获取指定路径的父目录
    :param path: 路径
    :param level: 父目录层级
    :return: 父目录路径
    """
    for _ in range(level):
        path = os.path.dirname(path)
    return path


def is_dir(path: str) -> bool:
    """
    判断路径是否为目录
    :param path: 路径
    :return: 是否为目录
    """
    if path is None or path == '':
        return False
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    """
    判断路径是否为文件
    :param path: 路径
    :return: 是否为文件
    """
    if path is None or path == '':
        return False
    return os.path.isfile(path)


def md5_file(file_path: str) -> str:
    """
    获取文件的MD5值
    :param file_path: 文件路径
    :return: MD5值
    """
    import hashlib
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def remove_dir(dir_path: str):
    """
    删除目录
    :param dir_path: 目录路径
    """
    shutil.rmtree(dir_path)


def remove_file(file_path: str):
    """
    删除文件
    :param file_path: 文件路径
    """
    os.remove(file_path)


def unzip_file(zip_path: str, out_dir: str):
    """
    解压指定文件
    :param zip_path: 压缩文件路径
    :param out_dir: 输出的目录路径
    """
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(out_dir)


def zip_files(paths: list[str], out_path: str, compression: int = zipfile.ZIP_STORED):
    """
    压缩指定文件
    :param paths: 文件路径组成的列表
    :param out_path: 输出的压缩文件的路径
    :param compression: 压缩方式
                ZIP_STORED = 0 # 不进行实际的压缩。它只是将文件原样打包到 ZIP 归档中，适用于已经经过其他压缩算法压缩的文件，或者对于不需要进一步压缩的文件。
                ZIP_DEFLATED = 8 # 使用 DEFLATE 算法进行压缩，通常可以提供较好的压缩比。
                ZIP_BZIP2 = 12 # 使用 BZIP2 算法进行压缩。BZIP2 通常比 DEFLATED 提供更好的压缩效果，但压缩和解压缩的速度可能会稍慢一些。
                ZIP_LZMA = 14 # 使用 LZMA 算法进行压缩。LZMA 通常能够提供更高的压缩比，但可能需要更多的计算资源来压缩和解压缩。
    :return:
    """
    zip_file = zipfile.ZipFile(out_path, "w", compression, allowZip64=True)

    for path in paths:
        pre_len = len(os.path.dirname(path))
        arc_name = path[pre_len:].strip(os.path.sep)
        zip_file.write(path, arc_name)
    zip_file.close()
