from distutils.command.config import config
import os
from configparser import ConfigParser
from turtle import fd
import pandas as pd
import re
import gzip
import shutil

configPath = r'C:\Projects\redoak_file_insight\config.ini'
ini_parser = ConfigParser()
ini_parser.read(configPath)
BrandPurchase_regex = '.*BRAND_PURCHASE_.*.gz$'
Purchase_regex = '.*PURCHASE_.*.gz$'
GenericNonSource_regex = '.*GENERIC_NONSOURCE_.*.gz$'
GenericSource_regex = '.*GENERIC_SOURCE_.*.gz$'
filePath = ini_parser.get('FILE_OSS','path')
outputPath = ini_parser.get('FILE_OSS','outputpath')
listFilesAtPath = [filePath+"\\"+fd for fd in os.listdir(filePath)]
fileBrandPurchase = ''
filePurchase = ''
fileGenericNonSource = ''
fileGenericSource = ''

for file in listFilesAtPath:
    if re.match(BrandPurchase_regex, file):
        fileBrandPurchase = file
    if re.match(Purchase_regex, file):
        filePurchase = file
    if re.match(GenericNonSource_regex, file):
        fileGenericNonSource = file
    if re.match(GenericSource_regex, file):
        fileGenericSource = file

df_fileBrandPurchase = pd.read_csv(fileBrandPurchase, compression='gzip', header=0, sep='\t')
df_fileBrandPurchaseMod = df_fileBrandPurchase[['PurchaseDate','PurchaseNumber']].copy()
df_fileBrandPurchaseMod['PurchaseDate'] = pd.to_datetime(df_fileBrandPurchaseMod['PurchaseDate'], errors='coerce')
df_fileBrandPurchaseMod_count_rows = df_fileBrandPurchase.groupby('RecordType').size().reset_index(name='counts')
df_fileBrandPurchaseModAgg= df_fileBrandPurchaseMod.groupby(df_fileBrandPurchaseMod['PurchaseDate'].dt.date)['PurchaseNumber'].agg(['count']).reset_index().rename(columns={'PurchaseDate':'Brand_PurchaseFile_Date', 'count': 'CountofBrand_PurchaseNumbers'})

with pd.ExcelWriter(outputPath+'/Brand_Purchase_log.xlsx', mode='w') as writer:
    df_fileBrandPurchaseMod_count_rows.to_excel(writer, sheet_name='TotalCount', index=False)
    df_fileBrandPurchaseModAgg.to_excel(writer, sheet_name='DateCount', index=False)

df_filePurchase = pd.read_csv(filePurchase, compression='gzip', header=0, sep='\t')
df_filePurchaseMod = df_filePurchase[['PurchaseDate','PurchaseNumber']].copy()
df_filePurchaseMod['PurchaseDate'] = pd.to_datetime(df_filePurchaseMod['PurchaseDate'], errors='coerce')
df_filePurchaseMod_count_rows = df_filePurchase.groupby('RecordType').size().reset_index(name='counts')
df_filePurchaseModAgg= df_filePurchaseMod.groupby(df_filePurchaseMod['PurchaseDate'].dt.date)['PurchaseNumber'].agg(['count']).reset_index().rename(columns={'PurchaseDate':'PurchaseFile_Date', 'count': 'CountofPurchaseNumbers'})

with pd.ExcelWriter(outputPath+'/Purchase_log.xlsx', mode='w') as writer:
    df_filePurchaseMod_count_rows.to_excel(writer, sheet_name='TotalCount', index=False)
    df_filePurchaseModAgg.to_excel(writer, sheet_name='DateCount', index=False)

df_fileGenericNonSource = pd.read_csv(fileGenericNonSource, compression='gzip', header=0, sep='\t')
df_fileGenericNonSourceMod = df_fileGenericNonSource[['Purchase_Date','PurchaseUID']].copy()
df_fileGenericNonSourceMod['Purchase_Date'] = pd.to_datetime(df_fileGenericNonSourceMod['Purchase_Date'], errors='coerce')
df_fileGenericNonSource_count_rows = df_fileGenericNonSource.groupby('RecordType').size().reset_index(name='counts')
df_fileGenericNonSourceModAgg= df_fileGenericNonSourceMod.groupby(df_fileGenericNonSourceMod['Purchase_Date'].dt.date)['PurchaseUID'].agg(['count']).reset_index().rename(columns={'Purchase_Date':'GenericNonSourceFile_Date', 'count': 'CountofPGenericNonSource'})

with pd.ExcelWriter(outputPath+'/GenericNonSource_log.xlsx', mode='w') as writer:
    df_fileGenericNonSource_count_rows.to_excel(writer, sheet_name='TotalCount', index=False)
    df_fileGenericNonSourceModAgg.to_excel(writer, sheet_name='DateCount', index=False)

df_fileGenericSource = pd.read_csv(fileGenericSource, compression='gzip', header=0, sep='\t')
df_fileGenericSourceMod = df_fileGenericSource[['PurchaseDate','PurchaseUID']].copy()
df_fileGenericSourceMod['PurchaseDate'] = pd.to_datetime(df_fileGenericSourceMod['PurchaseDate'], errors='coerce')
df_fileGenericSource_count_rows = df_fileGenericNonSource.groupby('RecordType').size().reset_index(name='counts')
df_fileGenericSourceModAgg= df_fileGenericSourceMod.groupby(df_fileGenericSourceMod['PurchaseDate'].dt.date)['PurchaseUID'].agg(['count']).reset_index().rename(columns={'PurchaseDate':'GenericSourceFile_Date', 'count': 'CountofGenericSource'})

with pd.ExcelWriter(outputPath+'/GenericNonSource_log.xlsx', mode='w') as writer:
    df_fileGenericSource_count_rows.to_excel(writer, sheet_name='TotalCount', index=False)
    df_fileGenericSourceModAgg.to_excel(writer, sheet_name='DateCount', index=False)


# print(df_fileBrandPurchaseModAgg)
# print(df_fileGenericNonSourceModAgg)
# print(df_fileGenericSourceModAgg)
# print(df_filePurchaseModAgg)





        