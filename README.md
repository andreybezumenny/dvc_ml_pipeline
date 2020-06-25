# dvc ml pipeline

install requirements ... 

## dvc ml pipeline 
```
+-----------------+     +----------------------+     +------------------------------+
|                 |     |                      |     |                              |
|  Extract data   +-----> Transform XLM to tsv +-----> Splitting training and test  |
|                 |     |                      |     |                              |
+-----------------+     +----------------------+     +--------------+---------------+
                                                                    |
                                                                    |
                                                                    |
+-----------------+     +----------------------+          +---------v--------+
|                 |     |                      |          |                  |
| Evaluate model  <-----+     Train model      <----------+ Extract features |
|                 |     |                      |          |                  |
+-----------------+     +----------------------+          +------------------+
```


1) create create_datase.py which will download/split/... datsets

2) create config.py which contain all path 

3) create assets dir which will include all dvc files (trained models, features, metrics etc.)

4) create pipeline files (extract/train/evaluate etc.)

5) store results:

    1) commit all new to git repo 
    
    2) start with -> `dvc init` it'll create .dvc dir
    
    3) choose location option (I've chosen local) `dvc remote add -d localremote /tmp/dvc-storage`
    
    4) disable analytics `dvc config core.analytics false`. You can check .dvc/config file
    
    5) To make our experiments reproducible we are going to using another command that dvc provides: `dvc run`
    So we can delete all from assets dir. And create ignore file in assets dir.
        
        1) `dvc run  \
        -d train/create_datase.py \
        -o assets/data \
        -n features \
        python train/create_datase.py` it'll create all files
        To track the changes with git, run:
        `git add dvc.lock dvc.yaml`
        2) ` dvc run -d train/extract_features.py -d assets/data -o assets/features -n extract_features python train/extract_features.py `
        To track the changes with git, run:
        `git add dvc.lock dvc.yaml`
        3) train model
        `dvc run -d train/train_model.py -d assets/features -o assets/models -n train_model python train/train_model.py`
        4) storing evaluation metrics 
        `dvc run -d train/evaluate_model.py -d assets/features -d assets/models -M assets/metrics.json -n evaluation  python train/evaluate_model.py `
        
    6) Commit all 
    `git add .`
    `git commit -m 'Complete dvc lr experiment'`
    `git tag -a 'lr-experiment' -m 'Experiment with lr'`
    
6) Check metrics with command:
    `dvc metrics show -T`
    ```workspace:                                                                      
            assets/metrics.json:
                    0.precision: 0.8385269121813032
                    0.recall: 0.8283582089552238
                    0.f1-score: 0.8334115438761144
                    0.support: 1072
                    1.precision: 0.8141414141414142
                    1.recall: 0.8249744114636642
                    1.f1-score: 0.8195221148957804
                    1.support: 977
                    accuracy: 0.8267447535383113
                    macro avg.precision: 0.8263341631613587
                    macro avg.recall: 0.826666310209444
                    macro avg.f1-score: 0.8264668293859474
                    macro avg.support: 2049
                    weighted avg.precision: 0.8268994687528153
                    weighted avg.recall: 0.8267447535383113
                    weighted avg.f1-score: 0.8267888146844178
                    weighted avg.support: 2049
    lr-experiment: <------- THIS IS VERSION OF EXPERIMENT 
            assets/metrics.json:
                    0.precision: 0.8385269121813032
                    0.recall: 0.8283582089552238
                    0.f1-score: 0.8334115438761144
                    0.support: 1072
                    1.precision: 0.8141414141414142
                    1.recall: 0.8249744114636642
                    1.f1-score: 0.8195221148957804
                    1.support: 977
                    accuracy: 0.8267447535383113
                    macro avg.precision: 0.8263341631613587
                    macro avg.recall: 0.826666310209444
                    macro avg.f1-score: 0.8264668293859474
                    macro avg.support: 2049
                    weighted avg.precision: 0.8268994687528153
                    weighted avg.recall: 0.8267447535383113
                    weighted avg.f1-score: 0.8267888146844178
                    weighted avg.support: 2049
    ```
7) Change experiment:

Try now rf classifier. So change the code in  train_model.py  
Then run `dvc repro dvc.yaml` 
it will find which files were changed and rerun only that steps
`git add .`
`git commit -m 'Complete dvc rf experiment'`
`git tag -a 'rf-experiment' -m 'Experiment with rf'`
`dvc metrics show -T`


