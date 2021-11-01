# Antisemitism-Detector 
This is the repository to my bachelors thesis. The code addresses different approaches described in my thesis.

---
## Preparing the environments.

I recommend using anaconda environment.s The *.yml files make sure that the correct library versions are installed.

```
git clone https://github.com/Nicolas-le/antisemitism-detector.git
cd antisemitism-detector/
conda env create -f ./anaconda_envs/data_analysis_app.yml
conda env create -f ./anaconda_envs/antisem_detector.yml
conda env create -f ./anaconda_envs/case_study.yml
```
---

## How-To Part 1: Main functionalities.

This chapter explains how to use the main functionalities.
The use of the analysis tool and the training of the model.

### Analysis Tool
The analysis tool runs as a local web app with flask. Just use your browser of choice to go on the shown local address after executing the code.
The start might take a little while because some models need to be initialized.

Copy the models into the corresponding directories. The models are only provided once for data size reasons and they are
tracked through git large file storage. **To get an overview over the structure you can look below under project structure.**

`./detector/distil_bert/models/with_keywords/DB_Modell_A/*` to `./data_set/analysis/App/classifier_models/trained_with_kws/`
`./detector/distil_bert/models/without_all_keywords/DB_Modell_B/*` to `./data_set/analysis/App/classifier_models/trained_without_all_kws/`
`./detector/distil_bert/models/without_slur_keywords/DB_Modell_C/*` to `./data_set/analysis/App/classifier_models/trained_without_slur_kws/`

```
conda activate data_analysis_app
cd ./data_set/analysis
python run_app.py
```

This is the expected output, in this case you have to go to the local address: http://127.0.0.1:5000/

```
 * Serving Flask app 'App.app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Train the model
```
conda activate antisem_detector
cd ./detector/distil_bert
```

There are three **training** options. 

**DB-Modell A: Training with all keywords** `python train.py 1`

**DB-Modell B: Training without all keywords** `python train.py 2`

**DB-Modell C: Training without slur/racist keywords** `python train.py 3`

The trained models will be saved into a directory named after the timestamp they were created
under `./detector/distil_bert/models/`

There are three **test** options. You will get some several metrics, f.ex. accuracy, confusion matrix, precision, recall, f1-score

**Test DB-Modell A** `python test.py 1`

**Test DB-Modell B** `python test.py 2`

**Test DB-Modell C** `python test.py 3`

---
## How-To Part 2: Preparing steps.

This chapter explains the use of the preparing steps to the main functionalities.
F.ex. the creation of specific datasets that are provided with the git. The use
is explained nevertheless to ensure the adaption of the code for your own projects.

### Dataset creations
`conda activate data_analysis_app`

#### Create the initial dataset

You have to get a list of thread IDs that are currently available by the 4chan-API Archive. This list gets updated by 4chan and
new threads are added to the end. You can get the JSON file here: `https://a.4cdn.org/pol/archive.json`. 
You save the file as `./data_set/creation/initial_database/pol_archive_thread_IDs.json`! The thread IDs are necessary because this is the only
way to access a specific thread. Because this is the only possibility and the script shouldn't save the same posts twice
you have to tell the script the last thread ID of the previous list of thread IDs you scraped. 
This happens if you scrape on several days and the list of thread IDs was refreshed by 4chan. 
The script stops when it reaches the newest thread of your previous scraping.

```
cd ./data_set/creation/initial_database
python 4chan_scraper.py <Last thread ID of previous list>
```
#### Create the database used for the analysis tool

```
cd ./data_set/creation/detection_database
python analysis_db_creator.py
```

#### Create a csv of the antisemitic keywords for later reference

The list has been created with the latest keyword list. If you want to change keywords, add them to the dictionary in
the `keyword_csv.py` file and run the script:

```
cd ./data_set/creation/create_keyword_csv
python keyword_csv.py
```

#### Create the labeled antisemitic subset

This is the tool created to presort and then label the comments for the training of the model. For this tool there 
are command line arguments implemented with argparse. I wrote a documentation in it, which is cited here.

```
cd ./data_set/creation/antisem_subset_database
conda activate data_analysis_app

usage: main.py [-h] [--filler] [--normal_creator]

The main labeling tool. Decide for the filler, which only inserts non
antisemitic comments or the normal creator which inserts depending on your
decision. The filler shows only comments without keywords, and the normal
creator only those with appearing keywords.

optional arguments:
  -h, --help        show this help message and exit
  --filler          Select this argument if you want to use the filler
                    functionality.
  --normal_creator  Select this argument if you want to use the normal creator
                    functionality.


```

### Other concepts and preparations for the models

`conda activate antisem_detector`

#### Create the training csv-files

```
cd ./detector/create_training_csv_files
python create_csv_files.py
```

#### Keyword approach
```
cd ./detector/keyword_approach
python keyword_classifier.py
```
#### Naive Bayes

```
cd ./detector/naive_bayes
python naive_bayes.py
```

---

## How-To Part 3: Case study.
This code is written with the single purpose to create the case study presented in the thesis. Thus, there are various 
hard-coded elements present. -> F.ex. for file names and paths. 

1. Save the DistilBERT Model that you want to use to `./case_study/resources/disitlbert_model`.
2. Get access to the YouTube API V3 (https://developers.google.com/youtube/v3)
3. Save your credential to the local file `./case_study/resources/api_cred.json`
4. Add the IDs of the youtube-videos you want to scrape to a file similar to `./case_study/resources/video_ids_corey_whole.csv`
5. Download the comments of the channel via `youtube_api.py`
6. Hit the `main.py` file ot classify the comments

```
usage: main.py [-h] [--plotting]

Classify the comments and get some metrics. This tool is based on the previous
use of the youtube_api.py file and therefore the download and creation of the
data.

optional arguments:
  -h, --help  show this help message and exit
  --plotting  Select this argument if you want to use the plotting
              functionality.
```

---
## Project Structure

The following tree shows the structure of the whole project. This documentation should help fix errors if there are
problems regarding the git, the path structures or missing files.

```
antisemitism-detector
|   README.md
|
└──── anaconda_envs
|     |     - these are the yml files for the anaconda environments with all the dependencies for the code
|     |     antisem_detector.yml
|     |     data_analysis_app.yml
|     |     case_study.yml
|
└──── case_study
|     |     classify_comment.py
|     |         - classifies the comments collencted from youtube
|     |     plotting.py
|     |         - create the plotly charts from the classified comments
|     |     youtube_api.py
|     |         - uses the youtube api to collect the comments
|     |
|     └──── resources
|     |     |       api_cred.json
|     |     |       collected_comments_corey_israel.json
|     |     |           - all the collected comments to the I-videos
|     |     |       collected_comments_corey_palestinian.json
|     |     |           - all the collected comments to the P-videos
|     |     |       collected_comments_corey_whole.json
|     |     |           - all the collected comments
|     |     |       video_ids_corey_israel.csv
|     |     |           - the video ids for the youtube api of the I-videos
|     |     |       video_ids_corey_palestinian.csv
|     |     |           - the video ids for the youtube api of the P-videos
|     |     |       video_ids_corey_whole.csv
|     |     |           - the video ids for the youtube api of all the videos
|     |     |
|     |     └──── distilbert_model
|     |     |     |     config.json
|     |     |     |     pytorch_model.bin
|     |     |     |     training_args.bin
|     |     |     |
|         
└──── data_set
|     |     4chan_pol_database.json
|     |         - the complete scraped dataset after preprocessing
|     |     antisemitic_subset.json
|     |         - the labeled subset (1500: antisem, 1500: not antisem)
|     |     detections_4chan_pol_database.json
|     |         - aggregated analysis and insights of the "4chan_pol_database.json" database, used for the analysis app
|     |     keywords.csv
|     |         - all the keywords as a csv file for later references.
|     |  
|     └──── analysis
|     |     |   run_app.py
|     |     |   
|     |     └──── App
|     |     |     |     app.py
|     |     |     |         - the main backend for the web app
|     |     |     |     data_preprocessing.py
|     |     |     |         - preprocessing of the data, f.ex. from the database retrieve
|     |     |     |     db_retrieve.py
|     |     |     |         - database connections
|     |     |     |     plotly_graphs.py
|     |     |     |         - create the plotly charts for visualizations
|     |     |     |     utils.py
|     |     |     |         - various utils suiting the backend
|     |     |     |
|     |     |     └────  classifier_models
|     |     |     |     └──── trained_with_kws
|     |     |     |     |     |       config.json
|     |     |     |     |     |       pytorch_model.bin
|     |     |     |     |     |       training_args.bin
|     |     |     |     |     |
|     |     |     |     └──── trained_without_all_kws
|     |     |     |     |     |       config.json
|     |     |     |     |     |       pytorch_model.bin
|     |     |     |     |     |       training_args.bin
|     |     |     |     |     |
|     |     |     |     └──── trained_without_slur_kws
|     |     |     |     |     |       config.json
|     |     |     |     |     |       pytorch_model.bin
|     |     |     |     |     |       training_args.bin
|     |     |     |     
|     |     |     └────  static
|     |     |     |     |       frontpage.css
|     |     |     |     |       plots.css
|     |     |     |     |       stylesheet.css
|     |     |     |      
|     |     |     └────  templates
|     |     |     |     |       classifier.html
|     |     |     |     |       home.html
|     |     |     |     |       keyword.html
|     |     |     |     |       plots.html
|     |     |     |     |       templates.html
|     |     
|     └──── creation
|     |     └──── antisem_subset_database
|     |     |     |     create_antisemitic_subset.py
|     |     |     |         - the SubsetCreator class keeping track of the labeling
|     |     |     |     create_initial_subset.py
|     |     |     |         - create the initial subsets with keywords and without
|     |     |     |     db_retrieve.py
|     |     |     |         - handle the database connection
|     |     |     |     fill_subset.py
|     |     |     |         - the filler class created for the described lack of non antisemtic comments
|     |     |     |     utils.py
|     |     |     |         - various util functions
|     |     |     |     main.py
|     |     |     |         - starts and controls the whole process
|     |     |     |
|     |     |     └──── initial_subsets    
|     |     |     |     |      initial_kw_subset.py 
|     |     |     |     |           - the initial sort with keywords
|     |     |     |     |      initial_non_kw_subset.py 
|     |     |     |     |           - the presort without keywords for the filling
|     |     | 
|     |     └──── create_keyword_csv   
|     |     |     |     keyword_csv.py
|     |     |     
|     |     └──── detection_database
|     |     |     |     analysis_db_creator.py
|     |     |     |         - handle the main process for the creation
|     |     |     |     data_preprocessing.py
|     |     |     |         - create the detections
|     |     |     |     db_retrieve.py
|     |     |     |         - handle the database connection
|     |     |     
|     |     └──── initial_database
|     |     |     |     pol_archive_thread_IDs.json
|     |     |     |         - list of thread IDs currently vailable throught the 4chan API
|     |     |     |     4_chan_scraper.py
|     |     |     |         - main API handling
|     |     |     |     data_cleaner.py
|     |     |     |         - preprocess the collected threads
|    
|
└──── detector        
|     |     data_train.csv
|     |     data_test.csv
|     |     data_without_all_keywords_train.csv
|     |     data_without_all_keywords_test.csv
|     |     data_without_slur_keywords_train.csv
|     |     data_without_slur_keywords_test.csv
|     |
|     └──── create_training_csv_files
|     |     |       create_csv_files.py
|     |     |       post.py
|     |     |       utils.py
|     |     
|     └──── distil_bert
|     |     |       metrics.py     
|     |     |       train.py
|     |     |       test.py
|     |     |       utils.py
|     |     |
|     |     └──── models
|     |     |     |     - this directory normally contains various trained models, only the models from thesis are provided
|     |     |     └──── with_keywords
|     |     |     |     └──── DB_Modell_A     
|     |     |     |     |     |     config.json
|     |     |     |     |     |     pytorch_model.bin
|     |     |     |     |     |     training_args.bin
|     |     |     |
|     |     |     └──── without_all_keywords
|     |     |     |     └──── DB_Modell_B    
|     |     |     |     |     |     config.json
|     |     |     |     |     |     pytorch_model.bin
|     |     |     |     |     |     training_args.bin
|     |     |     |
|     |     |     └──── without_slur_keywords
|     |     |     |     └──── DB_Modell_C   
|     |     |     |     |     |     config.json
|     |     |     |     |     |     pytorch_model.bin
|     |     |     |     |     |     training_args.bin
...
|     |     └──── saved_metrics
|     |     |     |     confusion_matrix.py
|     |     |     |         - a script provided by : https://github.com/DTrimarchi10 to style a confusion matrix
|     |     |     |     confusion_matrix_with_keywords.png   
|     |     |     |     confusion_matrix_without_all_keywords.png
|     |     |     |     confusion_matrix_without_slur_keywords.png
|     |     |     |     false_pos_trained_with_kws.csv
|     |     |     |     false_pos_trained_without_slurs.csv
|     |
|     └──── keyword_approach
|     |     |       keyword_classifer.py
|     |     |       keywords.csv
|     |
|     └──── naive_bayes
|     |     |       naive_bayes.py
```
