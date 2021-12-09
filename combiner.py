import pandas as pd
from pathlib import Path
import natsort
import statistics
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-P', '--path',
    default='.',
    dest='path',
    help='Provide a parent path for files. Defaults to .',
    type=str)
args = parser.parse_args()
p = Path(args.path)

def write_combined(results):
    #this aggregates the reulsts from the five reads into one
    df = pd.DataFrame.from_records(results)
    #write data to file
    dft = df.transpose()
    dft.columns = ['pedestals', 'strong_pedestals', 'colonies', 'proportion', 's-proportion', 'colony-ped', 'stregnth', 'area']
    dft.to_csv(p / 'combined_output.csv', sep=',', encoding='utf-8')

print("Reading data and aggregating total data")
df_results = pd.DataFrame()
lista = p.rglob('out.csv')
df = pd.read_csv(next(lista)).transpose()
df2 = pd.read_csv(next(lista)).transpose()
df3 = pd.read_csv(next(lista)).transpose()
df4 = pd.read_csv(next(lista)).transpose()
df5 = pd.read_csv(next(lista)).transpose()

df_results= pd.concat([df,df2,df3,df4,df5])
df_results.to_csv(p / 'total_data.csv', sep=',', encoding='utf-8')


length = df.shape[1]
width = df.shape[0] - 1

names =[]
for i in range(length):
    names.append(df.iloc[0,i])
    #print([i])

print("Calculating median of fields of view data")

reslist = np.empty((width,length), dtype=object)
for i in range(length):
    for j in range(width):
        temp = (df[i][j+1],df2[i][j+1],df3[i][j+1],df4[i][j+1],df5[i][j+1])
        temp = [i for i in temp if not pd.isnull(i)]
        #if len(temp) > 1:
        #    temp.remove(min(temp)) #because the lowest values are the autofocus failure or images with damaged monolayers
        result = (statistics.median(temp))
        #print(temp)
        reslist[j,i] = result


empty_lista= pd.DataFrame(reslist, columns=names)
write_combined(empty_lista)
print("Done!")
