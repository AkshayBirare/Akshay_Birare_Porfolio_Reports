# Loading required libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the source file (workbook)
# pip install openpyxl (Install and Import Openpyxl to load excel workbook)

df = pd.read_excel(r"C:\Users\Akshay Birare\Downloads\Financial Sample.xlsx", sheet_name= 'Sheet1')
print(df.head())

# Basic Summary Statistics
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())
print(df.memory_usage())

## Statistical overview

print(df.describe())

## Sales column has space added as a prefix, we have to remove those and rename it as Sales

df.rename(columns = {' Sales' : 'Sales'}, inplace=True)
print(df.info())

## Year and Month have int data type, which suppose to be treated as category, so changing the numbers to string
## Change column data types
df['Year'] = df['Year'].astype(str)  # Convert to string
df['Month Number'] = df['Month Number'].astype(str)

## Display the updated data type details and memory usage
print(df.dtypes)
print(df.info())

## Handle missing and null values
df_new = df.isnull()
# Fill Null values
df = df.fillna(0)

# Prepare for numerical variables and categorical variable separation
# Numeric Variables/Columns Handling
numerical_variables = df.select_dtypes(include=['number']).columns
print(f"Numerical Columns :  {numerical_variables}")

# Categorical Variables

categorical_variables = df.select_dtypes(include=['object', 'category', 'string']).columns
print(f"Categorical Columns :  {categorical_variables}")

# Descriptive Statistics

## Finding Co-Relation between numerical fields
corelation_matrix = df.corr(numeric_only=True)
print(corelation_matrix)

## Plot Heatmap for better visualization of co-relation
plt.figure() # Dynamic Plot Size
sns.heatmap(corelation_matrix, annot=True, cmap="coolwarm", fmt=".1f", linewidths=0.5)
plt.title("Heatmap of Financial Terms of Business")
plt.show()




# Alternative if data type wasn't changed as above
# print(numerical_variables) # It contains the Year and Month as well as part of numeric data types
# numerical_variables_excluded = []  # Initialize an empty list to store filtered column names
# # Loop through numeric columns and exclude 'Year' and 'Month Number'
# for col in numerical_variables:
#     if col.lower() != 'year' and col.lower() != 'month number': # Checking for true condition
#         numerical_variables_excluded.append(col) # The final filtered result going to be stored in the empty list, hence append
#
# print("Filtered Columns:", numerical_variables_excluded)
#



# Data Visualization for pattern identification and value distribution
## Plot Histogram (to see how data is spread across different intervals)
for hist_value in numerical_variables:
    plt.figure()
    plt.hist(df[hist_value], bins=5, color='blue', edgecolor='grey')

    # Cosmetic Details
    plt.title(f'Histogram for {hist_value}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    # Result Extraction (All together) including Adjustment of layout and display the plot
    plt.tight_layout()
    plt.show()

## Kernel Density Estimation (used to understand the shape and spread of data)
# for kde_data in numerical_variables:
#     plt.figure()  # Separate figure for KDE plot
#     df[kde_data].plot(kind='kde', color='blue', linewidth=2)
#
#     # Cosmetic Details for KDE
#     plt.title(f'KDE Chart for {kde_data}')  # Set title separately
#     plt.xlabel("Values")
#     plt.ylabel("Density")
#     plt.grid(True)
#
#     # Display the KDE chart
#     plt.tight_layout()
#     plt.show()

## Descriptive Analysis
for value in numerical_variables:
    mean = round(df[value].mean(),0) ## Average value of each numeric field
    median = round(df[value].median(),0) ## Center / Median Value of each numeric field
    mode = round(df[value].mode()[0],0) ## Most Frequent Occurrence
    std_dev = round(df[value].std(),0) ## Standard Deviation = √(∑(x−¯x) ( x − x ¯ ) 2 /n)

    # Printing the result statements
    print(f" The mean of the {value} is :  {mean} ")
    print(f" The median of the {value} is :  {median} ")
    print(f" The mode of the {value} is :  {mode} ")
    print(f" The standard deviation of the {value} is :  {std_dev} ")
    print("_" * 89)

## Box Plot Chart (Box plots offer a clear summary of a dataset's distribution, including the median, quartiles, and range)
## Identifying Outlier, IQR and plotting the Box plot for outliers analysis

for fields in numerical_variables:
    # Step 1 : Chart Plotting Details
    plt.figure() # Plot dynamic figure
    plt.boxplot(df[fields], vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    plt.title(f'Boxplot for {fields}')
    plt.xlabel('Values')
    plt.ylabel(fields)
    plt.show()

    # Step 2 : Identifying IQR of the data points
    q1 = np.quantile(df[fields], 0.25) # Quantile 25%
    #Median is Quantile 50%
    q3 = np.quantile(df[fields], 0.75) # Quantile 75%

    # IQR Formulas and Calculations
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr # Lower Limit Value (Start) for Symmetric Chart
    upper_bound = q3 + 1.5 * iqr # Upper Limit Value (End) for Symmetric Chart

    outliers = df[fields][(df[fields] < lower_bound) | (df[fields] > upper_bound)]

    print(f" Details for {fields}:")
    print(f"- Q1 (25th percentile): {q1:.2f}")  # Rounding it for two digits after decimal
    print(f"- Q3 (75th percentile): {q3:.2f}")  # Rounding it for two digits after decimal
    print(f"- IQR: {iqr:.2f}")
    print(f"- Lower bound: {lower_bound:.2f}, Upper bound: {upper_bound:.2f}")
    print(f"- Number of outliers: {len(outliers)}")

    # After Completion of each loop add the horizontal line at bottom to distinguish the result

    print("_" * 89)

# Summarized result for business overview
# Loop through categorical columns and create a horizontal bar chart
for grouped_data in categorical_variables:
    for grouped_numbers in numerical_variables :
        grouped_sum = df.groupby(df[grouped_data])[grouped_numbers].sum()
        grouped_average = df.groupby(df[grouped_data])[grouped_numbers].sum() / len(grouped_numbers)
        grouped_min = df.groupby(df[grouped_data])[grouped_numbers].min()
        grouped_max = df.groupby(df[grouped_data])[grouped_numbers].max()

        # Printing the result statements
        print(f" The sum of the {grouped_numbers} for {grouped_data} : {grouped_sum}")
        print(f" The average of the {grouped_numbers} for {grouped_data} : {grouped_average}")
        print(f" The minimum value of the {grouped_numbers} for {grouped_data} : {grouped_min}")
        print(f" The maximum value of the {grouped_numbers} for {grouped_data} : {grouped_max}")
        print("_" * 89)


# Bar Chart for Sales and Profit
for column in categorical_variables:
    for grouped_columns in df[['Gross Sales', 'Profit']]:
        sum_grouped = df.groupby(df[column])[grouped_columns].sum()

        # Define bar color logic based on column name
        # Determine bar color based on the column name
        if column == 'Country':
            bar_color = 'green'
        elif column == 'Product':
            bar_color = 'violet'
        else:
            bar_color = 'blue'

        plt.figure(figsize=(10,6))
        plt.barh(sum_grouped.index, sum_grouped.values, color = bar_color , edgecolor = 'black')

        # Add labels and title
        plt.xlabel(f'{column}')
        plt.ylabel(f'{grouped_columns}')
        plt.title(f'{grouped_columns} by {column}')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Display the plot
        plt.show()

# Line Chart (Trend Identification)

date_heirarchy = df[['Date', 'Year', 'Month Name']]
for line_chart in date_heirarchy:
    for line_marks in df[['Gross Sales', 'Profit']]:
        grouped_result = df.groupby(line_chart)[line_marks].sum()

        # Plotting
        plt.plot(grouped_result.index, grouped_result.values, marker='o', linestyle='-', color='g', label='Profit')

        # Formatting the plot
        plt.xlabel(f'{line_chart}')
        plt.ylabel(f'{line_marks}')
        plt.title(f'{line_chart}-wise {line_marks} Line Chart')
        plt.legend()
        plt.grid()
        plt.tight_layout()

        # Display the plot
        plt.show()

# Grouping Data Comparison for Manufacturing and Sales Price
Grouped_Manu = df.groupby('Product')['Manufacturing Price'].sum()
Grouped_Sale = df.groupby('Product')['Sale Price'].sum()

# Plotting
plt.plot(Grouped_Manu.index, Grouped_Manu.values, marker='o', color = 'grey' , label='Manufacturing Price')
plt.plot(Grouped_Sale.index, Grouped_Sale.values, marker='s', color = 'blue' , label='Sale Price')

# Formatting the plot
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Date vs Manufacturing and Sale Prices')

# Positioning the legend in the top-right corner
plt.legend(loc='upper right')
plt.grid()
plt.tight_layout()

# Display the plot
plt.show()