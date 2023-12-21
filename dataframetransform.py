import pandas as pd
from sklearn.impute import KNNImputer
from scipy import stats
from scipy.stats import yeojohnson
from scipy import stats
import numpy as np

# I will return to add comments and explanations at a later date


class DataFrameTransform:

    def __init__(self, df):
        self.df = df

    def find_col_nonzero_nan(self):
        col_nan_count = []
        col_nonzero_nan = []
        for col in self.df.columns:
            percentage_of_nan_col = round((self.df[col].isnull().sum()/len(self.df.index))*100, 2)
            list_element = [col, percentage_of_nan_col]
            col_nan_count.append(list_element)
        col_nonzero_nan = [x for x in col_nan_count if x[1] != 0]
        return col_nonzero_nan


    def drop_col_conditional(self, str, value):
        col_nonzero_nan = self.find_col_nonzero_nan()
        for i in col_nonzero_nan:
            if str == '>':
                col_nan_count_conditional = [i[0] for i in col_nonzero_nan if i[1] >= value]
            elif str == '<':
                col_nan_count_conditional = [i[0] for i in col_nonzero_nan if i[1] <= value]
            elif str == '=':
                col_nan_count_conditional = [i[0] for i in col_nonzero_nan if i[1] == value]
            else:
                print("Include an conditional operator >, < or = and a value to compare the NaN percentage to")
                print("The columns which satisfy this conditional statement are:", col_nan_count_conditional)
        for col in col_nan_count_conditional:
            if col in self.df.columns:
                self.df.drop(col, axis=1, inplace=True)
        df = self.df
        return df

    def drop_col(self, *args):
        if args:
            for col_name in args:
                self.df.drop(col_name, axis=1, inplace=True)
        df = self.df
        return df


    def drop_row_conditional(self, str, value):
        col_nonzero_nan = self.find_col_nonzero_nan()
        if str == '>':
            col_nan_count_conditional = [i[0] for i in col_nonzero_nan if i[1] >= value]
        elif str == '<':
            col_nan_count_conditional = [i[0] for i in col_nonzero_nan if i[1] <= value]
        elif str == '=':
            col_nan_count_conditional = [i[0] for i in col_nonzero_nan if i[1] == value]
        else:
            print("Include an conditional operator >, < or = and a value to compare the NaN percentage to")
        print("The columns which satisfy this conditional statement are: \n", col_nan_count_conditional)
        for col in col_nan_count_conditional:
            if col in self.df.columns:
                self.df.dropna(subset=col, inplace=True)
        df = self.df
        return df
    
    def replace_na_categorical(self, col_name, str):
        self.df[col_name].fillna(str, inplace=True)

    def impute_with_another_col(self, col1, col2):
        #Replace any NaN values in col1 with the corresponding values in col2.
        self.df[col1] = self.df[col1].fillna(self.df[col2])

    def impute_with_median(self, *args):
        if args:
            for col_name in args:
                self.df[col_name] = self.df[col_name].fillna(self.df[col_name].median())
            
    def box_cox_transform(self, col_name):
        boxcox_population = stats.boxcox(self.df[col_name])
        boxcox_population= pd.Series(boxcox_population[0])  
        self.df[col_name] = boxcox_population.values

    def yeo_johnson_transform(self, col_name):
        yeojohnson_population = stats.yeojohnson(self.df[col_name])
        yeojohnson_population = pd.Series(yeojohnson_population[0])

        self.df[col_name] = yeojohnson_population.values

    def drop_outliers(self, col_name, z_threshold):
        z = np.abs(stats.zscore(self.df[col_name]))
        outliers = self.df[z > z_threshold]
        self.df = self.df.drop(outliers.index)
        df = self.df
        return df



