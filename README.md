[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FAME Lab](https://img.shields.io/badge/Bioinformatics-EdwardsLab-03A9F4)](https://fame.flinders.edu.au/)


# Phynteny

## Phynteny: Synteny-based annotation of viral genes 

Phynteny is still a work in progress and the LSTM model has not yet been optimised. Use with caution! 

## Installation 

```
git clone https://github.com/susiegriggo/Phynteny
cd Phynteny 
pip install . 
```

## Usage 

test. Phynteny takes a genbank file containing PHROG annotations as input. If you phage is not yet in this format, [pharokka](https://github.com/gbouras13/pharokka) can take your phage (in fasta format) to a genbank file with PHROG annotations.  

**Reccomended:**  
```
phynteny test_phage.gbk  -o test_phage_reannotated.gbk 
```

If you wish to specify your own LSTM model and thresholds, you can run: 
```
phynteny test_phage.gbk -o test_phage_reannotated.gbk -m your_model.h5 -t custom_thresholds.pkl 
```

where custom_thresholds is dictionary contanining a softmax threshold for each of the nine PHROG categories 

## Training Phynteny 
Phynteny has already been trained for you on a dataset containing over 1 million prophages! However, If you feel inclined to train Phynteny yourself you can. <br> 
Phynteny is trained using genbank files containing PHROG annotations such as those generated by pharokka. 

Use `-i` as a text file with the paths to the genbank files 

```
python generate_training_data.py -i genbank_files.txt -o training_dataset.pkl -max_genes 120 -gene_cat 4 -c 11
python train_model.py ... 
```

This command generates training data including prophages with a maximum of 120 genes where each contains at least four different PHROG categories. The output data is separated into 11 different chunks which can be used for training with k-fold validation. 

**WARNING** Without a GPU training will take a very very long time! 

scripts are included to test your train models. Can refer to the included notebooks. 

## Bugs and Suggestions 
If you break Phynteny or would like to make any suggestions please open an issue or email me at susie.grigson@flinders.edu.au 


## Citation 
TODO 
If you use pharokka to first annotate your phage please site it as well! 
