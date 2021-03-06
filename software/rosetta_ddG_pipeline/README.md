# Rosetta stability pipeline

Rosetta stability pipeline is part of the PRISM reseach project. This pipeline aims to calculate ddG value from structure, by systematically mutating individual residues.

## Description
The stability pipeline uses as input a structure file (in PDB format), performs a relaxation, followed by a ∆∆G calculation by extracting the energy change upon (single point) mutation (∆∆Gmut - ∆∆Gwt). Therefore, the Rosetta software is used. The pipeline for soluble proteins follows the classical cartesian protocol by 
Hahnbeom Park, Philip Bradley, Per Greisen Jr., Yuan Liu, Vikram Khipple Mulligan, David E Kim, David Baker, and Frank DiMaio (2016) "Simultaneous optimization of biomolecular energy function on features from small molecules and macromolecules", JCTC.
The protocol for ∆∆G calculations of membrane proteins has not been published: it uses the frankling2019 scorefunction and follows the ∆∆G protocol of Park et al. except for performing the calculations in atom-tree space (compared to cartesian space in the soluble protein pipeline).


## Requirements 

The following python3 packages are required to run the pipeline:
    - pandas
    - numpy
    - biopython
    - scipy

Required software:
    - Rosetta
    - PyRosetta (via conda install)
    - Muscle (for alignment)

## Installation

To install the pipeline, get it from the GitHub page.

An installation file is not yet available.


The following links should be in your bashrc:
```bash
export Rosetta_main_path= ‘{Newest Rosetta version}’
export Rosetta_tools_path='{path to Rosetta tools}’
export Rosetta_database_path='{path to Rosetta database}’
export Rosetta_extension='linuxgccrelease'
export ddG_pipeline='{path to this pipeline}’
export muscle_exec='{path to muscle}’
export prism_parser='{path to prism parser}'
alias run_ddG_pipeline=’{path to run_pipeline.py}’
```


## Usage

The pipeline is invoked using:
```bash
run_ddG_pipeline -s {structure} (and any additional flags)
```

Run modes:
```bash
Run modes directs the actions of the pipeline
    print: prints default flag files 
    create: Creates all run files
    proceed: Starts calculations with created run files (incl. relax and ddG calculation) 
    relax: Starts relax calculations with created run files 
    ddg_calculation: Starts ddg_calculation calculations with created run files
    fullrun: runs full pipeline                              
'Default value: create'
```

For most cases create or fullrun should be used


General flags
```bash
    Flags:
    -s path to pdb file
    -o path to output directory
    -i run modes
    -mm mutation mode: do saturation mutagenesis [all] or use input mutfile 
    -m path to mutation input file: can be a rosetta_mutfile, mutfile_dir or similar (generated by prism2mutfile.py in ../scripts)
    --chainid which chain to run (default A)
    --run_struc which additional chains to keep in the structure to run (But not to calculate ddGs on)
    --ligand True/False whether to keep ligand 
    --overwrite_path True/False overwrites files and folders in output directory. needed for proceed mode
    --slurm_partition
    --verbose increase verbose level
    --gapped_output output pism and pdb file with shifted residue numbering according to input
    --dump_pdb dumps all mutant pdbs
```

Flags for membrane proteins:
```bash
    Flags:
    --mp needs to be set to true if running membrane protein pipeline
    --mp_span path to span file - if not present, choose calculation method in mp_calc_span_mode
    --mp_calc_span_mode span file calculation method, prefered DSSP
    --mp_prep_align_mode transfer protein into membrane plane, prefered OPM
    --mp_align_ref reference PDBid and chain for alignment, e.g. 3sn6_R
```


Flags for modifying the protocol/pipeline (mostly development, partly not visible with the --help option)
```bash
    Flags:
    --ddgflags path to ddgflg file
    --relaxflags path to relaxflag file
    --mp_relax_xml path to relaxxml file for membrane protein pipeline
    --uniprot not implemented

    --mp_thickness
    --mp_lipids
    --mp_temperature
    --mp_pH
    --benchmark_mp_repack
    --benchmark_mp_repeat
    --benchmark_mp_relax_repeat
    --benchmark_mp_relax_strucs
    --mp_ignore_relax_mp_flags
    --mp_energy_func
    --mp_repack_protocol
    --mp_multistruc_protocol
```


### Usage examples
#### Case 1 - Creating files for inspection
To run the pipeline without queing the jobs use the flag -i create

```bash
run_ddG_pipeline -s 1PGA.pdb -o run -i create --chainid A
```

To run from the same folder again, use --overwrite_path True 

```bash
run_ddG_pipeline -s 1PGA.pdb -o run -i fullrun --chainid A --overwrite_path True
```

#### Case 2 - Run on a single chain
To run saturation on a specific chain run:
```bash
run_ddG_pipeline -s 1PGA.pdb -o run -i fullrun --chainid A
```
This will create a folder "Run" relative to your current directory and run saturation mutagenesis on chain A using the structure 1PGA.pdb


#### Case 3 - Running specific variants
To run specific variants the variants need to specified in a mutation_input.txt

The format for the mutation_input.txt is Wildtype RosettaPositionNumber Variants:
```bash
G 10 DEA
H 11 TW
A 12 ACDEFGHIKLMNPQRSTVWY
```

Be aware that we are talking Rosetta numbering! This means numbering starts at 1 and there are no gaps

You can now do the run:
```bash
run_ddG_pipeline -s 1PGA.pdb -o run -i fullrun --chainid A -m mutation_input.txt
```

Alternatively, mutfile following the Rosetta scheme can be used. Also, prism files can be transfered into mutfiles following the ../script/prism2mutfile.py script. This script takes also a pdb file and renumbers it to rosetta numbering automatically.

#### Case 4 - Running chain in context of additional structure
To run for example chain A, while keeping chain B in structure the following flag can be used. To be safe also use the chainid flag and make sure run_struc contain all chains.

```bash
run_ddG_pipeline -s 1PGA.pdb -o run -i fullrun --chainid A --run_struc AB
```

#### Case 5 - Running a membrane protein
To run a protein through the membrane protein pipeline, -mp must be specified and a prepared protein provided. If the protein is not yet aligned, add --mp_align_ref which switches --mp_prep_align_mode to OPM. If no span file is provided, specify --mp_calc_span_mode with DSSP to calculate it:

```bash
run_ddG_pipeline -s 6xro.pdb -o run -i fullrun --chainid A -mp 1 --mp_calc_span_mode DSSP --mp_align_ref 6xro_A 
```




## Support
For general support:
    Anders Frederiksen - anders.frederiksen@bio.ku.dk
    
For support about membrane protein runs:
    Johanna Tiemann - johanna.tiemann@gmail.com

## Roadmap
TBD

## Contributing
Contributing to the project is not currently possible, but we are very open to suggestions

## Acknowledgements 

TBD


## License
TBD