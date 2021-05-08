# Evaluate Model Task

This bash script will make predictions on the validation data with the trained model and generate model evaluation reports.

```
Usage: ./evaluate_model.sh [OPTIONS]

Make predictions on the validation data with the trained model and generate model evaluation reports.

Parameters
----------
OUT_DIR: str
    directory where files should be saved to.
MODEL_PATH: str
    file path to the trained model.
X_VALID_PATH: str
    file path to the input X_test.pkl file.
Y_VALID_PATH: str
    file path to the input y_test.pkl file.

Returns
-------
None

Options: positional (without flags) in the order below
  (OUT_DIR) TEXT
  (MODEL_PATH) TEXT
  (X_VALID_PATH) TEXT
  (Y_VALID_PATH) TEXT
```

The output in the reports (calculations and plots) will automatically change when the pipeline is run with different inputs (i.e. different data, parameters etc...).

This task will produce the model evaluation report in 3 different formats in the `data_root/reports` directory: a pdf, html file and executed Jupyter Notebook.

The pdf and html reports are cleaner as they have code cells hidden that aren't necessary for the reader to view.

Of all the options, the html report opened in a browser is rendered and formatted the best.
