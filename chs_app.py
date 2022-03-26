from chs_wrapper_class import CompaniesHouseService
import pandas as pd
import datetime

#Initialise variables
key = "d8d5f785-9b19-4873-b1a0-22659560f7b9" 
company_numbers_file = "C:\\Users\\sami-\\Desktop\\python_directory\\CHS\\DummyData.csv"
company_output_file = "C:\\Users\\sami-\\zDesktop\\zpython_directory\\CHS\\CompanyDataOutput.csv"

#Read csv into pandas dataframe
df = pd.read_csv(company_numbers_file, converters={'Company Number': lambda x: str(x)})

#Create an instance of the wrapper class
ch_api = CompaniesHouseService(key)

#Start timer
tic = datetime.datetime.now()

#Loop through rows of dataframe
for index, row in df.iterrows():
    company_number = row["Company Number"]
    ch_profile = ch_api.get_company_profile(company_number)
    df.at[index, "Company Name"] = ch_profile.get("company_name", None)

    #SIC codes are returned as a list of up to 4 numbers
    sics = ch_profile.get("sic_codes", [None])
    for i in range(0,len(sics)):
        df.at[index, f"SIC {i+1}"] = sics[i]

    print(f"Num: {row['Company Number']} | "\
          f"Name: {df.at[index,'Company Name']}")
    
#End timer
toc = datetime.datetime.now()

avg_time = ((toc-tic).total_seconds())/(len(df.index)-1)
print(f"Average time between API calls: {avg_time:0.2f} seconds")

#Save the results to a csv file
df.to_csv(company_output_file, index=False)