#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import numpy as np
from sklearn.utils import resample
import pandas as pd

class KappaCalculator:
    """
    A class for calculating Cohen's kappa and Fleiss' kappa.

    Parameters:
    - y: The input data. It can be either a pandas DataFrame or a list.
    - infmt: The format of the input data. Allowed values are 'sample_list', 'sample_df', 'count_sq_df', and 'count_df'.
    - stringna: The string representation of missing values.

    Methods:
    - bootstrap_cohen_ci(n_iterations, confidence_level, outfmt, out_digits): Calculates the bootstrap confidence interval for Cohen's kappa.

    """

    def __init__(self, y, infmt='sample_list', stringna="stringna"):
        """
        Initializes the KappaCalculator object.

        Parameters:
        - y: The input data. It can be either a pandas DataFrame or a list.
        - infmt: The format of the input data. Allowed values are 'sample_list', 'sample_df', 'count_sq_df', and 'count_df'.
        - stringna: The string representation of missing values.

        Raises:
        - ValueError: If the value of infmt is invalid.
        - AssertionError: If the input data does not meet the required conditions.

        """

        assert isinstance(y, (pd.DataFrame, list)), "y must be either a pandas DataFrame or a list"
        if isinstance(y, pd.DataFrame):
            assert y.ndim == 2, "y must be a 2-dimensional DataFrame"
            assert y.shape[0] >= 2 and y.shape[1] >= 2, "y must be a pd.DataFrame with at least 2 columns and 2 rows"
        else:
            assert isinstance(y, list) and len(y) >= 2, "y must be a list with at least 2 elements"
            assert all(isinstance(x, list) for x in y), "all elements of y must be lists"
            assert all(isinstance(x, (str, int)) for sublist in y for x in sublist if x is not None), "all elements of y must be strings or numbers"
            assert all(len(x) == len(y[0]) for x in y), "all sublists in y must have the same length"

        if infmt not in ['sample_list', 'sample_df', 'count_sq_df', 'count_df']:
            raise ValueError("Invalid value for infmt. Allowed values are 'sample_list', 'sample_df', 'count_sq_df' and 'count_df'.")

        if infmt == 'sample_list' or infmt == 'sample_df':
            if infmt == 'sample_list':
                self.y_list = self.__convert_2dlist_to_string(y, stringna=stringna)
                self.y_df = pd.DataFrame(self.y_list).T
            else:
                self.y_df = y.replace({np.nan: stringna, None: stringna})
                self.y_df = self.y_df.applymap(lambda x: str(x) if isinstance(x, (int, float)) else x)
                self.y_list = self.y_df.values.tolist()

            self.y_count = self.y_df.apply(pd.Series.value_counts, axis=1).fillna(0)
            self.category = self.y_count.columns
            self.n_rater = len(self.y_list)
            self.n_category = len(self.category)

            if self.n_category == 2:
                self.y_count_sq = pd.crosstab(self.y_list[0], self.y_list[1], margins = False, dropna=False)
                i = self.y_count_sq.index.union(self.y_count_sq.columns, sort=True)
                self.y_count_sq.reindex(index=i, columns=i, fill_value=0)
            else:
                self.y_count_sq = None

        elif infmt == 'count_sq_df':
            assert y.shape[0] == y.shape[1], "y must be a square DataFrame"
            self.y_count_sq = y
            self.category = y.columns
            self.n_category = len(self.category)
            self.n_rater = 2
            tmp_count = self.y_count_sq.unstack().reset_index(name='count')
            self.y_df = tmp_count.loc[np.repeat(tmp_count.index.values, tmp_count['count'])]
            self.y_df.drop(columns='count', inplace=True)
            self.y_list = self.y_df.values.tolist()
            self.y_count = self.y_df.apply(pd.Series.value_counts, axis=1).fillna(0)

        elif infmt == 'count_df':
            tmp_row_sum = y.sum(axis=1) 
            assert tmp_row_sum.eq(tmp_row_sum[0]).all(), "Row sums of y must be equal"
            self.y_count = y
            self.category = y.columns
            self.n_rater = tmp_row_sum[0]
            self.n_category = len(self.category)
            self.y_count_sq= None
            self.y_list = None
            self.y_df = None

        else:
            self.y_list = None
            self.y_df = None
            self.y_count= None
            self.y_count_sq= None
            self.category = None
            self.n_rater = None
            self.n_category = None
            return

        if self.y_count is not None:
            if stringna in self.y_count.columns:
                column_values = self.y_count[stringna].unique()
                assert len(column_values) == 1, f"All values in column '{stringna}' must be the same"
                self.y_count.drop(columns=stringna, inplace=True)

        if self.n_rater == 2:
            if self.y_list is not None:
                self.cohen_kappa = self.__calculate_cohen_kappa(self.y_list[0],self.y_list[1])
            else:
                self.cohen_kappa = None
        else:
            self.cohen_kappa = None
        
        if self.n_rater >= 2:
            if self.y_count is not None:
                self.fleiss_kappa = self.__calculate_fleiss_kappa(self.y_count)
            else:
                self.fleiss_kappa = None
        else:
            self.fleiss_kappa = None

        return
            
    @staticmethod
    def __convert_2dlist_to_string(y=[], stringna=""):
        for i in range(len(y)):
            if any(isinstance(x, (int)) for x in y[i]):
                y[i] = [str(x) if x is not None else stringna for x in y[i]]
        return y

    @staticmethod
    def __calculate_cohen_kappa(y1, y2):
        total_pairs = len(y1)
        observed_agreement = sum(1 for i in range(total_pairs) if y1[i] == y2[i]) / total_pairs
        unique_labels = set(y1 + y2)
        expected_agreement = sum((y1.count(label) / total_pairs) * (y2.count(label) / total_pairs) for label in unique_labels)
        return (observed_agreement - expected_agreement) / (1 - expected_agreement)

    @staticmethod
    def __calculate_fleiss_kappa(y):

        nR = y.values.sum()
        p = y.values.sum(axis = 0)/nR
        Pbar_E = (p ** 2).sum()
        R = y.values.sum(axis = 1)[0]
        Pbar_O = (((y ** 2).sum(axis=1) - R) / (R * (R - 1))).mean()

        return (Pbar_O - Pbar_E) / (1 - Pbar_E)

    def bootstrap_cohen_ci(self, n_iterations=1000, confidence_level=0.95, outfmt='string', out_digits=6):
        assert isinstance(n_iterations, int) and n_iterations > 1, "n_iterations must be an integer greater than 1"
        assert isinstance(confidence_level, (float)) and 0 < confidence_level < 1, "confidence_level must be a number between 0 and 1"

        if self.n_rater != 2:
            return []

        y1 = self.y_list[0]
        y2 = self.y_list[1]
        kappa_values = []
        idx = range(len(y1))
        for _ in range(n_iterations):
            idxr = resample(idx)
            y1r = [y1[i] for i in idxr]
            y2r = [y2[i] for i in idxr]

            kappa = self.__calculate_cohen_kappa(y1r, y2r)
            kappa_values.append(kappa)

        lower_percentile = (1 - confidence_level) / 2
        upper_percentile = 1 - lower_percentile
        lower_bound = np.percentile(kappa_values, lower_percentile * 100)
        upper_bound = np.percentile(kappa_values, upper_percentile * 100)
        if outfmt=='string':
            return "Cohen's kappa: {:.{}f}".format(self.cohen_kappa, out_digits) + "\nConfidence Interval ({}%): [{:.{}f}, {:.{}f}]".format(confidence_level * 100, lower_bound, out_digits, upper_bound, out_digits)
        else:
            return [self.cohen_kappa, n_iterations, confidence_level, lower_bound, upper_bound]

if __name__ == "__main__":
    pass
