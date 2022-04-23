from distutils.command.config import config
import os
from configparser import ConfigParser
from turtle import fd
import pandas as pd
import re
import gzip
import shutil

# import regex
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

# print(fileBrandPurchase)

df_fileBrandPurchase = pd.read_csv(fileBrandPurchase, compression='gzip', header=0, sep='\t')
df_fileBrandPurchaseMod = df_fileBrandPurchase[['PurchaseDate','PurchaseNumber']].copy()
df_fileBrandPurchaseMod['PurchaseDate'] = pd.to_datetime(df_fileBrandPurchaseMod['PurchaseDate'], errors='coerce')
df_fileBrandPurchaseModAgg= df_fileBrandPurchaseMod.groupby(df_fileBrandPurchaseMod['PurchaseDate'].dt.date)['PurchaseNumber'].agg(['count']).reset_index().rename(columns={'PurchaseDate':'Brand_PurchaseFile_Date', 'count': 'CountofBrand_PurchaseNumbers'})
df_fileBrandPurchaseModAgg.to_csv(outputPath+'/Brand_Purchase_log.txt',sep='\t')

df_filePurchase = pd.read_csv(filePurchase, compression='gzip', header=0, sep='\t')
df_filePurchaseMod = df_filePurchase[['PurchaseDate','PurchaseNumber']].copy()
df_filePurchaseMod['PurchaseDate'] = pd.to_datetime(df_filePurchaseMod['PurchaseDate'], errors='coerce')
df_filePurchaseModAgg= df_filePurchaseMod.groupby(df_filePurchaseMod['PurchaseDate'].dt.date)['PurchaseNumber'].agg(['count']).reset_index().rename(columns={'PurchaseDate':'PurchaseFile_Date', 'count': 'CountofPurchaseNumbers'})
df_filePurchaseModAgg.to_csv(outputPath+'/Purchase_log.txt',sep='\t')

df_fileGenericNonSource = pd.read_csv(fileGenericNonSource, compression='gzip', header=0, sep='\t')
df_fileGenericNonSourceMod = df_fileGenericNonSource[['Purchase_Date','PurchaseUID']].copy()
df_fileGenericNonSourceMod['Purchase_Date'] = pd.to_datetime(df_fileGenericNonSourceMod['Purchase_Date'], errors='coerce')
df_fileGenericNonSourceModAgg= df_fileGenericNonSourceMod.groupby(df_fileGenericNonSourceMod['Purchase_Date'].dt.date)['PurchaseUID'].agg(['count']).reset_index().rename(columns={'Purchase_Date':'GenericNonSourceFile_Date', 'count': 'CountofPGenericNonSource'})
df_fileGenericNonSourceModAgg.to_csv(outputPath+'/GenericNonSource_log.txt',sep='\t')

df_fileGenericSource = pd.read_csv(fileGenericSource, compression='gzip', header=0, sep='\t')
df_fileGenericSourceMod = df_fileGenericSource[['PurchaseDate','PurchaseUID']].copy()
df_fileGenericSourceMod['PurchaseDate'] = pd.to_datetime(df_fileGenericSourceMod['PurchaseDate'], errors='coerce')
df_fileGenericSourceModAgg= df_fileGenericSourceMod.groupby(df_fileGenericSourceMod['PurchaseDate'].dt.date)['PurchaseUID'].agg(['count']).reset_index().rename(columns={'PurchaseDate':'GenericSourceFile_Date', 'count': 'CountofGenericSource'})
df_fileGenericSourceModAgg.to_csv(outputPath+'/GenericSource_log.txt',sep='\t')



# print(df_fileBrandPurchaseModAgg)
# print(df_fileGenericNonSourceModAgg)
# print(df_fileGenericSourceModAgg)
# print(df_filePurchaseModAgg)