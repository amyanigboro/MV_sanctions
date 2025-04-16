import numpy as np
import pandas as pd
import re

#loading the csv into a dataframe, starting the header on the second row
df = pd.read_csv('ConList.csv', header=1)

#Replacing nan values with an empty string
df[['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5']] = df[['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5']].fillna('')

#Merging the first names into a single column, joining each name with a space
df['First Name(s)'] = df[['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5']].apply(' '.join, axis=1)

#Removing trailing spaces
df['First Name(s)'] = df['First Name(s)'].str.strip()
df['First Name(s)'] = df['First Name(s)'].replace({'': np.nan})

df = df.rename(columns={'Name 6': 'Surname/Entity name'})

#Replacing the null address values with an empty string
df[['Address 1', 'Address 2', 'Address 3', 'Address 4', 'Address 5', 'Address 6']] = df[['Address 1', 'Address 2', 'Address 3', 'Address 4', 'Address 5', 'Address 6']].fillna('').astype(str)

#Joining all the address columns together, using a comma and space as a separator, ignoring the empty columns
df['Address 1'] = df[['Address 1', 'Address 2', 'Address 3', 'Address 4', 'Address 5', 'Address 6']].apply(lambda col: ', '.join(filter(None, col)), axis=1)

#Changing the empty strings back to nan values, to make them easier to handle for future use
df['Address 1'] = df['Address 1'].replace({'': np.nan}) 

#Renaming the address column that will be used in the final dataframe
df = df.rename(columns={'Address 1': 'Address'}) 


#Creating the final dataframe with our desired columns that we want to keep
sanctComp= df[['Surname/Entity name',
         'First Name(s)',
         'Name Non-Latin Script',
         'DOB',
         'Country of Birth',
         'Nationality',
         'Passport Number',
         'Passport Details',
         'National Identification Number',
         'National Identification Details',
         'Address',
         'Post/Zip Code',
         'Country',
         'Regime',       
         'Other Information',
         'Last Updated']].copy()

#Many values in the DOB have 00/00/YYYY date formats, which is invalid
#The years are still useful, so instead of nullifying these values, we will use 01/01 as a substitute
#For the days and months
def fix_date(date_str):
    parts = date_str.split('/')
    if len(parts) == 3:
        day, month, year = parts
        month = '01' if month == '0' or month == '00' else month
        day = '01' if day == '0' or day == '00' else day
        return f"{day}/{month}/{year}"
    return date_str

#Applying this function to fix the 'zero' dates before converting to datetime
sanctComp['DOB'] = sanctComp['DOB'].astype(str).apply(fix_date)

# splitting passport/NI numbers based on observed syntax e.g (1) a2304024 (2) 3942943
def splitdetails(details):
    details = str(details)
    if details.startswith('(1) '):
        parts = re.split(r'\(1\) |\s\(2\)', details)
        # numbers = [part.split(' ')[1] for part in parts]
        return parts[1], parts[2] #if len(parts) > 1 else np.nan
    else:
        return details, np.nan

#applying the function 
sanctComp[['Passport Number 1', 'O']] = sanctComp['Passport Number'].apply(splitdetails).apply(pd.Series)
sanctComp[['National Identification Number 1', 'National Identification Number 2']] = sanctComp['National Identification Number'].apply(splitdetails).apply(pd.Series)

#dropping the old columns
sanctComp = sanctComp.drop(['Passport Number', 'National Identification Number'], axis=1)


#Converting each column to their most appropriate type
sanctComp['Surname/Entity name'] = sanctComp['Surname/Entity name'].astype(str)
sanctComp['First Name(s)'] = sanctComp['First Name(s)'].astype(str)
sanctComp['Name Non-Latin Script'] = sanctComp['Name Non-Latin Script'].astype(str)
sanctComp['DOB'] = sanctComp['DOB'].astype('datetime64[ns]')
sanctComp['Country of Birth'] = sanctComp['Country of Birth'].astype(str)
sanctComp['Nationality'] = sanctComp['Nationality'].astype(str)
sanctComp['Passport Number 1'] = sanctComp['Passport Number 1'].astype(str)
sanctComp['Passport Number 2'] = sanctComp['Passport Number 2'].astype(str)
sanctComp['Passport Details'] = sanctComp['Passport Details'].astype(str)
sanctComp['National Identification Number 1'] = sanctComp['National Identification Number 1'].astype(str)
sanctComp['National Identification Number 2'] = sanctComp['National Identification Number 2'].astype(str)
sanctComp['National Identification Details'] = sanctComp['National Identification Details'].astype(str)
sanctComp['Address'] = sanctComp['Address'].astype(str)
sanctComp['Post/Zip Code'] = sanctComp['Post/Zip Code'].astype(str)
sanctComp['Country'] = sanctComp['Country'].astype(str)
sanctComp['Regime'] = sanctComp['Regime'].astype(str)
sanctComp['Other Information'] = sanctComp['Other Information'].astype(str)
sanctComp['Last Updated'] = sanctComp['Last Updated'].astype('datetime64[ns]')

#Adding non-latin name of particular record to the appropriate column as well
sanctComp.at[18797, 'Name Non-Latin Script'] = sanctComp.at[18797, 'Surname/Entity name']

#Exporting transformed df to csv file, not keeping the index generated by pandas
sanctComp.to_csv('sanctions_transformed.csv', index=False)

