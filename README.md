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
