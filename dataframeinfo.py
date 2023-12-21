import pandas as pd
from scipy.stats import normaltest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
tqdm.pandas()

# I will return to add comments and explanations at a later date

class DataFrameInfo:

    def __init__(self, df):
        self.df = df

    def general_info(self):
        print("Dataframe shape is: ", self.df.shape, "\n\n")
        print("The data types of series in the dataframe and non-null counts are: \n")
        print(self.df.info())

    def object_list(self):
        object_df = self.df.select_dtypes(include=['object'])
        object_series = []
        for i in object_df.columns:
            object_series.append(i)
        return object_series

    def object_df(self):
        object_df = self.df.select_dtypes(include=['object'])
        return object_df

    def numerical_list(self):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numerical_df = self.df.select_dtypes(include=numerics)
        numerical_series = []
        for i in numerical_df.columns:
            numerical_series.append(i)
        return numerical_series

    def numerical_df(self):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numerical_df = self.df.select_dtypes(include=numerics)
        return numerical_df 


    def categorical_info(self):
        categorial_df = self.df.select_dtypes(include=['object'])
        categorical_series = self.object_list()
        print("The categorical columns are:", categorical_series)
        for col in categorial_df:
            print(" \n Unique values in", col, ":", categorial_df[col].nunique())

    def category_list(self):
        categorial_df = self.df.select_dtypes(include=['category'])
        categorical_series = []
        for i in categorial_df.columns:
            categorical_series.append(i)
        return categorical_series


    def statistical_info(self, *args):
        pd.options.display.float_format = '{:.3f}'.format
        if args:
            for col_name in args:
                print(f"Mean value for series {col_name}:", self.df[col_name].mean(axis=0, skipna = True, numeric_only= True), "\n")
                print(f"Median value for series {col_name}:", self.df[col_name].median(axis=0, skipna = True, numeric_only= True), "\n")
                print(f"Standard deviation for series {col_name}:", self.df[col_name].std(skipna=True, numeric_only=True), "\n")     
        else:
            print("Mean values for numeric series:\n")
            print(self.df.mean(axis=0, skipna = True, numeric_only= True), "\n")
            print("Median values for numeric series:\n")
            print(self.df.median(axis=0, skipna = True, numeric_only= True), "\n")
            print("Median values for numeric series:\n")
            print(self.df.std(skipna=True, numeric_only=True)) 

    def null_info(self, *args):
        if args:
            for col_name in args:
                percentage_of_nan_col = round((self.df[col_name].isnull().sum()/len(self.df.index))*100, 2)
                print(f"Percentage of null values in {col_name}: ", percentage_of_nan_col)
        else:
            percentage_of_nan = round((self.df.isnull().sum()/len(self.df.index))*100, 2)
            print("The series which contain null values with the percentage of null values are:\n")
            print(percentage_of_nan.loc[percentage_of_nan != 0])

    def normality(self, *args):
        if args:
            for col_name in args:
                data = self.df[col_name]
                stat, p = normaltest(data, nan_policy='omit')
                print('Statistics=%.3f, p=%.3f' % (stat, p))

    def skewed_info(self):
        numerical_series = self.numerical_list()
        for col_name in numerical_series:
            print(f'Skew of {col_name}: ', round(self.df[col_name].skew(),2))
            
    
    def threshold_skew_list(self, non_skew_list, threshold):
        numerical_series = self.numerical_list()
        skewed_columns = []
        for col_name in numerical_series:
            skewness = self.df[col_name].skew() 
            if col_name not in non_skew_list and skewness >= threshold:
                skewed_columns.append(col_name)
            else:
                continue
        return skewed_columns

    def get_positive_negative_cols(self, threshold_skewed_columns):
        pos_threshold_col = []
        neg_threshold_col = []
        for col_name in threshold_skewed_columns:
            if (self.df[col_name] <=0).values.any() == False:
                pos_threshold_col.append(col_name)
            else:
                neg_threshold_col.append(col_name)
        return pos_threshold_col, neg_threshold_col

    def col_value_counts(self, col_name):
        return self.df[col_name].value_counts() / len(self.df)

    def col_percentage(self, col1, col2):
        col1_total = self.df[col1].sum()
        col2_total = self.df[col2].sum()
        percentage = round(col1_total / col2_total * 100, 2)
        return col1_total, col2_total, percentage

    def value_col_percentage(self, value1, col1, col2, int):
        total1 = value1 + self.df[col1].sum()
        total2 = self.df[col2].sum()
        percentage = round(total1 / total2 * 100, 2)
        print(f'Total funded amount recovered at the end of {int} months: {percentage}%')
        return percentage

    def col_percentage_prediction(self, col_list, col1, col2, int):
        df_query = self.df.copy()
        df_query = df_query[df_query['loan_status'].isin(col_list)]
        total1 = df_query[col1].sum() * int
        total2 = df_query[col2].sum()
        percentage = round(total1 / total2 * 100, 2)
        print(f'Loan repayment instalments from open accounts over the next {int} months represent {percentage}% of the total funded amount')
        return total1

    def add_months(self, start_date, delta_period):
        end_date = start_date + relativedelta(months=delta_period)
        return end_date

    def projected_collections_current(self, col_list):
        projected_df = self.df.copy()
        projected_df = projected_df[projected_df['loan_status'].isin(col_list)]
        projected_df['loan_end_date'] = projected_df.apply(lambda row: self.add_months(row["issue_date"], row["term"]), axis = 1)
        projected_df['loan_months_left'] = projected_df['loan_end_date'].dt.to_period('M').astype(int) - projected_df['last_payment_date'].dt.to_period('M').astype(int)
        projected_df.loc[projected_df['loan_months_left'].between(6, 100), 'loan_recovery_6_months'] = projected_df['instalment']*6
        projected_df.loc[projected_df['loan_months_left'].between(0, 6), 'loan_recovery_6_months'] = projected_df['instalment']*projected_df['loan_months_left']
        six_month_recovery_total = projected_df['loan_recovery_6_months'].sum() 
        total_rev_return_all_accounts = self.df['expected_rev_return'].sum()
        total_funded_amount_all_accounts = self.df['funded_amount'].sum()
        total_payment_so_far_all_accounts = self.df['total_payment'].sum()
        total_projected_revenue = round(six_month_recovery_total + total_payment_so_far_all_accounts, 2)
        percentage_total_rev_all_accounts = round(six_month_recovery_total / total_rev_return_all_accounts * 100, 2)
        percentage_funded_amount_all_accounts = round(six_month_recovery_total / total_funded_amount_all_accounts * 100, 2)
        print(f'The percentage of projected revenue over the next six months of the total funded amount for all accounts is {percentage_funded_amount_all_accounts}%. \nThis represents {percentage_total_rev_all_accounts}% of the total expected amount from all accounts including interest.\n\n')
        print(f'Alongside the total payments so far for all accounts, the recovery funds in six months would total £{total_projected_revenue}.')
        return percentage_total_rev_all_accounts, percentage_funded_amount_all_accounts

    def percentage_of_charged_off(self):
        amount_charged_off = len(self.df[self.df['loan_status']=='Charged Off'])
        percentage_of_charged_off = round(amount_charged_off / len(self.df) * 100, 2)
        print(f'Percentage of loans which are charged off: {percentage_of_charged_off}%')
        charged_off_df = self.df.copy()
        charged_off_df = charged_off_df.loc[charged_off_df['loan_status'] == 'Charged Off']
        total_payment_charged_off_so_far = round(charged_off_df['total_payment'].sum(), 2)
        total_funded_amount_charged_off = round(charged_off_df['funded_amount'].sum(), 2)
        total_expected_rev_charged_off = round(charged_off_df['expected_rev_return'].sum(), 2)
        percentage_paid_charged_off_funded_amount = round(total_payment_charged_off_so_far / total_funded_amount_charged_off * 100, 2)
        percentage_paid_charged_off_exp_rev = round(total_payment_charged_off_so_far / total_expected_rev_charged_off *100, 2)
        print(f'Total amount paid towards loans which are now charged off: £{total_payment_charged_off_so_far}')
        print(f'The percentage of charged off loans that was recovered to the total funded amount for these loans is is {percentage_paid_charged_off_funded_amount}%.\nThis represents {percentage_paid_charged_off_exp_rev}% of the total expected amount for charged off loans including interest')
        return percentage_paid_charged_off_funded_amount, total_payment_charged_off_so_far, total_funded_amount_charged_off

    def risky_loans_total_payment(self, risky_category_list):
        risky_df = self.df.copy()
        risky_df = risky_df[risky_df['loan_status'].isin(risky_category_list)]
        total_payment_risky = round(risky_df['total_payment'].sum(), 2)
        total_funded_amount_risky = round(risky_df['funded_amount'].sum(), 2)
        total_exp_rev_risky = round(risky_df['expected_rev_return'].sum(), 2)
        percentage_funded_amount_risky = round(total_payment_risky / total_funded_amount_risky * 100, 2)
        percentage_exp_rev_risky =  round(total_payment_risky / total_exp_rev_risky *100, 2)
        print(f'Total amount paid so far towards loans which are considered risky and would represent a loss if charged off is: £{total_payment_risky}')
        print(f'This represents {percentage_funded_amount_risky}% of the funded amount for these risky loans and {percentage_exp_rev_risky}% of the total expected revenue.')

    def default_loan_projections(self):
        default_df = self.df.copy()
        default_df = default_df.loc[default_df['loan_status'] == 'Default']

       

    def percentage_of_all_category(self, col_name, category_list):
        category_percentage_list = []
        category_count_list = []
        for i in category_list:
            count_category = len(self.df[self.df[col_name]==i])
            percentage_category = round(count_category / len(self.df)*100, 2)
            category_percentage_list.append(percentage_category)
            category_count_list.append(count_category)
        #for i, j, k in zip(category_list, category_percentage_list,category_count_list):
        #    print(f'Percentage of loan status {i}: {j}%')
        #    print(f'Number of loans with loan status {i}: {k} \n')
        return category_percentage_list, category_count_list
    
    def percentage_of_open_category(self, col_name, open_category_list):
        open_loan_status_df = self.df.copy()
        open_loan_status_df = open_loan_status_df[open_loan_status_df[col_name].isin(open_category_list)]
        category_percentage_list = []
        category_count_list = []
        for i in open_category_list:
            count_category = len(self.df[self.df[col_name]==i])
            percentage_category = round(count_category / len(open_loan_status_df)*100, 2)
            category_percentage_list.append(percentage_category)
            category_count_list.append(count_category)
        for i, j, k in zip(open_category_list, category_percentage_list,category_count_list):
            print(f'Percentage of loan status {i}: {j}%')
            print(f'Number of loans with loan status {i}: {k} \n')
        return category_percentage_list, category_count_list


    def projected_loss_from_category(self, cat_name, dataframe):
        dataframe['loan_end_date'] = dataframe.apply(lambda row: self.add_months(row["issue_date"], row["term"]), axis = 1)
        dataframe['loan_months_left'] = dataframe['loan_end_date'].dt.to_period('M').astype(int) - dataframe['last_payment_date'].dt.to_period('M').astype(int)
        dataframe['projected_loss'] = dataframe['loan_months_left'] * dataframe['instalment']
        projected_loss = round(dataframe['projected_loss'].sum(), 2)
        total_funded = self.df['funded_amount'].sum()
        exp_rev = self.df['expected_rev_return'].sum()
        exp_rev_cat = dataframe['expected_rev_return'].sum()
        percentage_loss_funded_amount = round(projected_loss / total_funded * 100, 2)
        percentage_loss_exp_rev = round(projected_loss / exp_rev * 100, 2)
        percentage_loss_exp_rev_cat =  round(projected_loss / exp_rev_cat *100, 2)
        print(f'The projected loss from {cat_name} loans would be: £{projected_loss}')
        print(f'This would represent {percentage_loss_funded_amount}% of the total funded amount and {percentage_loss_exp_rev}% of the total expected revenue including interest')
        print(f'This also represents {percentage_loss_exp_rev_cat}% of the total expected revenue for {cat_name} loans')
        return percentage_loss_funded_amount, percentage_loss_exp_rev, percentage_loss_exp_rev_cat


    def projected_possible_loss(self, cat_name, risky_category_list, open_category_list):
        open_df = self.df.copy()
        open_df = open_df[open_df['loan_status'].isin(open_category_list)]
        risky_df = self.df.copy()
        risky_df = risky_df[risky_df['loan_status'].isin(risky_category_list)]
        risky_df['loan_end_date'] = risky_df.apply(lambda row: self.add_months(row["issue_date"], row["term"]), axis = 1)
        risky_df['loan_months_left'] = risky_df['loan_end_date'].dt.to_period('M').astype(int) - risky_df['last_payment_date'].dt.to_period('M').astype(int)
        risky_df['projected_loss'] = risky_df['loan_months_left'] * risky_df['instalment']
        projected_loss_risky_loans = round(risky_df['projected_loss'].sum(), 2)
        total_funded_risky_loans = risky_df['funded_amount'].sum()
        total_funded_open_accounts = open_df['funded_amount'].sum()
        total_exp_rev_risky_loans = risky_df['expected_rev_return'].sum()
        total_exp_rev_open_accounts = open_df['expected_rev_return'].sum()
        percentage_loss_funded_risky = round(projected_loss_risky_loans / total_funded_risky_loans * 100, 2)
        percentage_loss_exp_risky = round(projected_loss_risky_loans / total_exp_rev_risky_loans *100, 2)
        percentage_loss_funded_open = round(projected_loss_risky_loans / total_funded_open_accounts *100, 2)
        percentage_loss_exp_open = round(projected_loss_risky_loans / total_exp_rev_open_accounts *100, 2)
        print(f'The projected loss from {cat_name} loans to the end of term would be: £{projected_loss_risky_loans}')
        print(f'This represents {percentage_loss_funded_risky}% of the total funded amount and {percentage_loss_exp_risky}% of total expected return of {cat_name} loans')
        print(f'This also represents {percentage_loss_funded_open}% of the total funded amount and {percentage_loss_exp_open}% of total expected return of all open accounts')
        return percentage_loss_exp_risky, percentage_loss_exp_open, projected_loss_risky_loans

    def dataframe_categorical(self):
        late_default_categories =  ['Late (31-120 days)','In Grace Period', 'Late (16-30 days)', 'Default']
        late_default_df = self.df.copy()
        charged_off_df = self.df.copy()
        fully_paid_df = self.df.copy()
        late_default_df = late_default_df[late_default_df['loan_status'].isin(late_default_categories)]
        charged_off_df = charged_off_df.loc[charged_off_df['loan_status'] == 'Charged Off']
        fully_paid_df = fully_paid_df.loc[fully_paid_df['loan_status'] == 'Fully Paid']
        return fully_paid_df, charged_off_df, late_default_df






