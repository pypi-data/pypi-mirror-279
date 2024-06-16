import unittest
import pandas as pd
from plotvizard.data_processing import load_data, filter_data

class TestDataProcessing(unittest.TestCase):

    def test_load_data(self):
        df = load_data('tests/sample_data.csv')
        self.assertIsInstance(df, pd.DataFrame)

    def test_filter_data(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'a']})
        filtered_df = filter_data(df, B='a')
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(filtered_df['B'] == 'a'))

if __name__ == '__main__':
    unittest.main()
