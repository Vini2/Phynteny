[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FAME Lab](https://img.shields.io/badge/Bioinformatics-EdwardsLab-03A9F4)](https://fame.flinders.edu.au/)


# Phynteny

## Phynteny: Synteny-based annotation of bacteriophage genes 

Approximatley 65% of all bacteriophage (phage) genes cannot be attributed a known biological function. Phynteny uses a long-short term memory model trained on phage synteny (the conserved gene order across phages) to assign hypothetical phage proteins to a [PHROG](https://phrogs.lmge.uca.fr/) category. 

Phynteny is still a work in progress and the LSTM model has not yet been optimised. Use with caution! 

**NOTE** This version of Phynteny will only annotate phages with 120 genes or less due to the architecture of the LSTM. We aim to adjust this in future versions. 


## Dependencies
Phynteny installation requires Python 3.7 or above. You will need the following python dependencies to run Phynteny and it's related support scripts. The latest tested versions of the dependencies are: 
* [python](https://www.python.org/) - version 3.9.0 
* [sklearn](https://scikit-learn.org/stable/) - version 1.2.2 
* [biopython](https://biopython.org/) - version 1.81
* [numpy](https://numpy.org/) - version 1.21.0 (Windows, Linux, Apple Intel), version 1.24.0 (Apple M1/M2)
* [tensorflow](https://www.tensorflow.org/) - version 2.9.0 (Windows, Linux, Apple Intel), tensorflow-macos version 2.11 (Apple M1/M2)
* [pandas](https://pandas.pydata.org/) - version 2.0.2
* [loguru](https://loguru.readthedocs.io/en/stable/) - version 0.7.0
* [click](https://click.palletsprojects.com/en/8.1.x/) - version 8.1.3 <br> 

We reccomend GPU support if you are training Phynteny. This requires CUDA and cuDNN:
* [CUDA toolkit](https://developer.nvidia.com/cuda-toolkit) - version 11.2 
* [cuDNN](https://developer.nvidia.com/cudnn) - version 8.1.1 

## Installation 

```
git clone https://github.com/susiegriggo/Phynteny.git --branch no_unknowns --depth 1 
cd Phynteny 
pip install . 
```

## Usage 

Phynteny takes a genbank file containing PHROG annotations as input. If you phage is not yet in this format, [pharokka](https://github.com/gbouras13/pharokka) can take your phage (in fasta format) to a genbank file with PHROG annotations.  Phynteny will then return a genbank files and a table containing the details of the predictions made using phynteny. Each prediction is accompanied by a 'phyteny score' which ranges between 1-10 and a recalibrated confidence score. 

**Reccomended**  
```
phynteny test_data/test_phage.gbk  -o test_phynteny
```

**Custom** 

If you wish to specify your own LSTM model, run: 

```
phynteny test_phage.gbk -o test_phage_phynteny -m your_models -t confidence_dict.pkl 
```
Details of how to train the phynteny models and generate confidence estimates is detailed below. 

## Training Phynteny 
Phynteny has already been trained for you on a dataset containing over 1 million prophages! However, If you feel inclined to train Phynteny yourself you can. 

### Generate Training Data 
Phynteny is trained using genbank files containing PHROG annotations such as those generated by pharokka. First you will need to generate training data using the `generate_training_data.py` script. This script takes a text file containing the genbank files' paths and includes parameters to specify the maximum number of genes in each prophage, the number of different PHROG categories which should be present in each phage. This outputs four pickled dictionaries, the X components of the testing and training data and the y components of the testing and training data. For example, to generate data from a textfile called `genbank_files.txt` where we would only like to include phages with 120 genes or less with genes from at least four different PHROG categories we would run the command:  

```
python scripts/generate_training_data.py -i genbank_files.txt -p phynteny_data -max_genes 120 -g 4
```

### Train the model 
After this, we can train the model by running the `train_model.py` script. This uses cross-validation to produce several models. The parameters for the LSTM can be adjusted including the numer of hidden layers, memory cells and dropout. For the full list run the command `python scripts/train_model.py --help`. Otherwise we can this command which will generate models with the prefix, `your_trained_phynteny`. 
```
python scripts/train_model.py -x training_data_X.pkl -y training_data_y.pkl -o your_trained_phynteny 
```

**WARNING** Without a GPU training will take a very very long time! 

### Compute Confidence 
Once you've trained your model you will need to take steps to generate an object specific to your model which can be used to compute the confidence of your predictions. We compute confidence using kernel densities (you can read why this is a good idea [here](https://arxiv.org/abs/2207.06529)). To do this, use the `compute_confidence.py` scripts and parse the testing data. 

```
python scripts/compute_confidence.py -b model_directory -x testing_data_X.pkl -y testing_data_y.pkl -o confidence_densities 
```
## Performance 

Coming soon: Notebooks demonstrating the performance of the model 

## Bugs and Suggestions 
If you break Phynteny or would like to make any suggestions please open an issue or email me at susie.grigson@flinders.edu.au 

## Citation 
If you use pharokka to annotate your phage before using Phynteny please site it as well! <br> 

George Bouras, Roshan Nepal, Ghais Houtak, Alkis James Psaltis, Peter-John Wormald, Sarah Vreugde, Pharokka: a fast scalable bacteriophage annotation tool, Bioinformatics, Volume 39, Issue 1, January 2023, btac776, https://doi.org/10.1093/bioinformatics/btac776
