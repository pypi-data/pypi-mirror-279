import pytest
import pandas as pd
import re
from .. import AssessmentAnalysis  # Replace with the actual module name where your class is defined

# Sample data for testing
data = {
    'Surname': ['Smith', 'Johnson', 'Williams', 'Overall average'],
    'Q. 1/1.00': [1, 0.5, 1, 1],
    'Q. 2/5.00': [5, 3, 1, 2]
}

df = pd.DataFrame(data)
df.to_csv("test_data.csv", index=False)


def test_file_read():
    analysis = AssessmentAnalysis("test_data.csv")
    assert analysis.df is not None
    assert len(analysis.df) == 3
    assert analysis.df.shape[1] == 3


def test_info():
    analysis = AssessmentAnalysis("test_data.csv")
    analysis.info()
    assert analysis.n_students is not None
    assert analysis.n_items is not None
    assert analysis.n_students == 3
    assert analysis.n_items == 2


def test_extract_max_marks():
    analysis = AssessmentAnalysis("test_data.csv")
    analysis.filter_columns()
    analysis.extract_max_marks()
    print(analysis.total_max_marks)
    assert analysis.total_max_marks is not None
    assert analysis.total_max_marks == 6


def test_exclude_overall_average():
    analysis = AssessmentAnalysis("test_data.csv")
    analysis.df = analysis.df[analysis.df['Surname'] != 'Overall average']
    assert len(analysis.df) == 3


def test_q_columns_count():
    analysis = AssessmentAnalysis("test_data.csv")
    q_columns = [col for col in analysis.df.columns if 'Q. ' in col]
    assert len(q_columns) == 2


def test_calc_desc():
    analysis = AssessmentAnalysis("test_data.csv")
    analysis.calc_desc()
    assert analysis.mean is not None
    assert analysis.median is not None
    assert analysis.std_dev is not None
    assert analysis.mean == 63.89
    assert analysis.median == 58.33
    assert analysis.std_dev == 33.68
