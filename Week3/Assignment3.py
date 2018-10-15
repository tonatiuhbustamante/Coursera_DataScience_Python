import pandas as pd
import numpy as np
def answer_one():
    energy=pd.read_excel('Energy Indicators.xls')
    energy=energy.drop("Unnamed: 0",1)
    energy=energy.drop("Unnamed: 1",1)
    energy = energy[16:243]
    #remove useless rows and change the name of columns
    #remove header and footer
    energy.rename(columns={"Environmental Indicators: Energy":"Country",
                       "Unnamed: 3": "Energy Supply",
                       "Unnamed: 4": "Energy Supply per Capita",
                       "Unnamed: 5": "% Renewable"},inplace=True)
    #energy = energy.drop(energy.columns[[0, 1]], axis=1)
    #For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.
    energy.replace("...", np.nan,inplace = True)
    #convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule)
    energy["Energy Supply"]*=1000000
    #There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,
    #e.g.
    #'Bolivia (Plurinational State of)' should be 'Bolivia',
    #'Switzerland17' should be 'Switzerland'.
    #is digt returns true if all characters in the string are digits and there is at least one character,
    #false otherwise.
    #find returns the index where "(" appears
    def remove_digit(data):
    #this removes the numberscolumns, still not clear how the isdigit work here
        newData = ''.join([i for i in data if not i.isdigit()])
        i = newData.find('(')
        if i>-1: newData = newData[:i]
        return newData.strip()
    energy['Country'] = energy['Country'].apply(remove_digit)
    energy.replace("Republic of Korea", "South Korea",inplace=True)
    energy.replace("United States of America","United States",inplace=True)
    energy.replace("United Kingdom of Great Britain and Northern Ireland","United Kingdom",inplace=True)
    energy.replace("China, Hong Kong Special Administrative Region","Hong Kong",inplace=True)
    energy = energy.set_index('Country')
#    print(energy)
    #Read the second file
    GDP=pd.read_csv('world_bank.csv',skiprows=4)
#    GDP
    GDP.replace('Korea, Rep.','South Korea',inplace=True)
    GDP.replace("Iran, Islamic Rep","Iran",inplace=True)
    GDP.replace("Hong Kong SAR, China","Hong Kong",inplace=True)
    GDP.rename(columns={"Country Name": "Country"},inplace=True)
    columns_to_keep = ["Country","2006","2007","2008","2009","2010","2011","2012","2013","2014", "2015"]
    GDP = GDP[columns_to_keep]
    GDP = GDP.set_index('Country')
    #GDP
    #Read the third file
    ScimEn=pd.read_excel("scimagojr-3.xlsx")
    ScimEn=ScimEn[0:15]
    ScimEn = ScimEn.set_index('Country')
#    ScimEn
    #inner gives the intersection
    preselection=pd.merge(ScimEn,energy,how="inner",left_index=True,right_index=True)
    selection=pd.merge(preselection,GDP,how="inner",left_index=True,right_index=True)
    return selection
print("answer:", answer_one())
