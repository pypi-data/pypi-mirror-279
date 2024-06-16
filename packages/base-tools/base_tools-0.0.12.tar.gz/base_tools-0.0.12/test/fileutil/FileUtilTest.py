import os.path
import shutil
import unittest

from src.cjlutils import FileUtil

base_dir = './temp'


class CreateDirTest(unittest.TestCase):
    def test_create_none(self):
        self.assertFalse(FileUtil.create_dir(None))

    def test_create_empty(self):
        self.assertFalse(FileUtil.create_dir(''))

    def test_create_exists(self):
        dir = f'{base_dir}/test'
        self.assertFalse(os.path.exists(dir))
        self.assertTrue(FileUtil.create_dir(dir))
        self.assertTrue(os.path.exists(dir))

        # 目录已经存在，再次创建
        self.assertTrue(FileUtil.create_dir(dir))
        self.assertTrue(os.path.exists(dir))
        shutil.rmtree(dir)
        self.assertFalse(os.path.exists(dir))

    def test_parent_not_exists_and_create(self):
        parent_dir = f'{base_dir}/parent'
        dir = f'{parent_dir}/test'
        self.assertFalse(os.path.exists(parent_dir))
        self.assertFalse(os.path.exists(dir))
        self.assertTrue(FileUtil.create_dir(dir))
        self.assertTrue(os.path.exists(dir))
        shutil.rmtree(parent_dir)
        self.assertFalse(os.path.exists(dir))

    def test_parent_not_exists_and_no_create(self):
        parent_dir = f'{base_dir}/parent'
        dir = f'{parent_dir}/test'
        self.assertFalse(os.path.exists(parent_dir))
        self.assertFalse(os.path.exists(dir))
        self.assertFalse(FileUtil.create_dir(dir, create_parent=False))
        self.assertFalse(os.path.exists(parent_dir))


class CreateFileTest(unittest.TestCase):
    def test_create_none(self):
        self.assertFalse(FileUtil.create_file(None))

    def test_create_empty(self):
        self.assertFalse(FileUtil.create_file(''))
        self.assertFalse(os.path.exists(''))

    def test_file_creation(self):
        file_path = f'{base_dir}/test.txt'
        content = "This is a test content."
        self.assertFalse(os.path.exists(file_path))

        FileUtil.create_file(file_path, content, create_parent=True)
        self.assertTrue(os.path.isfile(file_path))

        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))

    def test_file_content(self):
        file_path = f'{base_dir}/test.txt'
        content = "This is a test content."
        self.assertFalse(os.path.exists(file_path))

        FileUtil.create_file(file_path, content, create_parent=True)
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEqual(file_content, content)

        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))

    def test_file_content_None(self):
        file_path = f'{base_dir}/test.txt'
        content = None
        self.assertFalse(os.path.exists(file_path))

        FileUtil.create_file(file_path, content, create_parent=True)
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEqual(file_content, '')

        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))

    def test_no_parent_creation(self):
        dir = f'{base_dir}/test'
        file_path = f'{dir}/test.txt'
        content = "This is a test content."
        FileUtil.create_file(file_path, content, create_parent=False)
        self.assertFalse(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
