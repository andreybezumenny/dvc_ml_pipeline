# dvc ml pipeline

start with -> dvc init 
it'll create .dvc dir
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

    1) commit to git repo 
