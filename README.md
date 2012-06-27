# Introduction

The `bank-data.csv` file contains 600 rows corresponding to bank customers, and 11 columns that describe each customer's family, basic demographics, and current banking products.  The target column, `pep`, indicates whether the customer purchased a Personal Equity Plan after the most recent promotional campaign.

The overall goal of this analysis is to predict which customers are likely to purchase a PEP. 

This is a more in-depth example than the Quickstart and more closely maps to a traditional data science workflow.

We proceed as follows:

1. Define a schema for the table
2. Load the data from csv and divide it into training and test subsets
3. Connect to the Veritable API
4. Create a Veritable Table and upload training rows
5. Create a Veritable Analysis and wait for it to complete
6. For each row in the test set, predict the value and uncertainty for the target column
7. Evaluate prediction accuracy using different maximum uncertainty thresholds

To run this demo, clone it locally and then:

    pip install -r requirements.txt
    pip install -e .
    python -m bank_data.run
    


# Files

- `run.py`: A python script that divides the data in training and test sets, creates the table and analysis, and runs predictions on the test data
- `bank-data.csv`: A csv file containg the bank dataset

# Dataset Description

- 600 rows, each a bank customer
- 11 columns
- some missing values
- all column types: boolean, categorical, real, and count
- target column is `pep`: whether the bank customer purchased a Personal Equity Product

# Usage

    $ export VERITABLE_KEY=yourapikey
    $ python run.py

# Output

The `run.py` script will print its progress and the results to the console:

    Creating table 'bank-data-example' and uploading rows
    Creating analysis 'main-analysis' and waiting for it to complete
    Making predictions
    Predictions for pep are 55% (33/60) correct with 0% (0/60) ignored using a maximum uncertainty of 0.5
    Predictions for pep are 65% (17/26) correct with 57% (34/60) ignored using a maximum uncertainty of 0.4
    Predictions for pep are 85% (6/7) correct with 88% (53/60) ignored using a maximum uncertainty of 0.3


