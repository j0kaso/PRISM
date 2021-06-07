"""prism_rosetta_parser.py contains functions to convert prism to mut & ddG to prism

Author: Johanna K.S. Tiemann
Date of last major changes: 2020-05-01

"""

# Standard library imports
from datetime import datetime
import logging as logger
import re
import subprocess
import sys
import time


# Third party imports
import pandas as pd


# Local application imports
import rosetta_paths
sys.path.insert(1, rosetta_paths.prism_parser)
from PrismData import PrismParser, VariantData


def rosetta_to_prism(ddg_file, prism_file, sequence, rosetta_info=None, version=1, sys_name='', first_residue_number=1, sha_tag='', MP=False):
    
    sequence = sequence.replace('-', 'X')
    # create prism file with rosetta values
    logger.info('Create prism file with rosetta ddG values')
    variant = []
    norm_ddG_value = []
    std_ddG_value = []
    ddG_value = []
    with open(ddg_file, 'r') as fp:
        for line in fp:
            split_line = line.split(',')
            variant.append(split_line[0])
            norm_ddG_value.append(split_line[1])
            std_ddG_value.append(split_line[2].strip())
     #       ddG_value.append(split_line[1])

    data = {
        'variant': pd.Series(variant),
        'mean_ddG': pd.Series(norm_ddG_value),
        'std_ddG': pd.Series(std_ddG_value),
        #      'ddG': pd.Series(ddG_value),
        'n_mut': 1,  # pd.Series([1 for x in range(len(variant))]),
        'aa_ref': [[seg[0]] for seg in variant],
        "resi": [[seg[1:-1]] for seg in variant],
        "aa_var": [[seg[-1]] for seg in variant],
    }
    dataframeset = pd.DataFrame(data)

    sha = sha_tag.split('tag')[0]
    tag = sha_tag.split('tag')[1]

    if rosetta_info == None:
        rosetta_info = {
            "version": f"{tag} ({sha})",
        }

    if MP:
        units = ') REU'
    else:
        units = '/2.9) kcal/mol'

    metadata = {
        # new version always when the data is edited or major changes are made
        # to metadata
        "version": version,
        # extracted from uniprot
        "protein": {
            "name": sys_name,
            "organism": "",
            "uniprot": "",
            "sequence": sequence,
        },
        "rosetta": rosetta_info,
        # columns is dependent on the data. different conditions go into
        # different PRISM_files
        "columns": {
            "mean_ddG": f"mean Rosetta ddG values (mean((MUT-mean(WT)){units})",
            "std_ddG": f"std Rosetta ddG values (std((MUT-mean(WT)){units})",
        },
    }
    if first_residue_number != 1:
        metadata['protein']['first_residue_number'] = first_residue_number

    comment = [
        f"version {version} - {datetime.date(datetime.now())} - ddG pipeline",
    ]

    variant_dataset = VariantData(metadata, dataframeset)
    parser = PrismParser()
    parser.write(prism_file, variant_dataset, comment_lines=comment)


def write_prism(metadata, dataframe, prism_file, comment=''):
    variant_dataset = VariantData(metadata, dataframe)
    parser = PrismParser()
    parser.write(prism_file, variant_dataset, comment_lines=comment)


def read_prism(prism_file):
    parser = PrismParser()
    data = parser.read(prism_file)
    return data
