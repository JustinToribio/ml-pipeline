# Running the Pipeline

Execute all of the following commands from the parent directory of this repository.

Build the task images:

`./build-task-images.sh 0.1`

Execute the pipeline: 

`docker-compose up orchestrator` 

# Submission Artifacts

The below submission artifacts are located in the `artifacts` directory.

## Model Evaluation Report
The final task of this pipeline will automatically produce the model evaluation report in 3 different formats in the `data_root/reports` directory: a pdf, html file and executed Jupyter Notebook.

The output in the reports (calculations and plots) will automatically change when the pipeline is run with different inputs (i.e. different data, parameters etc...).

The html file produces the best rendering and formatting, so I printed a copy of that file as a pdf for this submission artifact.

## Pipeline Logs
There is a `.log` file for each pipeline task located in the `artifacts/logs` directory.  They were created from a complete run of the pipeline on my local machine.

The `weasyprint` module in the `EvaluateModel` task, which converts the html report into a pdf, is very verbose when executed and I could not find a way to execute it silently.  This is why you will see so many `WARNING` logs in `evaluatemodel.log`, as it is simply ignoring a lot of formatting options.
