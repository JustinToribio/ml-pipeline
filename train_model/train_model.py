from pathlib import Path

import click
import pandas as pd
from xgboost import XGBRegressor


@click.command()
@click.option('--name')
@click.option('--x-train')
@click.option('--y-train')
@click.option('--x-test')
@click.option('--y-test')
@click.option('--out-dir')
def train_model(name, x_train, y_train, x_test, y_test, out_dir):
    """Train an XGBoost model on the data and save it to disk.

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
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f'{name}.json'

    # Read the data
    x_train = pd.read_pickle(x_train)
    y_train = pd.read_pickle(y_train)
    x_valid = pd.read_pickle(x_test)
    y_valid = pd.read_pickle(y_test)

    # Define the model with selected hyperparameters
    model_1 = XGBRegressor(n_estimators=1000, learning_rate=0.05)
    
    # Train the model, stopping when there's no more improvement in
    # the validation loss 
    model_1.fit(x_train, y_train, early_stopping_rounds=5,
                eval_set=[(x_valid, y_valid)], verbose=False)

    # Save the model
    model_1.save_model(out_path)


if __name__ == '__main__':
    train_model()
