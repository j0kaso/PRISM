[![Changelog](https://img.shields.io/badge/changelog--lightgrey.svg?style=flat)](CHANGELOG)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KULL-Centre/PRISM/master?filepath=software%2Fdomain_protein_features%2Fjupyter_scripts%2Fextract_domain_protein_features_interactive.ipynb)


The domain protein features script extracts the domains, protein features (incl. topology, TM and disordered regions, disulfid bridges, active and binding sites) and pdb-ids for a uniprot id.



Features
--------

* extract domains for single uniprot-ids
* calculation for whole genome 
* additional information (nested domains, pdbs for domain family,)
* executable as python scripts (command line), inclusion in scripts and interactive (jupyter)


Table of contents
=================

* [Documentation](#documentation)
* [Cite](#cite)


Documentation
============

Detailed information concerning the installation, usage and results.


Installation
============

No installation necessary but needs a stable internet connection.

The scripts depends on Pandas. Please ensure that this is installed correctly and functional.


Running
=======

The script can be called either through the command line, by another script or by the jupyter notebook.

jupyter notebook
------------------

Optional. The notebook contains the single calls of the functions and also the final call. Please consider that the call to run through the complete human proteome is time consuming (several hours).

command line
-------------
```
usage: run.py [-h] [--human_proteome HUMAN_PROTEOME] [--uniprot_id UNIPROT_ID] [--reviewed REVIEWED] [--domainfamily_pdbs DOMAINFAMILY_PDBS] [--nested NESTED] [--output_dir OUTPUT_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --human_proteome HUMAN_PROTEOME, -hp HUMAN_PROTEOME
                        Calculate domains and features for the human proteome
  --uniprot_id UNIPROT_ID, -u UNIPROT_ID
                        Uniprot id for single runs (default: '')
  --reviewed REVIEWED, -r REVIEWED
                        Obtain only reviewed entries from uniprot (options: *, yes [default]
  --domainfamily_pdbs DOMAINFAMILY_PDBS, -dfp DOMAINFAMILY_PDBS
                        Get also all pdbs associated with each single domain family.
  --nested NESTED, -n NESTED
                        Get information about nested domains.
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        Directory where files will be specified, no output files will be printed

```

Result 
=======

The output can be saved (and loaded) as .json file or txt file.


general scheme:
```
({pfam_domain_id: 
	[[pfam_domain_name, start, end],
		[[extra information with position or start/end postition]],
		[[list of pdb_ids associated to the uniprot and domain
 		[pdb_id, chain, pdb_start, pdb_end, uniprot_start, uniprot_end]],
	 [if specified, list of additional pdb_ids mapped to the domain family]]],
 [[information which is not covered by the domain ranges, including definition and start and ending]])
```

example for uniprot_id = 'P10912'
```
({'PF00041': [['fn3', 159, 244],
   [['Extracellular', 19, 264]],
   [[['3HHR', 'C', 141, 226, 159, 244],
     ['1KF9', 'C', 641, 726, 159, 244],
     	...
     ['1KF9', 'F', 1641, 1726, 159, 244],
     ['1HWG', 'C', 141, 226, 159, 244]],
    [['6TPV', 'A', 321, 401, '', ''],
     	...
     ['5DWU', 'B', 341, 419, '', '']]]],
  'PF09067': [['EpoR_lig-bind', 43, 144],
   [['Extracellular', 19, 264],
    ['disulfid', 56, 66],
    ['disulfid', 101, 112],
    ['disulfid', 126, 140]],
   [[['3HHR', 'C', 32, 126, 50, 144],
   		...
     ['1HWG', 'C', 32, 126, 50, 144]],
    [['3N06', 'B', 2, 96, '', ''],
     ['1F6F', 'B', 5, 96, '', ''],
     	...
     ['4I18', 'C', 3, 96, '', '']]]],
  'PF12772': [['GHBP', 316, 617],
   [['Cytoplasmic', 289, 638], ['disorder:D', 269, 620]],
   [[], []]]},
 [['tm:Helical', 265, 288]])
```


Cite
====

When using, please cite:

* The UniProt Consortium. UniProt: a worldwide hub of protein knowledge. Nucleic Acids Res. 47: D506-515 (2019)
* S. El-Gebali, J. Mistry, A. Bateman, S.R. Eddy, A. Luciani, S.C. Potter, M. Qureshi, L.J. Richardson, G.A. Salazar, A. Smart, E.L.L. Sonnhammer, L. Hirsh, L. Paladin, D. Piovesan, S.C.E. Tosatto, R.D. Finn. The Pfam protein families database in 2019. Nucleic Acids Research (2019) doi: 10.1093/nar/gky995
* Hatos A et al. DisProt: intrinsic protein disorder annotation in 2020. Nucleic Acids Res., 2019.
* Piovesan D, Tabaro F, Paladin L, Necci M, Mičetić I, Camilloni C, Davey N, Dosztányi Z, Meszaros B, Monzon AM, Parisi G, Schad E, Sormanni P, Tompa P, Vendruscolo M, Vranken WF and Tosatto SCE. MobiDB3.0: More annotations for intrinsic disorder, conformational diversity and interactions in proteins. Nucleic Acid Research. 2018. 46(D1):D471-D476
