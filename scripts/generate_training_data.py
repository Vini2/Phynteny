import pickle
import click
from phynteny_utils import handle_genbank
from phynteny_utils import format_data
import pkg_resources

@click.command()
@click.option(
    "-i",
    "--input_data",
    help="Text file containing genbank files to build model",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "-g",
    "--maximum_genes",
    type=int,
    help="Specify the maximum number of genes in each genome",
    default=120,
)
@click.option(
    "-c",
    "--gene_categories",
    type=int,
    help="Specify the minimum number of cateogries in each genome",
    default=4,
)
@click.option(
    "--prefix",
    "-p",
    default='data',
    type=str,
    help="Prefix for the output files",
)


def main(input_data, maximum_genes, gene_categories, prefix):

    print("STARTING")

    # read in annotations
    phrog_integer = pkg_resources.resource_filename('phynteny_utils', 'phrog_annotation_info/phrog_integer.pkl')
    phrog_integer["No_PHROG"] = 0
    num_functions = len(
            list(set(phrog_integer.values()))
        )

    # takes a text file where each line is the file path to genbank files of phages to train a model
    print("getting input", flush=True)
    print(input, flush=True)
    data = handle_genbank.get_data(input_data, gene_categories, phrog_integer, maximum_genes)  # dictionary to store all of the training data

    # save the training data dictionary
    print("Done Processing!\n")
    print("Removing duplicate phrog category orders")
    
    # dereplicate the data and shuffle 
    derep_dict= handle_genbank.derep_trainingdata(data)
    
    # save the original data
    with open(prefix + "_all_data.pkl", "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close() 

    # save the de-replicated data
    with open(prefix + "_dereplicated.pkl", "wb") as handle:
        pickle.dump(derep_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

    # save the testing and training datasets
    format_data.test_train(data, prefix, num_functions, maximum_genes)

if __name__ == "__main__":
    main()
