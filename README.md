# Antisemitism-Detector 
Learn linguistic features of antisemitic language. 

---
## Preparing the environments.

I recommend using an anaconda environment. The *.yml files make sure that the correct library versions are installed.

```
git clone https://github.com/Nicolas-le/antisemitism-detector.git
cd antisemitism-detector/
conda env create -f ./anaconda_envs/data_analysis_app.yml
conda env create -f ./anaconda_envs/antisem_detector.yml
```
---

## How-To Part 1: Main functionalities.

This chapter explains how to use the main functionalities.
The use of the analysis tool and the training of the model.

### Analysis Tool
The analysis tool runs as a local web app with flask. Just use your browser of choice to go on the shown local adress after executing the code.
The start might take a little while because some models need to be initialized.

```
conda activate data_analysis_app
cd ./data_set/analysis
python run_app.py
```


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















































---
### Create and train the proposed models

---
### Case study

This code is written with the single purpose to create the case study presented in the thesis. Thus there are various 
coded elements present.



---
## File Structure

The following tree shows the structure of the whole project. This documentation should help fix errors if there are
problems regarding the git, the path structures or missing files.

```
antisemitism-detector
|   README.md
|
└──── anaconda_envs
|     |     antisem_detector.yml
|     |     data_analysis_app.yml
|
└──── case_study
|     |     classify_comment.py
|     |     plotting.py
|     |     youtube_api.py
|     |
|     └──── resources
|     |     |       collected_comments_corey_israel.json
|     |     |       collected_comments_corey_palestinian.json
|     |     |       collected_comments_corey_whole.json
|     |     |       collected_comments_corey_israel.json
|     |     |       collected_comments_corey_palestinian.json
|     |     |       collected_comments_corey_whole.json
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
|     |     |     |     data_preprocessing.py
|     |     |     |     db_retrieve.py
|     |     |     |     plotly_graphs.py
|     |     |     |     utils.py
|     |     |     |
|     |     |     └────  classifier_model
|     |     |     |     |       config.json
|     |     |     |     |       pytorch_model.bin
|     |     |     |     |       training_args.bin
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
|     |     |     |     create_initial_subset.py
|     |     |     |     db_retrieve.py
|     |     |     |     fill_subset.py
|     |     |     |     utils.py
|     |     |     |     main.py
|     |     |     |
|     |     |     └──── initial_subsets    
|     |     |     |     |      initial_kw_subset.py 
|     |     |     |     |      initial_non_kw_subset.py 
|     |     |          
|     |     └──── detection_database
|     |     |     |     analysis_db_creator.py
|     |     |     |     data_preprocessing.py
|     |     |     |     db_retrieve.py
|     |     |     
|     |     └──── initial_database
|     |     |     |     pol_archive_thread_IDs.json
|     |     |     |     4_chan_scraper.py
|     |     |     |     data_cleaner.py
|    
|
└──── detector        
|     |     data_train.csv
|     |     data_train_without_all_keywords.csv
|     |     data_train_without_slur_keywords.csv
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
|     |     |     |



```
