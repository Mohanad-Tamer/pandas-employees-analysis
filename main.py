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

sum_salaries=dataframe.groupby("department")["salary"].sum().reset_index()

max_salary=dataframe.groupby("department")["salary"].max().reset_index()


report = {
    "total_salaries": total_salaries,
    "sum_salaries_by_department": sum_salaries.to_dict(orient="records"),
    "max_salary_by_department": max_salary.to_dict(orient="records")
}

pd.Series(report).to_json("salaries_report.json",indent=4)

