import os
import subprocess
import time

# yes, I know global vars are bad...
default_path = {
    'muscle_exec': '/groups/sbinlab/software/muscle/muscle3.8.31_i86linux64',
    'TMalign_exec': '/groups/sbinlab/software/TMalign/TMalign',
    'ddG_pipeline': '/groups/sbinlab/software/PRISM_tools/rosetta_stability-v0.1/software/rosetta_ddG_pipeline',
    'Rosetta_main_path': '/sbinlab/software/Rosetta_2020_July_dc83fa/source/',
    'Rosetta_tools_path': '/sbinlab/software/Rosetta_tools/tools/',
    'Rosetta_database_path': '/sbinlab/software/Rosetta_2020_July_dc83fa/database/',
    'Rosetta_extension': 'linuxgccrelease',
    'prism_parser': '/groups/sbinlab/software/PRISM_tools/prism_parser/scripts',
}


def load_env(env):
    # load exec if within environment
    if os.getenv(env) != None:
        return os.getenv(env)
    else:
        os.environ[env] = default_path[env]
    return default_path[env]


muscle_exec = load_env('muscle_exec')
TMalign_exec = load_env('TMalign_exec')
ddG_pipeline = load_env('ddG_pipeline')
Rosetta_main_path = load_env('Rosetta_main_path')
Rosetta_tools_path = load_env('Rosetta_tools_path')
Rosetta_database_path = load_env('Rosetta_database_path')
Rosetta_extension = load_env('Rosetta_extension')
prism_parser = load_env('prism_parser')

try:
    pipes2 = subprocess.Popen("git describe --tags", shell=True, cwd=ddG_pipeline, stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    std_out2, std_err = pipes2.communicate()
    pipes = subprocess.Popen("git log -n 1 | grep -i commit", shell=True, cwd=ddG_pipeline, stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    std_out, std_err = pipes.communicate()
    time.sleep(3)
    sha = std_out.strip().decode('UTF-8').split()[1]
    tag = std_out2.strip().decode('UTF-8').split()[0]
except:
    sha = 'v0.1'
    tag = '09edce8ae74dceca2a79d20b2e8d0bbb5c0813e3'


print('current env paths & exec:', TMalign_exec, muscle_exec, ddG_pipeline, Rosetta_main_path,
      Rosetta_tools_path, Rosetta_database_path, Rosetta_extension, prism_parser, sha, tag)

# Rosetta paths
path_to_rosetta = Rosetta_main_path
path_to_clean_pdb = os.path.join(
    Rosetta_tools_path, 'protein_tools', 'scripts', 'clean_pdb.py')
path_to_clean_keep_ligand = os.path.join(
    path_to_rosetta, 'src', 'apps', 'public', 'relax_w_allatom_cst', 'clean_pdb_keep_ligand.py')
# Personal paths
path_to_stability_pipeline = ddG_pipeline
default_output_path = os.path.join(path_to_stability_pipeline, 'output')
path_to_data = os.path.join(
    path_to_stability_pipeline, 'data')

# Muscle exec
path_to_muscle = muscle_exec

# TMalign exec
path_to_TMalign = TMalign_exec
