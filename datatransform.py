import pandas as pd

# I will return to add comments and explanations at a later date

class DataTransform:
    def __init__(self, df):
        self.df = df

    def convert_to_period(self, *args): 
        if args:
            for col_name in args:
                self.df[col_name] = pd.to_datetime(self.df[col_name], format = '%b-%Y')
                #self.df[col_name] = self.df[col_name].dt.to_period('M')
        else:
            print("Please enter at least one column name as an argument to the method to convert to a date format")
        return self.df
        

    def str_replace(self, str1, str2):
        df = self.df.replace(str1,str2)
        return df
    
    def object_list(self):
        categorial_df = self.df.select_dtypes(include=['object'])
        categorical_series = []
        for i in categorial_df.columns:
            categorical_series.append(i)
        return categorical_series

    def convert_to_categorical(self):
        object_series = self.df.object_list()
        for col_name in object_series:
            self.df[col_name] = self.df[col_name].astype("category")
            return df






