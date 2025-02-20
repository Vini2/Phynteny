from pycirclize import Circos
from pycirclize.parser import Gff
from pycirclize.parser import Genbank
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import os
import numpy as np
import sys


# Load GFF file

def create_plot( gff_file,gbk_file,  interval, annotations, title_size, plot_title, truncate, outfile, dpi, label_size, label_hypotheticals, remove_other_features_labels):

    gff = Gff(gff_file)

    # get only to range of gff - as by default gbk takes all contigs, gff only the first
    gbk = Genbank(gbk_file)

    # instantiate circos
    circos = Circos(sectors={gbk.name: gbk.range_size})

    # title if not blank
    circos.text(plot_title, size=int(title_size), r=190)

    sector = circos.get_sector(gbk.name)
    cds_track = sector.add_track((70, 80))
    cds_track.axis(fc="#EEEEEE", ec="none")

#### plot each PHROG fwd and reverse
## colours

## update colours



#4deeea              
#74ee15
#ffe700
#f000ff
#001eff
#8900ff
#ff008d
#1c1c1c
#ffffff    


# unknown 

    unk_col = "#AAAAAA"

    unk_fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):

        if f.qualifiers.get("function")[0] == 'unknown function' and f.qualifiers.get("phynteny")[0] == 'unknown function':

            unk_fwd_list.append(f)

    cds_track.genomic_features(
        unk_fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=unk_col,
    )

    unk_rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):

        if f.qualifiers.get("function")[0] == 'unknown function':

            unk_rev_list.append(f)

    cds_track.genomic_features(
        unk_rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=unk_col,
    )

# other

    other_col = "#a6761d"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'other':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=other_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'other':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=other_col,
    )

    # phynteny predictions


    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'other' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=other_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'other' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=other_col,
    )

# tail 

    tail_col = "#e6ab02"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'tail':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=tail_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'tail':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=tail_col,
    )

    # phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'tail' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=tail_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'tail' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=tail_col,
    )

# transcription regulation

    transcription_col = "#80b1d3"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'transcription regulation':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=transcription_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'transcription regulation':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=transcription_col,
    )

    # phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'transcription regulation' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=transcription_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'transcription regulation' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=transcription_col,
    )

# DNA, RNA and nucleotide metabolism

    dna_col = "#e7298a"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'DNA':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=dna_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'DNA':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=dna_col,
    )

    # phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'DNA' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=dna_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'DNA' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=dna_col,
    )

#lysis

    lysis_col = "#66a61e"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'lysis':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=lysis_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'lysis':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=lysis_col,
    )

    # phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'lysis' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=lysis_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'lysis' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=lysis_col,
    )

# moron, auxiliary metabolic gene and host takeover

    moron_col = "#cab2d6"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'moron':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=moron_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'moron':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=moron_col,
    )

    # phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'moron' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=moron_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'moron' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=moron_col,
    )

    # integration and excision

    int_col = "#1b9e77"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'integration and excision':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=int_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'integration and excision':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=int_col,
    )

    # phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'integration and excision' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=int_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'integration and excision' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=int_col,
    )

# head and packaging

    head_col = "#7570b3"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'head and packaging':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=head_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'head and packaging':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=head_col,
    )

    #phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'head and packaging' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=head_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'head and packaging' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=head_col,
    )

# connector

    con_col = "#d95f02"

    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("function")[0] == 'connector':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=con_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("function")[0] == 'connector':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=con_col,
    )

    # phynteny predictions
    fwd_list = []
    for f in gff.extract_features("CDS", target_strand=1):
        if f.qualifiers.get("phynteny")[0] == 'connector' and f.qualifiers.get("function")[0] == 'unknown function':
            fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=con_col,
    )

    rev_list = []
    for f in gff.extract_features("CDS", target_strand=-1):
        if f.qualifiers.get("phynteny")[0] == 'connector' and f.qualifiers.get("function")[0] == 'unknown function':
            rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=con_col,
    )

###################################################
#### Extra Features
###################################################

# only if flag isn't set


    extras_col = 'black'

    fwd_list = []
    for f in gff.extract_features("tRNA", target_strand=1):
        fwd_list.append(f)
    for f in gff.extract_features("tmRNA", target_strand=1):
        fwd_list.append(f)
    for f in gff.extract_features("repeat_region", target_strand=1):
        fwd_list.append(f)

    cds_track.genomic_features(
        fwd_list,
        plotstyle="arrow",
        r_lim=(75, 80),
        fc=extras_col,
    )

    rev_list = []
    for f in gff.extract_features("tRNA", target_strand=-1):
        rev_list.append(f)
    for f in gff.extract_features("tmRNA", target_strand=-1):
        rev_list.append(f)
    for f in gff.extract_features("repeat_region", target_strand=-1):
        rev_list.append(f)

    cds_track.genomic_features(
        rev_list,
        plotstyle="arrow",
        r_lim=(70, 75),
        fc=extras_col,
    )


##################################
####### thin out extra features #########
##################################

    if remove_other_features_labels == False:

        # trna
        pos_list_trna, labels_trna, length_list_trna = [], [], []
        for f in gff.extract_features("tRNA"):
            start, end = int(str(f.location.end)), int(str(f.location.start))
            pos = (start + end) / 2.
            length = end - start
            label = 'tRNA'
            pos_list_trna.append(pos)
            labels_trna.append(label)
            length_list_trna.append(length)

    # if trnas exist
        if len(length_list_trna) > 0:
            # thin out the trnas to avoid overlaps
            # Create an empty list to store the filtered indices
            filtered_indices_trna = []
            # add the first tRNA
            filtered_indices_trna.append(0)
            
            for i in range(1,len(length_list_trna)):
                # If the position of the trna is at least 500bp away from the previous, add it
                if pos_list_trna[i] > (pos_list_trna[i-1] + 500):
                    filtered_indices_trna.append(i)

            # Use the filtered indices to create new lists for pos_list, labels, and length_list
            pos_list_trna = [pos_list_trna[i] for i in filtered_indices_trna]
            labels_trna = [labels_trna[i] for i in filtered_indices_trna]
            length_list_trna = [length_list_trna[i] for i in filtered_indices_trna]


        # tmrna
        pos_list_tmrna, labels_tmrna, length_list_tmrna = [], [], []
        for f in gff.extract_features("tmRNA"):
            start, end = int(str(f.location.end)), int(str(f.location.start))
            pos = (start + end) / 2.
            length = end - start
            label = 'tmRNA'
            pos_list_tmrna.append(pos)
            labels_tmrna.append(label)
            length_list_tmrna.append(length)

        if len(length_list_tmrna) > 0:
            # thin out the trnas to avoid overlaps
            # Create an empty list to store the filtered indices
            filtered_indices_tmrna = []
            # add the first tmRNA
            filtered_indices_tmrna.append(0)

            for i in range(1,len(length_list_tmrna)):
                # If the position of the tmRNA is at least 500bp away from the previous, add it
                if pos_list_tmrna[i] > (pos_list_tmrna[i-1] + 500):
                    filtered_indices_tmrna.append(i)

            # Use the filtered indices to create new lists for pos_list, labels, and length_list
            pos_list_tmrna = [pos_list_tmrna[i] for i in filtered_indices_tmrna]
            labels_tmrna = [labels_tmrna[i] for i in filtered_indices_tmrna]
            length_list_tmrna = [length_list_tmrna[i] for i in filtered_indices_tmrna]

        
        # crispr
        pos_list_crispr, labels_crispr, length_list_crispr = [], [], []
        for f in gff.extract_features("repeat_region"):
            start, end = int(str(f.location.end)), int(str(f.location.start))
            pos = (start + end) / 2.
            length = end - start
            label = 'CRISPR'
            pos_list_crispr.append(pos)
            labels_crispr.append(label)
            length_list_crispr.append(length)

        if len(length_list_crispr) > 0:

            # thin out the crisprs to avoid overlaps
            # Create an empty list to store the filtered indices
            filtered_indices_crispr = []
            # add the first crispr
            filtered_indices_crispr.append(0)

            for i in range(1,len(length_list_tmrna)):
                # If the position of the crispr is at least 500bp away from the previous, add it
                if pos_list_crispr[i] > (pos_list_crispr[i-1] + 500):
                    filtered_indices_crispr.append(i)

            # Use the filtered indices to create new lists for pos_list, labels, and length_list
            pos_list_crispr = [pos_list_crispr[i] for i in filtered_indices_crispr]
            labels_crispr = [labels_crispr[i] for i in filtered_indices_crispr]
            length_list_crispr = [length_list_crispr[i] for i in filtered_indices_crispr]


##################################
####### truncate CDS labels
##################################

    # truncation 
    truncate = int(truncate)

    # Extract CDS product labels
    pos_list, labels, length_list = [], [], []
    for f in gff.extract_features("CDS"):
        start, end = int(str(f.location.end)), int(str(f.location.start))
        pos = (start + end) / 2.
        length = end - start
        label = f.qualifiers.get("product", [""])[0]
        # skip hypotheticals if the flag is false (default)
        if label_hypotheticals == False:
            if label == "" or label.startswith("hypothetical") or label.startswith("unknown") :
                continue
        if len(label) > truncate:
            label = label[:truncate] + "..."
        pos_list.append(pos)
        labels.append(label)
        length_list.append(length)

###################################################
#### thin out CDS annotations
###################################################
    annotations = float(annotations)

    if annotations == 0:
        print("by inputting --annotations 0 you have chosen to plot no annotations. Continuing.")
    elif annotations == 0:
        print("by inputting --annotations 1 you have chosen to plot all annotations. Continuing.")
    elif annotations > 1:
        print("You have input a --annotations value greater than 1. Setting to 1 (will plot all annotations). Continuing.")
        annotations = 1
    elif annotations < 0: 
        print("You have input a --annotations value less than 1. Setting to 0 (will plot no annotations). Continuing.")
        annotations = 0

    ####### running the sparsity

    median_length = np.quantile(length_list, annotations)
    # Create an empty list to store the filtered indices
    filtered_indices = []

    # Loop through the indices of the length_list
    for i in range(len(length_list)):
        # If the length at this index is greater than or equal to the median, add the index to filtered_indices
        if length_list[i] < median_length:
            filtered_indices.append(i)

    # Use the filtered indices to create new lists for pos_list, labels, and length_list
    pos_list = [pos_list[i] for i in filtered_indices]
    labels = [labels[i] for i in filtered_indices]
    length_list = [length_list[i] for i in filtered_indices]

    # Plot CDS product labels on outer position
    cds_track.xticks(
        pos_list,
        labels,
        label_orientation="vertical",
        show_bottom_line=True,
        label_size=label_size,
        line_kws=dict(ec="grey"),
    )

###################################################
# set other features 
###################################################
    if remove_other_features_labels == False:
        # add trnas
        cds_track.xticks(
            pos_list_trna,
            labels_trna,
            label_orientation="vertical",
            show_bottom_line=True,
            label_size=label_size,
            line_kws=dict(ec="grey"),
        )
        # add tmrnas
        cds_track.xticks(
            pos_list_tmrna,
            labels_tmrna,
            label_orientation="vertical",
            show_bottom_line=True,
            label_size=label_size,
            line_kws=dict(ec="grey"),
        )
        # add crisprs
        cds_track.xticks(
            pos_list_crispr,
            labels_crispr,
            label_orientation="vertical",
            show_bottom_line=True,
            label_size=label_size,
            line_kws=dict(ec="grey"),
        )

###################################################
# set gc content and skew coordinates
###################################################
    gc_content_start = 42.5
    gc_content_end = 60
    gc_skew_start = 25 
    gc_skew_end = 42.5

    # Plot GC content
    gc_content_track = sector.add_track((gc_content_start, gc_content_end))

    pos_list, gc_contents = gbk.calc_gc_content()
    gc_contents = gc_contents - gbk.calc_genome_gc_content()
    positive_gc_contents = np.where(gc_contents > 0, gc_contents, 0)
    negative_gc_contents = np.where(gc_contents < 0, gc_contents, 0)
    abs_max_gc_content = np.max(np.abs(gc_contents))
    vmin, vmax = -abs_max_gc_content, abs_max_gc_content
    gc_content_track.fill_between(
        pos_list, positive_gc_contents, 0, vmin=vmin, vmax=vmax, color="black"
    )
    gc_content_track.fill_between(
        pos_list, negative_gc_contents, 0, vmin=vmin, vmax=vmax, color="grey"
    )

    # Plot GC skew
    gc_skew_track = sector.add_track((gc_skew_start, gc_skew_end))

    pos_list, gc_skews = gbk.calc_gc_skew()
    positive_gc_skews = np.where(gc_skews > 0, gc_skews, 0)
    negative_gc_skews = np.where(gc_skews < 0, gc_skews, 0)
    abs_max_gc_skew = np.max(np.abs(gc_skews))
    vmin, vmax = -abs_max_gc_skew, abs_max_gc_skew
    gc_skew_track.fill_between(
        pos_list, positive_gc_skews, 0, vmin=vmin, vmax=vmax, color="green"
    )
    gc_skew_track.fill_between(
        pos_list, negative_gc_skews, 0, vmin=vmin, vmax=vmax, color="purple"
    )

    label_size = int(label_size)

    # Plot xticks & intervals on inner position
    cds_track.xticks_by_interval(
        interval=int(interval),
        outer=False,
        show_bottom_line=False,
        label_formatter=lambda v: f"{v/ 1000:.0f} Kb", # no decimal place
        label_orientation="vertical",
        line_kws=dict(ec="grey"),
        label_size=8
    )

    ################################
    # phrog legend
    ###############################

    # # Add legend
    handle_phrogs = [
        Patch(color=unk_col, label="Unknown/Other Function"),
        Patch(color=transcription_col, label="Transcription Regulation"),
        Patch(color=dna_col, label="DNA/RNA & nucleotide \n metabolism"),
        Patch(color=lysis_col, label="Lysis"),
        Patch(color=moron_col, label="Moron, auxiliary metabolic \n gene & host takeover"),
        Patch(color=int_col, label="Integration & excision"),
        Patch(color=head_col, label="Head & packaging"),
        Patch(color=con_col, label="Connector"),
        Patch(color=tail_col, label="Tail"),
    ]

    fig = circos.plotfig()

    phrog_legend_coords = (0.10, 1.175)
    phrog_legend = circos.ax.legend(
    handles=handle_phrogs,
    bbox_to_anchor=phrog_legend_coords,
    fontsize=9.5,
    loc="center",
    title="PHROG CDS",
    handlelength=2
    )
    
    circos.ax.add_artist(phrog_legend)

    ################################
    # gc and other features legend
    ###############################

    handle_gc_content = [
        Line2D([], [], color="black", label="Positive GC Content", marker="^", ms=6, ls="None"),
        Line2D([], [], color="grey", label="Negative GC Content", marker="v", ms=6, ls="None"),
    ]

    handle_gc_skew = [
        Line2D([], [], color="green", label="Positive GC Skew", marker="^", ms=6, ls="None"),
        Line2D([], [], color="purple", label="Negative GC Skew", marker="v", ms=6, ls="None")
    ]

    handle_other_features = [
        Patch(color=extras_col, label="tRNA/tmRNA/CRISPR")
    ]

    # shrink plot a bit (0.8)
    box = circos.ax.get_position()
    circos.ax.set_position([box.x0, box.y0, box.width * 0.65, box.height*0.9])

    # gc content and skew coordinates
    gc_content_anchor = (0.92, 1.30)
    gc_skew_anchor = (0.92, 1.20)

    gc_legend_cont = circos.ax.legend(
    handles=handle_gc_content,
    bbox_to_anchor=gc_content_anchor,
    loc="center",
    fontsize=9.5,
    title="GC Content",
    handlelength=2,
    )

    circos.ax.add_artist(gc_legend_cont)

    gc_legend_skew = circos.ax.legend(
    handles=handle_gc_skew,
    bbox_to_anchor=gc_skew_anchor,
    loc="center",
    fontsize=9.5,
    title="GC Skew",
    handlelength=2,
    )

    circos.ax.add_artist(gc_legend_skew)

    # other features 
    other_features_anchor = (0.92, 1.10)

    other_features_legend = circos.ax.legend(
    handles=handle_other_features,
    bbox_to_anchor=other_features_anchor,
    loc="center",
    fontsize=9.5,
    title="Other Features",
    handlelength=2,
    )

    circos.ax.add_artist(other_features_legend)

    dpi = int(dpi)
    
    fig.savefig(outfile, dpi=dpi)
