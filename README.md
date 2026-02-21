# Data Immersion & Wrangling 

This repository is about the **data access, familiarization, quality assessment, cleaning, and transformation** workflow quickly and in a repeatable way.
Walmart Sales Data Analysis Project
## 1) Project Overview

This task focuses on cleaning and preparing the Walmart Sales dataset for further analysis and dashboard development.
The objective is to transform raw sales data into a structured, reliable, and analysis-ready dataset.

Data preparation is a critical step to ensure accurate insights in subsequent exploratory data analysis (EDA) and business intelligence reporting.
## 2) Objective

Load and inspect the raw dataset
Handle missing values and inconsistencies
Remove duplicate records
Correct data types
Create time-based features for analysis
Export a clean dataset for downstream tasks

## 3) Dataset Description

The dataset contains weekly sales data for multiple Walmart stores, along with economic and environmental indicators such as:

Store ID
Date
Weekly Sales
Holiday Flag
Temperature
Fuel Price
Consumer Price Index (CPI)
Unemployment Rate

## Data Cleaning Steps Performed
1) Data Loading

Imported CSV file using Pandas
Inspected structure using:
.head()
.info()
.shape()

2)Missing Value Handling

Checked for null values using:
df.isnull().sum()
Filled or handled missing values appropriately to ensure dataset completeness.

3)Duplicate Removal

Identified duplicate rows using:
df.duplicated().sum()
Removed duplicates:
df.drop_duplicates(inplace=True)

4)Data Type Corrections

Converted Date column to datetime format:
df['Date'] = pd.to_datetime(df['Date'])

5)Feature Engineering

Created additional time-based columns to support time-series analysis:
Year
Month
Week
Example:
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Week'] = df['Date'].dt.isocalendar().week

6)Data Validation

Ensured no missing values remain
Confirmed no duplicate entries
Verified correct data types

7)The cleaned dataset was exported for use in further tasks:

df.to_csv("cleaned_walmart_sales.csv", index=False)

## Outcome

The dataset is now:
Clean
Structured
Consistent
Ready for analytical modeling and dashboard integration
