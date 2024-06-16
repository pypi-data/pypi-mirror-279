import unittest
from year_extractor.converter import YearExtractor

class TestYearExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = YearExtractor()

    def test_extract_and_convert(self):
        text = "The project started in last year."
        year = self.extractor.extract_and_convert(text)
        print("&&&&&&&&&&&&&year   ",year)

if __name__ == '__main__':
    unittest.main()
