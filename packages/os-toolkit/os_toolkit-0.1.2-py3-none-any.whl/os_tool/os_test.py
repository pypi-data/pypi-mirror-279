import unittest
from pathlib import Path
import os_01 as ost01

class Test_auto_rename_series(unittest.TestCase):
    path01 = r"H:\D_Video\BigBang Portugues\BigBang PT Season 05_testPython"
    def test_basic01_prefix_no_space(self):
        ost01.auto_rename_series(self.path01,prefix="BigBang PT")
    
    def test_basic01_prefix_with_space(self):
        ost01.auto_rename_series(self.path01,prefix="BigBang PT ")
    
class Test_extract_filename(unittest.TestCase):
    path01_01 = r'H:\\D_Video\\The Ark Season 01 Portuguese\\The Ark S01E02 PT.mkv'
    path02_01 = r"H:\D_Video\The Ark Season 01 Portuguese\The Ark S01E03 PT.mkv"
    path03_01 = r"H:/D_Video/The Ark Season 01 Portuguese/The Ark S01E04 PT.mkv"

    path04_01 = r"H:/D_Video/The Ark Season 01 Portuguese/The Ark S01.E04. PT.mkv"

    path_list01 = [path01_01,path02_01,path03_01]

    path01_02 = Path(path01_01)
    path02_02 = Path(path02_01)
    path03_02 = Path(path03_01)

    path04_02 = Path(path04_01)

    def test_basice01_with_extension(self):
        actual01 = ost01.extract_filename(self.path01_01)
        actual02 = ost01.extract_filename(self.path02_01)
        actual03 = ost01.extract_filename(self.path03_01)

        expected01 = 'The Ark S01E02 PT.mkv'
        expected02 = 'The Ark S01E03 PT.mkv'
        expected03 = 'The Ark S01E04 PT.mkv'

        self.assertEqual(actual01,expected01)
        self.assertEqual(actual02,expected02)
        self.assertEqual(actual03,expected03)
    
    def test_basice02_list_input(self):
        actual = ost01.extract_filename(self.path_list01)
        expect = ['The Ark S01E02 PT.mkv','The Ark S01E03 PT.mkv','The Ark S01E04 PT.mkv']

        self.assertEqual(actual,expect)
    
    def test_with_path_dot_no_extension(self):
        actual = ost01.extract_filename(self.path04_02,with_extension=False)
        expect = 'The Ark S01.E04. PT'

        msg = f"Input: '{self.path04_02}' \nActual: '{actual}' \nExpect: '{expect}' "
        self.assertEqual(actual,expect,msg)

def test__auto_rename_series():
    path01 = r"H:\D_Video\BigBang Portugues\BigBang PT Season 05_testPython"
    
    ost01.auto_rename_series(path01,prefix="BigBang PT")
    ost01.auto_rename_series(path01,prefix="BigBang PT ")
    
def try_auto_rename_series():
    
    path_list = [
        r"H:\GoogleDrive\The 100\Portuguese\The 100 Season 01 Portuguese",
        r"H:\GoogleDrive\The 100\Portuguese\The 100 Season 02 Portuguese",
        r"H:\GoogleDrive\The 100\Portuguese\The 100 Season 03 Portuguese",
        r"H:\GoogleDrive\The 100\Portuguese\The 100 Season 04 Portuguese",
        r"H:\GoogleDrive\The 100\Portuguese\The 100 Season 05 Portuguese",
    ]
    for folder in path_list:
        ost01.auto_rename_series(folder,prefix="The 100 PT_")

if __name__ == '__main__':
    # unittest.main()
    # test__auto_rename_series()
    try_auto_rename_series()

