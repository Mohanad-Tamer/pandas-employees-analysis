import pandas as pd


import json



dataframe=pd.read_json("employees.json")

#data cleaning
dataframe = dataframe.drop(columns=["postal_code"])

dataframe = dataframe.drop_duplicates()

dataframe["salary"] = dataframe["salary"].fillna("Trainee")

dataframe=dataframe.dropna(subset=["department"])

dataframe=dataframe.set_index("name")

print(dataframe.to_string())

#analysis
print ("average for each column:")
print(dataframe.mean(numeric_only=True))


print ("max value for each column:")
print (dataframe.max(numeric_only=True))

#search by employee name
emp_name = input("Enter empolyee name:")
try:
    print(dataframe.loc[emp_name])
except KeyError:
    print(f"{emp_name} not found")

#generating report
dataframe["salary"]=pd.to_numeric(dataframe["salary"],errors="coerce")#don't crash on (trainee) values

total_salaries = dataframe["salary"].sum()




with pd.ExcelWriter("salaries_report.xlsx", engine="openpyxl") as writer:

    # summary
    pd.DataFrame({
        "metric": ["total_salaries"],
        "value": [total_salaries]
    }).to_excel(writer, sheet_name="summary", index=False)

    # group by department
    for dept, group in dataframe.groupby("department"):
        group.to_excel(writer, sheet_name=str(dept), index=False)
