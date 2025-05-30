# RGC Data Engineering Test

This task is being used to assess your development ability and process. We expect you to demonstrate your understanding
of Python and Pandas, along with your general data engineering ability.

All data used in this task has been randomly generated and provided for you, please do not change the input data.

# Table of Contents

* [Task](#task)
    * [Data Processing](#data-processing)
    * [Reporting](#reporting)
* [Assessment Criteria](#assessment-criteria)
    * [Core](#core)
    * [Bonus](#bonus)
* [Tips/Hints](#tipshints)

# Task

We have a dataset of company data, we would like you to process this data and create annual reports for one or more
companies.

## Data Processing

Our data is currently fractured in different formats and folders, each folder is a different set of data.

Please process all the data in the [data](./data) folder and save it per company, in a structured way.

### Input

All data can be found in the [data](./data) folder.

The datasets are seperated into four sections:

1. Companies - A list of companies, in csv format, includes unique identifiers, name, address, etc...
2. People - A list of people, in json format
    * Be aware that some company names have been malformed during the generation of this data
    * You will need to find a common field other than company name to match on
3. Market Data - The last price since 2020 for all companies, split into one parquet file per year for all companies,
   indexed on the figi id
    * Be aware, some companies didn't start operating until after 2020
4. Financial Statements - The financial statements per company, in Excel format, each worksheet is a different quarter
    * We do not have financial statements for all companies
    * The sheet names are not in a consistent order

### Output

The final output can be in whatever format you prefer, some options include:

1. A folder per company with the data stored in a structured way
    * It could be an Excel file with the data in different worksheets
    * Parquet or CSV files containing the data
2. A file based database containing the data for all companies - SQLite, Iceberg

We do not need the output stored in the repository, simply submit your code. We will run it locally and check the
output.

## Reporting

Once the data has been processed we would like a one-page annual report for one or more companies. The reporting period
would be Jan - Dec.

Consider this report a tear-sheet for the company for that year, it would be publicly available and should include the
following sections:

1. Reporting period
2. Company Profile
    * Name, address, etc...
3. Notable people
    * Name, title, etc...
4. Stock price for the year in question
    * Graph over the year, starting on the first business day of the year at 100
5. Quarterly financial statements

We only want the report for a year that has ended, please do not include any data for the year in progress.

### Input

The processed output data from the previous section.

### Output

The output can be in whatever format you prefer, some options include:

1. A single HTML file containing an annual report for a company/year
2. A single PDF or Word document for the company with each annual report being on a separate page
3. A single HTML webapp that allows the user to select a company and year to view the report
4. A dashboard in Streamlit or Dash that allows the user to select a company and year to view the report

Please don't feel obliged to go too far with this, if you can simply produce one annual report for a company that is
fine. The assessment criteria below outlines what we are looking for.

# Assessment Criteria

Please use whichever tools you feel are most appropriate for this task. You are not restricted to a specific dependency
manager.

The only requirement is that your code runs on a Windows machine with Python 3.10.

In addition to the obvious skills we are assessing (such as Python, pandas, git, etc...) there are a few additional
gotcha's to look out for. Please consider what has been asked for and the contextual information provided.

## Core

1. The code works with minimal intervention
    * Requirements are clearly defined
    * Any additional instructions are included in the [README](./README.md) file, are clear and accurate
    * We will make some effort to run your code but if we are unable to do so we will consider it a failure
2. The project is well-structured
    * Use of modules and packages as appropriate
    * Use of best practices for Python project structure
3. Demonstrate a good understanding of Python
    * Use packages rather than reinventing the wheel
    * Use of best practices for Python development
4. Demonstrate an understanding of pandas
    * Reading a processing a dataset
    * Merging datasets
    * Grouping and aggregating data
    * Date conversions
5. Data Reporting/Visualisation concepts
    * Consider what data is appropriate to include in the report
    * Good use of page real-estate
6. Development process
    * Good use of version control

## Bonus

These are optional, and a secondary consideration to the core assessment criteria above.

1. Unit tests
2. Documentation
3. Containerisation of your code, either front end or back end
4. Continuous integration

# Tips/Hints

If you are having problems with the task, please get in touch, we would be happy to help you.

* Project Structure - not sure how/where to start
  * Use a tool to create a project structure, don't run it in this repo as it may complain
    * [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/index.html)
    * [copier](https://copier.readthedocs.io/en/latest/)
  * Several guides exist
    * [realpython](https://realpython.com/python-pyproject-toml/)
    * [python-guide](https://python-guide.readthedocs.io/en/latest/writing/structure/)
* Data Processing - useful libs/links
  * [Pandas](https://pandas.pydata.org/)
  * [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
  * [Pyarrow](https://arrow.apache.org/)
* Utilise AI if you want
  * This is meant to represent a real project, use whatever resources you have availible to help you
* Report Generation
  * [jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
  * [streamlit](https://streamlit.io/)
  * [plotly](https://plotly.com/python/)
  * [dash](https://dash.plotly.com/)
* Have fun
  * I hope you find this task enjoyable and learn something new 
