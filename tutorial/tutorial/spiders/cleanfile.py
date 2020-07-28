import pandas as pd

path = "singapore_pharmaceuticals_contact.csv"

phdf = pd.read_csv("ph_" + path, index_col=0)
phdf.columns = ['phone', 'link']
phdf = phdf.drop_duplicates(subset='phone')
phdf = phdf.reset_index(drop=True)
phdf.to_csv("ph_" + path, mode='w', header=True)