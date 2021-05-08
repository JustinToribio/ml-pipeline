# Train Model Task

This script will Train an XGBoost model on the data and save it to disk.

```
Usage: train_model.py [OPTIONS]

Train an XGBoost model on the data and save it to disk.

Parameters
----------
name: str
    name of the model file on local disk, without '.json' suffix.
x_train: str
    file path to the input X_train.pkl file.
y_train: str
    file path to the input y_train.pkl file.
x_test: str
    file path to the input X_test.pkl file.
y_test: str
    file path to the input y_test.pkl file.
out_dir: str
    directory where file should be saved to.

Returns
-------
None

Options:
  --name TEXT
  --x-train TEXT
  --y-train TEXT
  --x-test TEXT
  --y-test TEXT
  --out-dir TEXT
```
