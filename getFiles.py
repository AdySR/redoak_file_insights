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
BranchPurchase_regex = '.*BRAND_PURCHASE_.*.gz$'
Purchase_regex = '.*PURCHASE_.*.gz$'
GenericNonSource_regex = '.*GENERIC_NONSOURCE_.*.gz$'
GenericSource_regex = '.*GENERIC_SOURCE_.*.gz$'
filePath = ini_parser.get('FILE_OSS','path')
listFilesAtPath = [filePath+"\\"+fd for fd in os.listdir(filePath)]
fileBranchPurchase = ''
filePurchase = ''
fileGenericNonSource = ''
fileGenericSource = ''

for file in listFilesAtPath:
    if re.match(BranchPurchase_regex, file):
        fileBranchPurchase = file
    if re.match(Purchase_regex, file):
        filePurchase = file
    if re.match(GenericNonSource_regex, file):
        fileGenericNonSource = file
    if re.match(GenericSource_regex, file):
        fileGenericSource = file

print(fileBranchPurchase)

# df_fileBranchPurchase = pd.read_csv(fileBranchPurchase, compression='gzip', header=0, sep='\t')
# df_fileBranchPurchaseMod = df_fileBranchPurchase[['PurchaseDate','PurchaseNumber']].copy()
# df_fileBranchPurchaseMod['PurchaseDate'] = pd.to_datetime(df_fileBranchPurchaseMod['PurchaseDate'], errors='coerce')
# df_fileBranchPurchaseModAgg= df_fileBranchPurchaseMod.groupby(df_fileBranchPurchaseMod['PurchaseDate'].dt.date)['PurchaseNumber'].agg(['count'])
df_filePurchase = pd.read_csv(filePurchase, compression='gzip', header=0, sep='\t')
df_filePurchaseMod = df_filePurchase[['PurchaseDate','PurchaseNumber']].copy()
df_filePurchaseModAgg= df_filePurchaseMod.groupby(df_filePurchaseMod['PurchaseDate'].dt.date)['PurchaseNumber'].agg(['count']).reset_index().rename(columns={'PurchaseDate':'PurchaseFile_Date', 'count': 'CountofPurchaseNumbers'})
# df_filePurchaseModAgg= df_filePurchaseMod.groupby(df_filePurchaseMod['PurchaseDate'].dt.date)['PurchaseNumber'].agg(['count'])
# df_fileGenericNonSource = pd.read_csv(fileGenericNonSource, compression='gzip', header=0, sep='\t')
# df_fileGenericNonSourceMod = df_fileGenericNonSource[['Purchase_Date','PurchaseUID']].copy()
# df_fileGenericNonSourceMod['Purchase_Date'] = pd.to_datetime(df_fileGenericNonSourceMod['Purchase_Date'], errors='coerce')
# df_fileGenericNonSourceModAgg= df_fileGenericNonSourceMod.groupby(df_fileGenericNonSourceMod['Purchase_Date'].dt.date)['PurchaseUID'].agg(['count'])
# df_fileGenericSource = pd.read_csv(fileGenericSource, compression='gzip', header=0, sep='\t')
# df_fileGenericSourceMod = df_fileGenericSource[['PurchaseDate','PurchaseUID']].copy()
# df_fileGenericSourceMod['PurchaseDate'] = pd.to_datetime(df_fileGenericSourceMod['PurchaseDate'], errors='coerce')
# df_fileGenericSourceModAgg= df_fileGenericSourceMod.groupby(df_fileGenericSourceMod['PurchaseDate'].dt.date)['PurchaseUID'].agg(['count'])

# print(df_fileBranchPurchaseModAgg)
# print(df_fileGenericNonSourceModAgg)
# print(df_fileGenericSourceModAgg)




print(df_filePurchaseModAgg)