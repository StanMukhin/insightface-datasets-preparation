# insightface-datasets-preparation
Data preparation scripts for training and evaluating with insightface
There are some rudiment things I left here. Cropping certain area for example. Change it if needed

## 1. Set up environment

Use conda or virtualenv
```shell
pip install -r requirements.txt
```

## 2. Prepare dataset

Copy dataset in "dataset"
It has to be like this:
```shell
# directories and files in your dataset
./dataset
├── folder_name
│   ├── image_1.jpg
│   ├── doesnt_matter_how_it_calls.jpeg
├── another-folder
│   ├── fuhewur.jpg
│   ├── ndjkfsjdfnj.jpeg
```

## 3. Run
Just run
```shell
python prepare_dataset.py
```
