#!/usr/bin/env python
# coding: utf-8

# ## Capstone_PythonHero19
# 
# null

# **Capstone Project: 2025 UK Industry Demand (Ongoing Project)**

# 

# **Import the Necessary Libraries (For CSV File)**

# In[2]:


# Import pandas so we can load and work with CSV data:
import pandas as pd

# Import the specific tool we need to save data to the Lakehouse:
from deltalake import write_deltalake

# Show a message so we know the libraries imported successfully:
print("Libraries imported successfully.")


# **Define the CSV File Location**

# In[78]:


# Store the web address for the industry demand in 2025:
industry_2025_url = "https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/17bfed6e-4133-4796-9006-df89163446f2/csv"


# Print a message so we know the file links have been stored:
print("CSV file links saved.")


# **Save to Lakehouse **

# **Load the CSV File Into Python**

# In[79]:


# Load the 2025 industry demand CSV file into a DataFrame:
df_2025_industry = pd.read_csv(industry_2025_url)

# Print the first five rows loaded from the 2025 industry demand:
display(df_2025_industry.head())


# **Save the Data to a Lakehouse Table**

# **Define The Table Details**

# In[80]:


# Define the Lakehouse location:
location ="abfss://PythonHero@onelake.dfs.fabric.microsoft.com/PythonHero_Lakehouse.Lakehouse/Tables"

# Define the prefix for your table name as your username (for e.g. PythonHero01):
hero_name = "pythonhero19"

# Define the name for your table:
table_name = "2025_INDUSTRY_DEMAND"

# Define the table details by bringing it all together:
table_path = f"{location}/{hero_name}/{table_name}"


# **Fabric Connection Settings**

# In[81]:


# Define how to securely connect to your Lakehouse (Fabric connection settings):
storage_options = {
    "bearer_token": notebookutils.credentials.getToken("storage"),
    "use_fabric_endpoint": "true",
    "allow_unsafe_rename": "true"
}


# **Save the Dataframe to a Lakehouse Table**

# In[82]:


# Save the combined DataFrame as a Lakehouse table:
write_deltalake(
    table_path,
    data = df_2025_industry,
    mode = "overwrite",
    storage_options = storage_options
)


# ****Exploratory Data Analysis****

# In[83]:


# Import the libraries we need:
from deltalake import DeltaTable


# In[84]:


# Open the 2025 industry demand reference table and convert it into a pandas DataFrame:
df_2025_ID = DeltaTable(
    table_path,
    storage_options = storage_options
).to_pandas()


# **Check the unique values of the categorical column variables**

# In[85]:


display(df_2025_ID["soc20_unit"].unique()) #SOC20 - Filter by occupation unit


# In[86]:


display(df_2025_ID["soc20_label"].unique()) #	SOC20 Description - Filter by occupation description


# In[87]:


display(df_2025_ID["SIC_name"].unique()) #	Industry name - Filter by industry name


# In[88]:


display(df_2025_ID["occupation_workers"].unique()) #Number of occupation workers


# In[89]:


display(df_2025_ID["industry_workers"].unique()) #Number of industry workers


# In[90]:


display(df_2025_ID["demand_level"].unique()) #Demand level - Filter by level of demand


# In[91]:


display(df_2025_ID["skill_level"].unique()) #ONS skill level - Filter by ONS skill level


# In[92]:


display(df_2025_ID["immigration_salary_list"].unique()) #Occupation is in the immigration salary list


# In[93]:


display(df_2025_ID["construction"].unique()) #Occupation is in construction


# In[94]:


display(df_2025_ID["STEM"].unique()) #	Occupation is in STEM


# In[95]:


display(df_2025_ID["indicator_uncertainty"].unique()) #Uncertainty in demand indicators


# In[96]:


display(df_2025_ID["indicator_demand"].unique()) #Indicators that are in demand


# In[97]:


display(df_2025_ID["indicator_demand_uncertainty_flag"].unique()) #Uncertainty in indicators which are in high demand - Filter by whether an occupation has demand indicators which also hit uncertainty flags


# In[98]:


display(df_2025_ID["imputation_capped_indicators"].unique()) #Indicators capped at elevated demand due to imputation


# In[99]:


display(df_2025_ID["named_imputed_indicators"].unique()) #Indicators imputed from 3-digit SOC


# In[100]:


display(df_2025_ID["count"].unique()) #Number of occupations


# In[101]:


display(df_2025_ID["percent"].unique()) #Proportion of workers


# In[102]:


display(df_2025_ID["demand_level_percent"].unique()) #Proportion of workers in demand


# In[103]:


display(df_2025_ID["time_period"].unique()) #year


# In[104]:


display(df_2025_ID["time_identifier"].unique()) #time identifier


# In[105]:


display(df_2025_ID["geographic_level"].unique()) #geographic level


# In[106]:


display(df_2025_ID["country_code"].unique()) #country code


# In[107]:


display(df_2025_ID["country_name"].unique()) #country name


# **Data Cleaning**

# In[108]:


#Preview the table
print("Number of rows:", len(df_2025_ID))


# In[109]:


#Remove the total rows for all the columns
df_2025_ID_filtered = df_2025_ID[
    ~(df_2025_ID == "Total").any(axis=1)
]


# In[110]:


#Show the number of rows after filtering
print("2025 industry rows after cleaning:", len(df_2025_ID_filtered))


# In[111]:


# Print the first five rows loaded from the filtered table of the 2025 UK industry demand
display(df_2025_ID_filtered.head())


# **Data Analysis and Visualization**

# **Import the required visualization library**

# 

# In[112]:


#Import the required visualization library
import matplotlib.pyplot as plt


# **Number of UK workers by industry in 2025**

# In[113]:


#Group the workers by industry and add up the number of workers in each group
workers_by_industry = (
    df_2025_ID_filtered.groupby("SIC_name", as_index=False)["industry_workers"].sum()
    .sort_values("industry_workers", ascending=False)
)

#Use comma after every three digits from the right for readability and display the result
workers_by_industry["industry_workers"] = workers_by_industry["industry_workers"].apply(lambda x: f"{x:,}")
display(workers_by_industry)


# **Proportion of UK workers by demand level in 2025**

# In[114]:


#Group by demand level
workers_by_demand = df_2025_ID_filtered.groupby("demand_level", as_index=False)["industry_workers"].sum()

#Show count and percentage
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f"{count:,}\n({pct:.1f}%)"
    return my_autopct

#Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(workers_by_demand["industry_workers"], labels=workers_by_demand["demand_level"], 
        autopct=make_autopct(workers_by_demand["industry_workers"])
)
plt.title("Workers by Demand Level")
plt.axis("equal")
plt.show()


# **Notes:** A total of five demand indicators are used to categorise occupations into one of three demand levels: critical demand (substantially higher demand than usual), elevated demand (above average), and not in high demand. Occupations are defined using the Standard Occupational Classification (SOC) and are categorised using the following steps, which are covered in more detail in the accompanying methodology:
# - A demand level is calculated for each individual indicator based on thresholds specific to that indicator.
# - For change in wage, change in hours, wage premium and job advert density the thresholds are set based on a period of historical data.
# - For visa grant density, the thresholds are a relative measure for that year’s density of visas across occupations, as policy changes make historical comparisons more challenging.
# - The overall demand level is based on the number of indicators that are in critical or elevated demand. 
# 
# 

# **Demand indicators used to create the demand classification**
# - Visa grant density - The number of visas granted as a proportion of employment in that occupation.
# - Online job advert density - The number of online job adverts as a proportion of employment in that occupation.
# - Annual percentage change in hourly wage - The year-on-year percentage change in average hourly wage in an occupation.
# - Wage premium - The average wage of an occupation compared to other occupations in the same ONS skill level when controlling for factors such as age and sex. 
# - Annual change in hours worked - The year-on-year absolute change in average weekly hours worked in an occupation.
# 
# Source: https://explore-education-statistics.service.gov.uk/find-statistics/occupations-in-demand/2025#section-demand-levels-across-indicators

# **Number of UK workers under critical demand per industry in 2025**

# In[116]:


#Filter for Critical Demand only
critical_workers = df_2025_ID_filtered[df_2025_ID_filtered["demand_level"] == "Critical demand"]

#Group the workers by industry and add up the number of workers in each group
workers_by_industry = (
    critical_workers.groupby("SIC_name", as_index=False)["industry_workers"].sum()
    .sort_values("industry_workers", ascending=True)
)

#Create bar chart
plt.figure(figsize=(10, 6))
bars = plt.barh(workers_by_industry["SIC_name"], workers_by_industry["industry_workers"])

#Add the exact number of workers label on top of each bar
for bar in bars:
    width = bar.get_width()
    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width):,}",
        ha="left",
        va="center"
    )

plt.xlabel("Number of Workers")
plt.title("Critical Demand Workers by Industry")
plt.tight_layout()
plt.show()


# ****Critical Demand Occupations: Health and Social Care****

# In[124]:


#Filter the number of workers by health and social care industry and critical demand
critical_health_filtered = df_2025_ID_filtered[
    (df_2025_ID_filtered["SIC_name"] == "Health and social care") &
    (df_2025_ID_filtered["demand_level"] == "Critical demand")
]

#Group by occupation and add up the number of workers in each group
cw_health = (
    critical_health_filtered.groupby(["soc20_label", "immigration_salary_list", "construction", "STEM", "skill_level"], as_index=False)["industry_workers"].sum()
    .sort_values("industry_workers", ascending=True)
)

#Remove rows where industry_workers is 0
cw_health = cw_health[cw_health["industry_workers"] != 0]

#Function to build badge labels based on the flags
def get_icons(row):
    badges = []
    if row["immigration_salary_list"] == "Yes":
        badges.append("I")
    if row["construction"] == "Yes":
        badges.append("C")
    if row["STEM"] == "Yes":
        badges.append("S")
    if pd.notna(row["skill_level"]):
        badges.append("SL" + str(row["skill_level"]).split()[-1])
    return " ".join(badges)

cw_health["icons"] = cw_health.apply(get_icons, axis=1)

#Create bar chart
plt.figure(figsize=(12, 8))
bars = plt.barh(cw_health["soc20_label"], cw_health["industry_workers"])


#Add the exact number of workers + badges beside each bar
for bar, icons in zip(bars, cw_health["icons"]):
    width = bar.get_width()
    label = f"{int(width):,}"
    if icons:
        label += f"  [{icons}]"
    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        label,
        ha="left",
        va="center",
        fontsize=9
    )

plt.xlabel("Number of Workers")
plt.title("Number of Workers in Health and Social Care under Critical Demand")

#Add legend below the text
legend_text = (
    "I = Immigration Salary List   |   C = Construction   |   S = STEM\n"
    "SL1 = Skill Level 1   |   SL2 = Skill Level 2   |   SL3 = Skill Level 3   |   SL4 = Skill Level 4"
)
plt.figtext(0.5, -0.02, legend_text, ha="center", fontsize=8, wrap=True)

plt.tight_layout()
plt.show()


# **Critical Demand Occupations: Professional Scientific and Technical**

# In[126]:


#Filter the number of workers by professional scientific and technical industry and critical demand
critical_scientific_filtered = df_2025_ID_filtered[
    (df_2025_ID_filtered["SIC_name"] == "Professional scientific and technical") &
    (df_2025_ID_filtered["demand_level"] == "Critical demand")
]

#Group by occupation and add up the number of workers in each group
cw_scientific = (
    critical_scientific_filtered.groupby(["soc20_label", "immigration_salary_list", "construction", "STEM", "skill_level"], as_index=False)["industry_workers"].sum()
    .sort_values("industry_workers", ascending=True)
)

#Remove rows where industry_workers is 0
cw_scientific = cw_scientific[cw_scientific["industry_workers"] != 0]

#Function to build badge labels based on the flags
def get_icons(row):
    badges = []
    if row["immigration_salary_list"] == "Yes":
        badges.append("I")
    if row["construction"] == "Yes":
        badges.append("C")
    if row["STEM"] == "Yes":
        badges.append("S")
    if pd.notna(row["skill_level"]):
        badges.append("SL" + str(row["skill_level"]).split()[-1])
    return " ".join(badges)

cw_scientific["icons"] = cw_scientific.apply(get_icons, axis=1)

#Create bar chart
plt.figure(figsize=(10, 8))
bars = plt.barh(cw_scientific["soc20_label"], cw_scientific["industry_workers"])


#Add the exact number of workers + badges beside each bar
for bar, icons in zip(bars, cw_scientific["icons"]):
    width = bar.get_width()
    label = f"{int(width):,}"
    if icons:
        label += f"  [{icons}]"
    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        label,
        ha="left",
        va="center",
        fontsize=9
    )

plt.xlabel("Number of Workers")
plt.title("Number of Workers in Professional Scientific and Technical under Critical Demand")

#Add legend below the text
legend_text = (
    "I = Immigration Salary List   |   C = Construction   |   S = STEM\n"
    "SL1 = Skill Level 1   |   SL2 = Skill Level 2   |   SL3 = Skill Level 3   |   SL4 = Skill Level 4"
)
plt.figtext(0.5, -0.02, legend_text, ha="center", fontsize=8, wrap=True)

plt.tight_layout()
plt.show()


# **Critical Demand Occupations: Manufacturing and Production**

# In[128]:


#Filter the number of workers by manufacturing industry and critical demand
critical_manufacturing_filtered = df_2025_ID_filtered[
    (df_2025_ID_filtered["SIC_name"] == "Manufacturing and production") &
    (df_2025_ID_filtered["demand_level"] == "Critical demand")
]

#Group by occupation and add up the number of workers in each group
cw_manufacturing = (
    critical_manufacturing_filtered.groupby(["soc20_label", "immigration_salary_list", "construction", "STEM", "skill_level"], as_index=False)["industry_workers"].sum()
    .sort_values("industry_workers", ascending=True)
)

#Remove rows where industry_workers is 0
cw_manufacturing = cw_manufacturing[cw_manufacturing["industry_workers"] != 0]

#Function to build badge labels based on the flags
def get_icons(row):
    badges = []
    if row["immigration_salary_list"] == "Yes":
        badges.append("I")
    if row["construction"] == "Yes":
        badges.append("C")
    if row["STEM"] == "Yes":
        badges.append("S")
    if pd.notna(row["skill_level"]):
        badges.append("SL" + str(row["skill_level"]).split()[-1])
    return " ".join(badges)

cw_manufacturing["icons"] = cw_manufacturing.apply(get_icons, axis=1)

#Create bar chart
plt.figure(figsize=(10, 8))
bars = plt.barh(cw_manufacturing["soc20_label"], cw_manufacturing["industry_workers"])


#Add the exact number of workers + badges beside each bar
for bar, icons in zip(bars, cw_manufacturing["icons"]):
    width = bar.get_width()
    label = f"{int(width):,}"
    if icons:
        label += f"  [{icons}]"
    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        label,
        ha="left",
        va="center",
        fontsize=9
    )

plt.xlabel("Number of Workers")
plt.title("Number of Workers in Manufacturing and Production under Critical Demand")

#Add legend below the text
legend_text = (
    "I = Immigration Salary List   |   C = Construction   |   S = STEM\n"
    "SL1 = Skill Level 1   |   SL2 = Skill Level 2   |   SL3 = Skill Level 3   |   SL4 = Skill Level 4"
)
plt.figtext(0.5, -0.02, legend_text, ha="center", fontsize=8, wrap=True)

plt.tight_layout()
plt.show()


# **Critical Demand Occupations: Public Administration and Defence**

# In[132]:


#Filter the number of workers by public administration and defence industry and critical demand
critical_publicad_filtered = df_2025_ID_filtered[
    (df_2025_ID_filtered["SIC_name"] == "Public administration and defence") &
    (df_2025_ID_filtered["demand_level"] == "Critical demand")
]

#Group by occupation and add up the number of workers in each group
cw_publicad = (
    critical_publicad_filtered.groupby(["soc20_label", "immigration_salary_list", "construction", "STEM", "skill_level"], as_index=False)["industry_workers"].sum()
    .sort_values("industry_workers", ascending=True)
)

#Remove rows where industry_workers is 0
cw_publicad = cw_publicad[cw_publicad["industry_workers"] != 0]

#Function to build badge labels based on the flags
def get_icons(row):
    badges = []
    if row["immigration_salary_list"] == "Yes":
        badges.append("I")
    if row["construction"] == "Yes":
        badges.append("C")
    if row["STEM"] == "Yes":
        badges.append("S")
    if pd.notna(row["skill_level"]):
        badges.append("SL" + str(row["skill_level"]).split()[-1])
    return " ".join(badges)

cw_publicad["icons"] = cw_publicad.apply(get_icons, axis=1)

#Create bar chart
plt.figure(figsize=(12, 10))
bars = plt.barh(cw_publicad["soc20_label"], cw_publicad["industry_workers"])


#Add the exact number of workers + badges beside each bar
for bar, icons in zip(bars, cw_publicad["icons"]):
    width = bar.get_width()
    label = f"{int(width):,}"
    if icons:
        label += f"  [{icons}]"
    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        label,
        ha="left",
        va="center",
        fontsize=9
    )

plt.xlabel("Number of Workers")
plt.title("Number of Workers in Public Administration and Defence under Critical Demand")

#Add legend below the text
legend_text = (
    "I = Immigration Salary List   |   C = Construction   |   S = STEM\n"
    "SL1 = Skill Level 1   |   SL2 = Skill Level 2   |   SL3 = Skill Level 3   |   SL4 = Skill Level 4"
)
plt.figtext(0.5, -0.02, legend_text, ha="center", fontsize=8, wrap=True)

plt.tight_layout()
plt.show()


# **Critical Demand Occupations: Information and Communication**

# In[133]:


#Filter the number of workers by information and communication industry and critical demand
critical_info_filtered = df_2025_ID_filtered[
    (df_2025_ID_filtered["SIC_name"] == "Information and communication") &
    (df_2025_ID_filtered["demand_level"] == "Critical demand")
]

#Group by occupation and add up the number of workers in each group
cw_info = (
    critical_info_filtered.groupby(["soc20_label", "immigration_salary_list", "construction", "STEM", "skill_level"], as_index=False)["industry_workers"].sum()
    .sort_values("industry_workers", ascending=True)
)

#Remove rows where industry_workers is 0
cw_info = cw_info[cw_info["industry_workers"] != 0]

#Function to build badge labels based on the flags
def get_icons(row):
    badges = []
    if row["immigration_salary_list"] == "Yes":
        badges.append("I")
    if row["construction"] == "Yes":
        badges.append("C")
    if row["STEM"] == "Yes":
        badges.append("S")
    if pd.notna(row["skill_level"]):
        badges.append("SL" + str(row["skill_level"]).split()[-1])
    return " ".join(badges)

cw_info["icons"] = cw_info.apply(get_icons, axis=1)

#Create bar chart
plt.figure(figsize=(10, 6))
bars = plt.barh(cw_info["soc20_label"], cw_info["industry_workers"])


#Add the exact number of workers + badges beside each bar
for bar, icons in zip(bars, cw_info["icons"]):
    width = bar.get_width()
    label = f"{int(width):,}"
    if icons:
        label += f"  [{icons}]"
    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        label,
        ha="left",
        va="center",
        fontsize=9
    )

plt.xlabel("Number of Workers")
plt.title("Number of Workers in Information and Communication under Critical Demand")

#Add legend below the text
legend_text = (
    "I = Immigration Salary List   |   C = Construction   |   S = STEM\n"
    "SL1 = Skill Level 1   |   SL2 = Skill Level 2   |   SL3 = Skill Level 3   |   SL4 = Skill Level 4"
)
plt.figtext(0.5, -0.02, legend_text, ha="center", fontsize=8, wrap=True)

plt.tight_layout()
plt.show()

