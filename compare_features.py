import format_data 
import train_model
import pickle
import pandas as pd
import numpy as np
import argparse

def parse_args():
    """ 
    Parse args provided by the user 
    
    :return: parsed arguments 
    """
    
    parser = argparse.ArgumentParser(description='Train LSTM on PHROG orders')
    parser.add_argument('-features', '--features', help = 'Number of features to include')
    parser.add_argument('-t','--training_data', help='Training data', required=True)
    parser.add_argument('-f', '--flip_genomes', help='Flip genomes to ensure that an integrase is at the start of each sequence', required = True) 
    parser.add_argument('-num_genes', '--num_genes', help = 'Maximum number of genes considered in a training instance. Genomes with a number of genes above this will not be included', default = 120, type = int)  
    parser.add_argument('-m', '--memory_cells', help = 'Number of memory cells to use', type = int, default = 20) 
    parser.add_argument('-b', '--batch_size', help = 'Batch size', type = int, default = 128) 
    parser.add_argument('-phrogs', '--phrog_annotations', help = 'csv file containing the annotation and category of each phrog', required = True) 
    parser.add_argument('-e', '--epochs', help = 'Number of epochs', type = int, default = 120) 
    parser.add_argument('-dropout', '--dropout', help = 'Dropout for LSTM', type = float, default = 0.2) 
    parser.add_argument('-recurrent', '--recurrent_dropout', help = 'Recurrent dropout for LSTM', type = float, default = 0) 
    parser.add_argument('-lr', '--learning_rate', help = 'Learning rate for the Adam optimizer', type = float, default = 0.001) 
    parser.add_argument('-p', '--patience', help = 'Early stopping condition patience', type = int, default = 3) 
    parser.add_argument('-early', '--early_stopping', help = 'Whether to include an early stopping condition in the model', type = bool, default = True)
    parser.add_argument('-d', '--min_delta', help = 'Early stopping condition min delta', type = float, default = 1e-5)
    parser.add_argument('-out', '--out_file_prefix', help = 'Prefix used for the output files', required = True)
    parser.add_argument('-portion', '--training_portion', help = 'Portion of the data to use to train the model', type = float, default = 0.5) 
    
    return vars(parser.parse_args())

def main(): 
    
    #get arguments 
    args = parse_args() 
    
    #need to read in training genomes - manipulate such that we are reading in just some consistent set of training data 
    print('opening required files', flush = True) 
    file = open(args['training_data'],'rb')
    training_data = pickle.load(file)
    file.close()

    #generate dictionary 
    training_keys = list(training_data.keys())
    annot = pd.read_csv(args['phrog_annotations'], sep = '\t')
    cat_dict = dict(zip([str(i) for i in annot['phrog']], annot['category']))
    cat_dict[None] = 'unknown function'

    #hard-codedn dictionary matching the PHROG cateogories to an integer value 
    one_letter = {'DNA, RNA and nucleotide metabolism' : 4,
         'connector' : 2,
         'head and packaging' : 3,
         'integration and excision': 1,
         'lysis' : 5,
         'moron, auxiliary metabolic gene and host takeover' : 6,
         'other' : 7,
         'tail' : 8,
         'transcription regulation' : 9,
         'unknown function' :  0}

    #use this dictionary to generate an encoding of each phrog
    phrog_encoding = dict(zip([str(i) for i in annot['phrog']], [one_letter.get(c) for c in annot['category']]))

    #add a None object to this dictionary which is consist with the unknown 
    phrog_encoding[None] = one_letter.get('unknown function') 

    print('filtering data', flush = True) 
    #flip the genome if there is an integrase at the end of the sequence 
    if args['flip_genomes'] == True: 
        training_data = format_data.flip_genomes(training_data, phrog_encoding)

    #derepicate training data 
    training_data_derep = format_data.derep_trainingdata(training_data, phrog_encoding)
    
    #filter training data to remove prophages with too many genes 
    training_data_derep_numgenes = format_data.filter_genes(training_data_derep, args['num_genes']) 
    training_keys_derep_numgenes = list(training_data_derep_numgenes.keys())

    #shuffle the data 
    data_shuffled = format_data.shuffle_dict(training_data_derep_numgenes)
    keys_shuffled = list(data_shuffled.keys())  

    #generate features 
    print('generating features', flush = True) 
    training_encodings, features = format_data.format_data(data_shuffled, phrog_encoding) 
    num_functions = len(one_letter)
    max_length = args['num_genes']
    n_features = num_functions + len(features[0])

    #generate test and training datasets
    train_num = int(args['portion']*len(training_encodings)) 

    #generate features 
    if args['features'] == 'all': 
        X_train, y_train, masked_idx = format_data.generate_dataset(training_encodings[:train_num], features[:train_num], num_functions, n_features, max_length) 
        X_test, y_test, masked_idx = format_data.generate_dataset(training_encodings[train_num:], features[train_num:], num_functions, n_features, max_length) 
        
    elif args['features'] == 'strand': 
        X_train, y_train, masked_idx = format_data.generate_dataset(training_encodings[:train_num], [f[:2] for f in features[:train_num]], num_functions, n_features, max_length) 
        X_test, y_test, masked_idx = format_data.generate_dataset(training_encodings[train_num:], [f[:2] for f in features[train_num:]], num_functions, n_features, max_length) 
        n_features = num_functions + 2
        
    elif args['features'] == 'none': 
        X_train, y_train, masked_idx = format_data.generate_dataset(training_encodings[:train_num], [[] for i in range(train_num)], num_functions, n_features, max_length) 
        X_test, y_test, masked_idx = format_data.generate_dataset(training_encodings[train_num:],[[] for i in range(len(training_encodings) - train_num)] , num_functions, n_features, max_length) 
        n_features = num_functions
        
    else: 
        print('ERROR') 

    model_file = 'all_features' + '_trained_LSTM.h5' 
    history_file = 'all_features' + '_history.pkl' 

    train_model.train_model(X_train,
                            y_train,
                            X_test, 
                            y_test, 
                            max_length, 
                            n_features, 
                            num_functions, 
                            model_file, 
                            history_file, 
                            args['memory_cells'], 
                            args['batch_size'], 
                            args['epochs'], 
                            args['dropout'], 
                            args['recurrent_dropout'],
                            args['learning_rate'],
                            args['early_stopping'],
                            args['patience'], 
                            args['min_delta'])

    #Save the ids of the data in the test dataset 
    test_id_filename = args['out_file_prefix'] + '_test_prophage_ids.txt' 
    with open(test_id_filename, 'w') as f:
        for line in test_ids:
            f.write(f"{line}\n")
            
if __name__ == "__main__":
    main()