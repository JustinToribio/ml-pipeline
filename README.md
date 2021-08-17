# Executing a complete machine learning pipeline

This project will execute a complete machine learning pipeline with Docker Compose and Luigi.  With just 2 commands, the full pipeline will download the data, process it, train a gradient boosting machine with XGBoost and generate a dynamic evaluation report that communicates the model’s effectiveness and suitability for a non-technical audience.

# Requirements

You will need Docker and Docker Compose to run this project: 

* [How to install Docker](https://docs.docker.com/engine/installation/)
* [How to install Docker Compose](https://docs.docker.com/compose/install/)

# Context

The objective of the pipeline is to train and evaluate a wine rating prediction machine learning model.  

The pipeline will download a dataset of 10,000 different wines, which includes various qualitative and quantitative attributes of the wines, including the wines' ratings ("points").

The pipeline will then process the dataset, train a gradient boosting machine and generate a dynamic report that evaluates the model.

Here is an excerpt of the dataset:

country|description|designation|points|price|province|region_1|region_2|taster_name|taster_twitter_handle|title|variety|winery
---|---|---|---|---|---|---|---|---|---|---|---|---
Italy|Fragrances suggest hay, crushed tomato vine and exotic fruit. The bright but structured palate delivers peach, papaya, cantaloupe and energizing mineral notes alongside fresh acidity. It's nicely balanced with good length,|Kirchleiten|90|30.0|Northeastern Italy|Alto Adige||Kerin O’Keefe|@kerinokeefe|Tiefenbrunner 2012 Kirchleiten Sauvignon (Alto Adige)|Sauvignon|Tiefenbrunner
France|Packed with fruit and crisp acidity, this is a bright, light and perfumed wine. Red-berry flavors are lifted by red currants and a light spice. Drink now for total freshness.||87|22.0|Loire Valley|Sancerre||Roger Voss|@vossroger|Bernard Reverdy et Fils 2014 Rosé (Sancerre)|Rosé|Bernard Reverdy et Fils

# Running the pipeline



Execute all of the following commands from the parent directory of this repository.

Build the task images:

`./build-task-images.sh 0.1`

Execute the pipeline: 

`docker-compose up orchestrator` 


# Output
## Model evaluation report
The final task of this pipeline will automatically produce the model evaluation report in 3 different formats in the `data_root/reports` directory: a pdf, html file and executed Jupyter Notebook.

The output in the reports (calculations and plots) will automatically change when the pipeline is run with different inputs (i.e. different data, parameters etc...).

The html file produces the best rendering and formatting.
