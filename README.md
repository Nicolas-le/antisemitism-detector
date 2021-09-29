# Antisemitism-Detector 
Learn linguistic features of antisemitic language. 

---

## Dataset

4chan.org/pol Posts

subset labeled antisem/ not antisem

## File Structure

```
antisemitism-detector
|   README.md
|
└──── anaconda_envs
|     |     antisem_detector.yml
|     |     data_analysis_app.yml
|
└──── data_set
|     |     4chan_pol_database.json
|     |         - the complete scraped dataset after preprocessing
|     |     antisemitic_subset.json
|     |         - the labeled subset (1500: antisem, 1500: not antisem)
|     |     detections_4chan_pol_database.json
|     |         - aggregated analysis and insights of the "4chan_pol_database.json" database, used for the analysis app
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
