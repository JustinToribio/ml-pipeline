#!/usr/bin/env bash

# Get the CLI parameters
OUT_DIR=$1
MODEL_PATH=$2
X_VALID_PATH=$3
Y_VALID_PATH=$4

# Create the output directory and copy in the report images
mkdir $OUT_DIR
cp -r images $OUT_DIR/images

# Execute the report notebook with the CLI parameters
# and save the new notebook to the output directory
papermill pre_report.ipynb \
          $OUT_DIR/evaluation_report.ipynb \
          -p model_path $MODEL_PATH \
          -p x_valid_path $X_VALID_PATH \
          -p y_valid_path $Y_VALID_PATH

# Clean and convert the report notebook to a .html file
# in the output directory
jupyter nbconvert $OUT_DIR/evaluation_report.ipynb \
                  --TagRemovePreprocessor.remove_cell_tags='{"hide-cell"}' \
                  --to "html"

# Convert the .html report to a .pdf report
weasyprint $OUT_DIR/evaluation_report.html $OUT_DIR/evaluation_report.pdf

# Add the .SUCCESS flag to the output directory
touch $OUT_DIR/.SUCCESS
