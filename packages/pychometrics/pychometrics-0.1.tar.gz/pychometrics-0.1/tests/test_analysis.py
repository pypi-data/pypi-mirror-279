# tests/test_analysis.py
import unittest
import pandas as pd
from assessment_analysis import AssessmentAnalysis

class TestAssessmentAnalysis(unittest.TestCase):
    def setUp(self):
        data = {
            'Q. 1 /5.00': [1, 2, 3],
            'Q. 2 /5.00': [4, 5, 6],
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'Q. 3 /1.00': [7, 8, 9],
            'Facility Index': [0.12345, 0.67891, 0.23456],
            'Discrimination Index': [1.23456, 2.34567, 3.45678]
        }
        df = pd.DataFrame(data)
        df.to_csv('test_data.csv', index=False)
        self.analysis = AssessmentAnalysis('test_data.csv')

    def test_filter_columns(self):
        self.analysis.filter_columns()
        self.assertIn('Q. 1 /5.00', self.analysis.marks_df.columns)
        self.assertNotIn('Name', self.analysis.marks_df.columns)

    def test_extract_max_marks(self):
        self.analysis.filter_columns()
        self.analysis.extract_max_marks()
        self.assertEqual(self.analysis.total_max_marks, 11.0)

    def test_calculate_totals(self):
        self.analysis.filter_columns()
        self.analysis.extract_max_marks()
        self.analysis.calculate_totals()
        self.assertIn('Total', self.analysis.marks_df.columns)
        self.assertIn('Total_Percentage', self.analysis.marks_df.columns)

    def test_calculate_statistics(self):
        self.analysis.run_analysis()
        self.assertIsInstance(self.analysis.mean, float)
        self.assertIsInstance(self.analysis.median, float)
        self.assertIsInstance(self.analysis.std_dev, float)
        self.assertIsInstance(self.analysis.skewness, float)
        self.assertIsInstance(self.analysis.kurt, float)

    def test_generate_report(self):
        self.analysis.run_analysis()
        with open('report.txt', 'r') as file:
            content = file.read()
            self.assertIn("Marks DataFrame:", content)
            self.assertIn("Total Max Marks:", content)
            self.assertIn("Item Analysis:", content)

if __name__ == '__main__':
    unittest.main()
