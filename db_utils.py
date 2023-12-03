import pandas as pd
import psycopg2
import yaml

class RDSDatabaseConnector:

    def __init__(self, dict_cred):
        self.dict_cred = dict_cred

    
    def data_extract_from_RDS(self):
        conn = psycopg2.connect(
                     host = self.dict_cred['RDS_HOST'],
                     database = self.dict_cred['RDS_DATABASE'],
                     user = self.dict_cred['RDS_USER'],
                     password = self.dict_cred['RDS_PASSWORD'],
                     port = self.dict_cred['RDS_PORT'])
        cur = conn.cursor()
        cur.execute("Select * FROM loan_payments")
        colnames = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        loan_payments = pd.DataFrame(data, columns = colnames)
        conn.close()
        return loan_payments



def load_dict_of_credentials():
    with open("credentials.yaml", "r") as yaml_cred:
        try:
            dict_cred = yaml.safe_load(yaml_cred)
            return dict_cred
        except yaml.YAMLError as exc:
            print(exc)


dict_cred = load_dict_of_credentials()
chloe = RDSDatabaseConnector(dict_cred)
loan_payments = chloe.data_extract_from_RDS()

def save_data_to_csv(loan_payments):
    loan_payments.to_csv('loan_payments.csv')

def load_data_to_df():
    df = pd.read_csv('loan_payments.csv', index_col =0)
    print(df.shape)

save_data_to_csv(loan_payments)
load_data_to_df()
