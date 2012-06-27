import veritable
from veritable.utils import read_csv, split_rows, clean_data
from os.path import dirname, join

DATA_FILE = join(dirname(__file__),'bank-data.csv')
TRAIN_FRAC = .80
PRED_COUNT = 100
TARGET_COL = 'pep'
TABLE_ID = 'bank-data-example'
ANALYSIS_ID = 'main-analysis'
MAXIMUM_UNCERTAINTY_THRESHOLDS = [0.5, 0.4, 0.3]




def main():

    ##########
    # UPLOAD #
    ##########

    # 1. Define the schema for the table - specify column names and data types
    table_schema = {
        'age': {'type': 'count'},
        'sex': {'type': 'categorical'},
        'region': {'type': 'categorical'},
        'income': {'type': 'real'},
        'married': {'type': 'boolean'},
        'children': {'type': 'count'},
        'car': {'type': 'boolean'},
        'save_act': {'type': 'boolean'},
        'current_act': {'type': 'boolean'},
        'mortgage': {'type': 'boolean'},
        'pep': {'type': 'boolean'},
    }

    # 2. Load the data from csv and divide it into training and test subsets
    rows = read_csv(DATA_FILE)                                  # Load rows from CSV, returns all row data values as strings
    clean_data(rows, table_schema)                               # Convert row data values to correct types based on schema
    training_rows, test_rows = split_rows(rows, TRAIN_FRAC)     # Split into training and test sets

    # 3. Connect to the Veritable API
    api = veritable.connect()
    if api.table_exists(TABLE_ID):
        print("Deleting old table '%s'" %TABLE_ID)
        api.delete_table(TABLE_ID)

    # 4. Create a Veritable Table and upload training rows
    print("Creating table '%s' and uploading rows" %TABLE_ID)
    table = api.create_table(table_id=TABLE_ID)
    table.batch_upload_rows(training_rows)



    ###########
    # ANALYZE #
    ###########

    # 5. Create a Veritable Analysis and wait for it to complete
    print("Creating analysis '%s' and waiting for it to complete" %ANALYSIS_ID)
    analysis = table.create_analysis(schema=table_schema, analysis_id=ANALYSIS_ID)
    analysis.wait()



    ###########
    # PREDICT #
    ###########


    # 6. For each row in the test set, predict the value and uncertainty for the target column
    print("Making predictions")

    prediction_results = []
    for test_row in test_rows:
        # Prepare the prediction request
        prediction_request = test_row.copy()        # Copy known values from test row
        del prediction_request['_id']               # '_id' should not be present in prediction requests
        prediction_request[TARGET_COL] = None       # None values are predicted by Veritable

        # Make predictions
        prediction = analysis.predict(prediction_request, PRED_COUNT)

        # Derive a single value estimate and uncertainty metric
        estimate = prediction[TARGET_COL]
        uncertainty = prediction.uncertainty[TARGET_COL]

        # Compare estimate to actual value from test row
        is_correct = (estimate == test_row[TARGET_COL])

        # Collect results
        prediction_results.append( { 'is_correct':is_correct, 'uncertainty':uncertainty } )


    # 7. Evaluate prediction accuracy using different maximum uncertainty thresholds
    for maximum_uncertainty in MAXIMUM_UNCERTAINTY_THRESHOLDS:
        # Treat prediction results as unknown if uncertainty is above the maximum_uncertainty threshold
        unknown_prediction_results = [r for r in prediction_results if r['uncertainty'] > maximum_uncertainty]
        unknown_count = len(unknown_prediction_results)

        # Only look at prediction results if uncertainty is below the maximum_uncertainty threshold
        known_prediction_results = [r for r in prediction_results if r['uncertainty'] <= maximum_uncertainty]
        known_count = len(known_prediction_results)

        # Identify prediction results we looked at that are correct
        known_correct_prediction_results = [r for r in known_prediction_results if r['is_correct']]
        known_correct_count = len(known_correct_prediction_results)

        print( "Predictions for {0} are {1:.0%} ({2}/{3}) correct with {4:.0%} ({5}/{6}) ignored using a maximum uncertainty of {7}".format(
                    TARGET_COL,
                    0.0 if known_count == 0 else float(known_correct_count) / known_count,
                    known_correct_count,
                    known_count,
                    float(unknown_count) / (known_count+unknown_count),
                    unknown_count,
                    known_count+unknown_count,
                    maximum_uncertainty ) )



if __name__ == '__main__':
    main()
