'''
Code to read a structured concentration file and calculate the median values for each point per year
Input files:
* Idrochimica

Author: Pietro Mazzon

'''

# import libraries
import os

import pandas as pd
print('Pandas version: '+pd.__version__) #check version

import numpy as np
print('Numpy version: '+np.__version__) #check version

# set WD
# cwd = os.getcwd()
# print(cwd)
cwd = "c:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/" #my directory

# set input files dir
filepath = os.path.join(cwd,'PerConfronto')
print('La cartella dei file di input è: ',filepath)

# Read the DF
file = 'idrochimica_tutti_step6_SL_31102024'
extension = '.xlsx'
path = os.path.join(filepath,file + extension)
df = pd.read_excel(path)

# Writes DF as csv
writepath = os.path.join(filepath,file + '.csv')
df.to_csv(writepath, index=False)

df.dtypes # variable types
# drop unwanted cols

#df2=df.copy() # for testing

df.drop(
    ['COMUNE', 'Descrizione Punto', 'PUNTO_PRELIEVO', 'Tipo di campione', 'Tipologia di analisi', 
     'Nota Prelievo', 'Nota Prelevatore', 'VALORE_ORIGINE', 'UM', 'FONTE'],
    axis=1, 
    inplace=True
)


print(df.columns)

# check for NaN values

# Checking for missing values using isnull()
df.isnull() # Creates a set of boolean values
df.isnull().sum() # make the sum to count the missing values -> better, summarize

# groupby ID_PUNTO and then by YEAR
#df2=df.copy() # for testing
# create a column "YEAR"
df['ANNO']=df['DATA'].dt.year
#df.describe()
#df.head()
#df.tail()

# groupby and median values
result_grouped = df.groupby(['PARAMETRO','ID_PUNTO','ANNO'])['VALORE_MODIFICATO'].median() #select by PARAMETER, point and by year, then calculates the median of the column valore modificato

result_reset_index = result_grouped.reset_index() # make the series "result" a DF and reset of indexes
result_reset_index.rename(columns={'VALORE_MODIFICATO': 'MEDIANA_ANNO'}, inplace=True)
print(result_reset_index.head(10))

#writepath2 = os.path.join(filepath,'mediane.csv')
result_reset_index.to_excel(os.path.join(filepath, "mediane_annuale_anagrafica_all.xlsx")) # save to excel, in the same filepath as the input file
#print(result_reset_index)