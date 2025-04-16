# UK Sanctions Dataset

## Execution Instructions

1. Install python 3 if not already done.
2. Install required packages if not already done:
   
   -pip install pandas
   
   -pip install numpy 

## Things to note

### Justification of columns
- Many columns of interest i.e DOB, Country of birth, Nationality, Passport number, National identification number, Passport details, National identification details, Address, Post/zip code, and country were sparsely populated, but were still deemed essential enough for the null values to be preserved. The bank may use these as references to support their decision on whether to accept a customer.
- Non-latin script and Non-latin language were not included in the final table, as they were too sparsely populated to justify keeping as a valuable column.

### Changes made to values
- DOB had many invalid dates, such as 00/00/19XX, with only the year being valid. These year-only values were changed to have a placeholder date of 01/01/19XX instead, as their year of birth can still be used as a reference to customer details.
- Passport and NI number columns had to be split into 2 separate columns, as many of them held more than one number in the same column
- First names were also combined into a single column to save space
- 'Name 6' was renamed as 'Surname/Entity name' as it was observed that organisations were on this list as well as single individuals
- One record had a non-latin name in its surname/first name columns, so the name was also put in the 'name non-latin script' column for easier searchability.

### Data inconsistencies 
- There were many duplicate names, with individual details such as DOB being altered each time. For this reason these entries were left alone, as it was unclear which one was correct.
- Quite a few rows ended up with more than one value in their 'other _ number' column, but creating an extra column to hold those was not deemed worth it, so they were left alone.
- Country of birth and nationality also tended to have more than one value. It doesn't make sense to separate them into different columns, as only one of can be true. Therefore, they were left alone, meaning the bank can choose how they will interpret those.

- Although useful as a reference point, In light of many columns containing null values, this dataset alone cannot be relied on alone, and must be paired with other more complete sources.

