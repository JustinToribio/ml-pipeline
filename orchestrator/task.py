import logging

import luigi
import os
from pathlib import Path

from util import DockerTask

VERSION = os.getenv('PIPELINE_VERSION', '0.1')


class Debug(DockerTask):
    """Use this task with appropriate image to debug things."""

    @property
    def image(self):
        return f'code-challenge/download-data:{VERSION}'

    @property
    def command(self):
        return [
            'sleep', '3600'
        ]


class DownloadData(DockerTask):
    """Initial pipeline task downloads dataset."""

    fname = luigi.Parameter(default='wine_dataset')
    out_dir = luigi.Parameter(default='/usr/share/data/raw/')
    url = luigi.Parameter(
        default='https://github.com/datarevenue-berlin/code-challenge-2019/'
                'releases/download/0.1.0/dataset_sampled.csv'
    )

    @property
    def image(self):
        return f'code-challenge/download-data:{VERSION}'

    @property
    def command(self):
        return [
            'python', 'download_data.py',
            '--name', self.fname,
            '--url', self.url,
            '--out-dir', self.out_dir
        ]

    def output(self):
        out_dir = Path(self.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        return luigi.LocalTarget(
            path=str(out_dir/f'{self.fname}.csv')
        )


class MakeDatasets(DockerTask):
    """Pipeline task to make train and test datasets ready for ML model."""
    
    out_dir = luigi.Parameter(default='/usr/share/data/datasets/')

    @property
    def image(self):
        return f'code-challenge/make-dataset:{VERSION}'

    def requires(self):
        return DownloadData()

    @property
    def command(self):
        return [
            'python', 'dataset.py',
            '--in-csv', self.input().path,
            '--out-dir', self.out_dir
        ]

    def output(self):
        return luigi.LocalTarget(
            path=str(Path(self.out_dir) / '.SUCCESS')
        )


class TrainModel(DockerTask):
    """Pipeline task to train a ML model."""

    fname = luigi.Parameter(default='model')
    out_dir = luigi.Parameter(default='/usr/share/data/model/')

    @property
    def image(self):
        return f'code-challenge/train-model:{VERSION}'

    def requires(self):
        return MakeDatasets()

    @property
    def command(self):
        return [
            'python', 'train_model.py',
            '--name', self.fname,
            '--x-train', self.input().path.replace('.SUCCESS', 'X_train.pkl'),
            '--y-train', self.input().path.replace('.SUCCESS', 'y_train.pkl'),
            '--x-test', self.input().path.replace('.SUCCESS', 'X_test.pkl'),
            '--y-test', self.input().path.replace('.SUCCESS', 'y_test.pkl'),
            '--out-dir', self.out_dir
        ]

    def output(self):
        return luigi.LocalTarget(
            path=str(Path(self.out_dir) / f'{self.fname}.json')
        )
