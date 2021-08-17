import click
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def _save_datasets(X_train, X_test, y_train, y_test, outdir: Path):
    """Save data sets into nice directory structure and write SUCCESS flag."""

    out_X_train = outdir / 'X_train.pkl/'
    out_X_test = outdir / 'X_test.pkl/'
    out_y_train = outdir / 'y_train.pkl/'
    out_y_test = outdir / 'y_test.pkl/'
    flag = outdir / '.SUCCESS'

    X_train.to_pickle(str(out_X_train))
    X_test.to_pickle(str(out_X_test))
    y_train.to_pickle(str(out_y_train))
    y_test.to_pickle(str(out_y_test))

    flag.touch()


@click.command()
@click.option('--in-csv')
@click.option('--out-dir')
def make_datasets(in_csv, out_dir):
    """Create train and test datasets from a csv and save them to disk.

    Parameters
    ----------
    in_csv: str
        file path to the input csv file.
    out_dir: str
        directory where files should be saved to.

    Returns
    -------
    None
    """
    log = logging.getLogger('make-datasets')

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    log.info('Making datasets')
    log.info(f'Will write to {out_dir}')
    
    # Pandas Implementation
    # Read the data
    X = pd.read_csv(in_csv, index_col=0)

    # Remove rows with missing target and separate target from predictors
    X.dropna(axis=0, subset=['points'], inplace=True)
    y = X.points              
    X.drop(['points'], axis=1, inplace=True)

    # Break off validation set from training data
    X_train_full, X_valid_full, y_train, y_valid = train_test_split(
        X, y, train_size=0.8, test_size=0.2, random_state=0)

    # Drop high-cardinality and unnecessary features    
    low_cardinality_cols = [
        cname for cname in X_train_full.columns 
        if X_train_full[cname].nunique() < 1000 and 
        X_train_full[cname].dtype == "object"
        ]
    low_cardinality_cols.remove('taster_twitter_handle')

    # Select numeric columns
    numeric_cols = [
        cname for cname in X_train_full.columns
        if X_train_full[cname].dtype in ['int64', 'float64']
        ]

    # Keep selected columns only
    my_cols = low_cardinality_cols + numeric_cols
    X_train = X_train_full[my_cols].copy()
    X_valid = X_valid_full[my_cols].copy()

    # One-hot encode the data and align the columns between the 
    # train and validation datasets
    X_train = pd.get_dummies(X_train)
    X_valid = pd.get_dummies(X_valid)
    X_train, X_valid = X_train.align(X_valid, join='left', axis=1)

    # Save the datasets
    _save_datasets(X_train, X_valid, y_train, y_valid, out_dir)

    log.info('Making datasets complete')


if __name__ == '__main__':
    make_datasets()
