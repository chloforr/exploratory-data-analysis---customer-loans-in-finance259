import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot
import numpy as np
from scipy import stats
from scipy.stats import yeojohnson

# I will return to add comments and explanations at a later date


class Plotter:

    def __init__(self, df):
        self.df = df
    
    def numerical_df(self):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numerical_df = self.df.select_dtypes(include=numerics)
        return numerical_df 

    def visualise_nulls(self):
        plt.figure(figsize=(10,6))
        sns.heatmap(self.df.isna(),
            cmap=sns.cubehelix_palette(as_cmap=True),
            cbar_kws={'label': 'Missing Data'})
        plt.show()

    def plot_histogram(self, *args):
        if args:
            for col_name in args:
                self.df[col_name].hist(bins=25)
                plt.show()
        else:
            self.df.hist(bins=25)
            plt.show()

    def col_qq_plot(self, *args):
        numerical_df = self.numerical_df()
        if args:
            for col_name in args:
                qq_plot = qqplot(self.df[col_name] , scale=1 ,line='q')
        pyplot.show()

    def df_qq_plot(self):
        numerical_df = self.numerical_df()
        for col_name in numerical_df.columns:
            qq_plot = qqplot(numerical_df[col_name], scale=1 ,line='q')
        pyplot.show()

    def check_correlation(self, *args):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numerical_df = self.df.select_dtypes(include=numerics)
        col_name_list = []
        plt.figure(figsize=(10,6))
        if args:
            for col_name in args:
                col_name_list.append(col_name)
                sns.heatmap(self.df[col_name_list].corr(), annot=True, cmap='coolwarm')
            plt.show()
        else:
            corr = numerical_df.corr()
            mask = np.zeros_like(corr, dtype=bool)
            mask[np.triu_indices_from(mask)] = True
            sns.heatmap(numerical_df.corr(), mask=mask, annot=True, fmt=',.1f', cmap=sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=True))
            plt.show()

    def plot_skewness(self, *args):
        col_name_list = []
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numerical_df = self.df.select_dtypes(include=numerics)
        if args:
            for col_name in args:
                col_name_list.append(col_name)
                sns.set(font_scale=0.7)
                f = pd.melt(self.df[col_name_list])
                g = sns.FacetGrid(f, col="variable",  col_wrap=3, sharex=False, sharey=False)
                g = g.map(sns.histplot, "value", kde=True)
            pyplot.tight_layout() 
            pyplot.show()
        else:
            sns.set(font_scale=0.7)
            f = pd.melt(numerical_df)
            g = sns.FacetGrid(f, col="variable",  col_wrap=3, sharex=False, sharey=False)
            g = g.map(sns.histplot, "value", kde=True)
            pyplot.tight_layout()
            pyplot.show()
            

    def pos_skew_transforms_and_qq(self, col_name):
        skew_transformed_df = self.df.copy()
        skew_transformed_df['log_transform'] = self.df[col_name].map(lambda i: np.log(i) if i > 0 else 0)
        skew_transformed_df['box_cox'] = pd.Series(stats.boxcox(self.df[col_name])[0]).values


        fig, axes = pyplot.subplots(nrows=2, ncols= 3, figsize=(16, 8))

        axes[0, 0].set_title('Original', fontsize=16)
        axes[0, 1].set_title('Log Transformed', fontsize=16)
        axes[0, 2].set_title('Box-Cox Transformed', fontsize=16)

        axes[1, 0].set_title('Original Q-Q Plot', fontsize=16)
        axes[1, 1].set_title('Log Transformed Q-Q Plot', fontsize=16)
        axes[1, 2].set_title('Box-Cox Transformed Q-Q Plot', fontsize=16)


        sns.set(font_scale=0.7)
        a = sns.histplot(self.df[col_name], label="Skewness: %.2f"%(self.df[col_name].skew()), kde=True, ax=axes[0, 0]) 
        a.legend(fontsize=16) 
        b = sns.histplot(skew_transformed_df['log_transform'], label="Skewness: %.2f"%(skew_transformed_df['log_transform'].skew()), kde=True, ax=axes[0, 1]) 
        b.legend(fontsize=16)
        c = sns.histplot(skew_transformed_df['box_cox'], label="Skewness: %.2f"%(skew_transformed_df['box_cox'].skew()), kde=True, ax=axes[0, 2]) # Box Cox Histogram
        c.legend(fontsize=16) 
            
        stats.probplot(self.df[col_name], plot=axes[1, 0]) 
        stats.probplot(skew_transformed_df['log_transform'], plot=axes[1, 1]) 
        stats.probplot(skew_transformed_df['box_cox'], plot=axes[1, 2]) 
        pyplot.suptitle(col_name, fontsize=24)
        pyplot.tight_layout() 
        return pyplot.show()


    def neg_skew_transforms_and_qq(self, col_name):
        skew_transformed_df = self.df.copy()
        skew_transformed_df['log_transform'] = self.df[col_name].map(lambda i: np.log(i) if i > 0 else 0)
        skew_transformed_df['yeo_johnson'] = pd.Series(stats.yeojohnson(self.df[col_name])[0]).values


        fig, axes = pyplot.subplots(nrows=2, ncols= 3, figsize=(16, 8))

        axes[0, 0].set_title('Original', fontsize=16)
        axes[0, 1].set_title('Log Transform', fontsize=16)
        axes[0, 2].set_title('Yeo-Johnson Transform', fontsize=16)

        axes[1, 0].set_title('Original', fontsize=16)
        axes[1, 1].set_title('Log Transform', fontsize=16)
        axes[1, 2].set_title('Yeo-Johnson Transform', fontsize=16)


        sns.set(font_scale=0.7)
        a = sns.histplot(self.df[col_name], label="Skewness: %.2f"%(self.df[col_name].skew()), kde=True, ax=axes[0, 0]) 
        a.legend(fontsize=16)
        a.set(xlabel= f'{col_name}', ylabel='Count')
        b = sns.histplot(skew_transformed_df['log_transform'], label="Skewness: %.2f"%(skew_transformed_df['log_transform'].skew()), kde=True, ax=axes[0, 1]) 
        b.legend(fontsize=16)  
        c = sns.histplot(skew_transformed_df['yeo_johnson'], label="Skewness: %.2f"%(skew_transformed_df['yeo_johnson'].skew()), kde=True, ax=axes[0, 2]) 
        c.legend(fontsize=16)   
            
            
        stats.probplot(self.df[col_name], plot=axes[1, 0]) 
        stats.probplot(skew_transformed_df['log_transform'], plot=axes[1, 1]) 
        stats.probplot(skew_transformed_df['yeo_johnson'], plot=axes[1, 2]) 
        pyplot.suptitle(col_name, fontsize=24)
        pyplot.tight_layout() 
        return pyplot.show()

    def outlier_box_plot(self, col_names):
        df_melt = self.df.melt(value_vars= col_names)
        facet_grid = sns.FacetGrid(df_melt, col="variable",  col_wrap=5, sharex=False, sharey=False) 
        facet_grid = facet_grid.map(sns.boxplot, "value", flierprops=dict(marker='x', markeredgecolor='red')) # Map box-plot onto each plot on grid.
        pyplot.tight_layout() 

    def outlier_histogram(self, col_names):
        df_melt = self.df.melt(value_vars= col_names)
        facet_grid = sns.FacetGrid(df_melt, col="variable",  col_wrap=1, sharex=False, sharey=False, height =3, aspect=2.5) 
        facet_grid = facet_grid.map(sns.histplot, "value")
        plt.show()

    def outlier_boxplot_comparison(self, df_with_outliers, col_name):
        fig, axes = pyplot.subplots(nrows=1, ncols= 2, figsize=(16, 8))
        axes[0].set_title(f'{col_name} box plot before outlier removal', fontsize=16)
        axes[1].set_title(f'{col_name} box plot after outlier removal', fontsize=16)
        sns.set(font_scale=0.7)

        sns.boxplot(data = df_with_outliers, y=col_name, color='lightgreen', showfliers=True, ax=axes[0], flierprops=dict(marker='x', markeredgecolor='red'))


        sns.boxplot(data = self.df, y=col_name, color='lightgreen', showfliers=True, ax=axes[1], flierprops=dict(marker='x', markeredgecolor='red'))

        pyplot.tight_layout() 
        return pyplot.show()

    def bar_chart(self, value_list, title_list, title, y_label):
        fig = pyplot.subplots(figsize=(16, 8))
        ax = sns.barplot(x=value_list, y = title_list, palette = sns.color_palette("Paired"))
        ax.bar_label(ax.containers[0])
        ax.set(xlabel=y_label)
        pyplot.title(title)
        pyplot.show()

    def two_variable_pie_chart(self, total1, total2, label1, label2, title):
        data = [total1, total2]
        labels = [label1, label2]
        colors = sns.color_palette("Paired")
        plt.pie(data, labels = labels, colors = colors, autopct='%1.1f%%')
        plt.title(title)
        plt.show()

    def loan_status_dataframes(self):
        late_default_categories =  ['Late (31-120 days)','In Grace Period', 'Late (16-30 days)', 'Default']
        late_default_df = self.df.copy()
        charged_off_df = self.df.copy()
        fully_paid_df = self.df.copy()
        late_default_df = late_default_df[late_default_df['loan_status'].isin(late_default_categories)]
        charged_off_df = charged_off_df.loc[charged_off_df['loan_status'] == 'Charged Off']
        fully_paid_df = fully_paid_df.loc[fully_paid_df['loan_status'] == 'Fully Paid']
        return fully_paid_df, charged_off_df, late_default_df

    def risk_identifier_categorical(self, col_name):
        fully_paid_df, charged_off_df, late_default_df = self.loan_status_dataframes()

        fig, axes = pyplot.subplots(nrows=2, ncols= 2, figsize=(16, 8))

        axes[0, 0].set_title('All Loans', fontsize=16)
        axes[0, 1].set_title('Fully Paid Loans', fontsize=16)
        axes[1, 0].set_title('Late and Defaulted Loans', fontsize=16)
        axes[1, 1].set_title('Charged Off Loans', fontsize=16)

        data_all = self.df[col_name].value_counts()
        data_fully_paid = fully_paid_df[col_name].value_counts()
        data_late_default = late_default_df[col_name].value_counts()
        data_charged_off = charged_off_df[col_name].value_counts()
        
        ax1 = sns.barplot(y=data_all.index, x=data_all.values,palette = sns.color_palette("Paired"),  ax=axes[0,0]) # Generate subplot for all loans
        ax2 = sns.barplot(y=data_fully_paid.index, x=data_fully_paid.values, palette = sns.color_palette("Paired"), ax=axes[0,1]) # Generate subplot for fully paid loans
        ax3 = sns.barplot(y=data_late_default.index, x=data_late_default.values, palette = sns.color_palette("Paired"), ax=axes[1,0]) # Generate subplot for charged off and defaulted loans
        ax4 = sns.barplot(y=data_charged_off .index, x=data_charged_off .values, palette = sns.color_palette("Paired"), ax=axes[1,1]) # Ge
        ax1.bar_label(ax1.containers[0])
        ax2.bar_label(ax2.containers[0])
        ax3.bar_label(ax3.containers[0])
        ax4.bar_label(ax4.containers[0])
        ax1.set(xlabel='Count', ylabel = col_name)
        ax2.set(xlabel='Count', ylabel = col_name)
        ax3.set(xlabel='Count', ylabel = col_name)
        ax4.set(xlabel='Count', ylabel = col_name)
        pyplot.tight_layout() 
    

    def risk_identifier_numerical(self, col_name):
        fully_paid_df, charged_off_df, late_default_df = self.loan_status_dataframes()
        fig, axes = pyplot.subplots(nrows=2, ncols= 2, figsize=(16, 8))

        axes[0, 0].set_title('All Loans', fontsize=16)
        axes[0, 1].set_title('Fully Paid Loans', fontsize=16)
        axes[1, 0].set_title('Late and Defaulted Loans', fontsize=16)
        axes[1, 1].set_title('Charged Off Loans', fontsize=16)

        data_all = self.df[col_name]
        data_fully_paid = fully_paid_df[col_name]
        data_late_default = late_default_df[col_name]
        data_charged_off = charged_off_df[col_name]

        ax1 = sns.histplot(data=data_all, label="Mean: %.2f"%(data_all.mean()), kde=True, ax=axes[0, 0])
        ax1.legend(fontsize=16)
        ax2 = sns.histplot(data=data_fully_paid,label="Mean: %.2f"%(data_fully_paid.mean()), kde=True, ax=axes[0, 1]) 
        ax2.legend(fontsize=16)
        ax3 = sns.histplot(data=data_late_default, label="Mean: %.2f"%(data_late_default.mean()),kde=True, ax=axes[1, 0]) 
        ax3.legend(fontsize=16)
        ax4 = sns.histplot(data=data_charged_off, label="Mean: %.2f"%(data_charged_off.mean()),kde=True, ax=axes[1, 1]) 
        ax4.legend(fontsize=16)

        ax1.set(xlabel=col_name, ylabel = 'Count')
        ax2.set(xlabel=col_name, ylabel = 'Count')
        ax3.set(xlabel=col_name, ylabel = 'Count')
        ax4.set(xlabel=col_name, ylabel = 'Count')

        

        ax1.axvline(data_all.mean(), c='orange', ls='--', lw=2.5)
        ax2.axvline(data_fully_paid.mean(), c='orange', ls='--', lw=2.5)
        ax3.axvline(data_late_default.mean(), c='orange', ls='--', lw=2.5)
        ax4.axvline(data_charged_off.mean(), c='orange', ls='--', lw=2.5)

        sns.despine(ax=axes[0, 0])
        sns.despine(ax=axes[0, 1])
        sns.despine(ax=axes[1, 0])
        sns.despine(ax=axes[1, 1])
        pyplot.tight_layout() 




    


        

 


