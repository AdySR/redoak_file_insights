from pickle import TRUE
from pydoc import describe
from tkinter.messagebox import YES
from nbformat import write
import pandas as pd

df = pd.read_csv(r'C:\Projects\python\pandas\GENERIC_NONSOURCE_20220324000000.txt',sep='\t')

new = df[['Purchase_Date','PurchaseUID']].copy()


new['Purchase_Date'] = pd.to_datetime(new['Purchase_Date'], errors='coerce')


writer= new.groupby(new['Purchase_Date'].dt.date)['PurchaseUID'].agg(['count'])
print(writer)
# writer.to_csv(r'C:\Projects\python\pandas\PURCHASE_20220324000000_writer.csv')

