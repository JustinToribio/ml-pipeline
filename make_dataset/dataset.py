import click
# import dask.dataframe as dd
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# from distributed import Client
from pathlib import Path


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
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Connect to the dask cluster
    # c = Client('dask-scheduler:8786')

    # load data as a dask Dataframe if you have trouble with dask
    # please fall back to pandas or numpy
    # ddf = dd.read_csv(in_csv, blocksize=1e6)

    # we set the index so we can properly execute loc below
    # ddf = ddf.set_index('Unnamed: 0')

    # trigger computation
    # n_samples = len(ddf)

    # TODO: implement proper dataset creation here
    # http://docs.dask.org/en/latest/dataframe-api.html

    # split dataset into train test feel free to adjust test percentage
    # idx = np.arange(n_samples)
    # test_idx = idx[:n_samples // 10]
    # test = ddf.loc[test_idx]

    # train_idx = idx[n_samples // 10:]
    # train = ddf.loc[train_idx]

    
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


if __name__ == '__main__':
    make_datasets()
