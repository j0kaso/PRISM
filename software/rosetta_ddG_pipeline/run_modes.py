"""run_modes.py contains helpful functions.

Author: Anders Frederiksen
Contribution: Johanna K.S. Tiemann

Date of last major changes: 2020-04-15

"""

# Standard library imports
import logging as logger
from os.path import join
import subprocess
from get_memory_stats import check_memory

def relaxation(folder):
    """Runs relax scripts and parsing of the relax results. Output parse_relax_process_id, that can be used to run ddg_calculation right after"""
    
    #Launching Rosetta_relax.sbatch
    relax_call = subprocess.Popen(f'sbatch {join(folder.relax_input,"rosetta_relax.sbatch")}', stdout=subprocess.PIPE, shell=True, cwd=folder.relax_run)

    #Gettin process ID
    relax_process_id_info = relax_call.communicate()
    relax_process_id = str(relax_process_id_info[0]).split()[3][0:-3]

    with open(join(folder.relax_run, f'job_id_relax.txt'), 'w') as job_id_file:     
        job_id_file.write(relax_process_id)
                                                                                                                               
    #Launching parse_relax.sbatch
    parse_relaxation_call = subprocess.Popen(f'sbatch --dependency=afterany:{relax_process_id} {join(folder.relax_input, "parse_relax.sbatch")}', stdout=subprocess.PIPE, shell=True, cwd=folder.relax_run)
                                                                                            
    #Gettin process ID                                          
    parse_relax_process_id_info = parse_relaxation_call.communicate()
    parse_relax_process_id = str(parse_relax_process_id_info[0]).split()[3][0:-3]

    return parse_relax_process_id


def ddg_calculation(folder, parse_relax_process_id=None, mp_multistruc=0):
    """Runs cartesian_ddg script and parsing of the ddg results"""                                         
                                             
    if parse_relax_process_id == None:
        dependency = ''
        parse_relax_process_id = ''
    else:
        dependency = '--dependency=afterany:'
    
    if  mp_multistruc==0:
        #Launching Rosetta_ddg.sbatch
        ddg_call = subprocess.Popen(f'sbatch {dependency}{parse_relax_process_id} {join(folder.ddG_input, "rosetta_ddg.sbatch")}', stdout=subprocess.PIPE, shell=True, cwd=folder.ddG_run)

        #Gettin process ID                                
        ddg_process_id_info = ddg_call.communicate()
        logger.info(f'ddG process ID info: {ddg_process_id_info}')
        ddg_process_id = str(ddg_process_id_info[0]).split()[3][0:-3]
         
        with open(join(folder.ddG_run, f'job_id_ddg.txt'), 'w') as job_id_file:     
            job_id_file.write(ddg_process_id)                                                            
                                    
        #Launching parse_ddgs.sbatch
        parse_results_call = subprocess.Popen(f'sbatch --dependency=afterany:{ddg_process_id} {join(folder.ddG_input, "parse_ddgs.sbatch")}', stdout=subprocess.PIPE, shell=True, cwd=folder.ddG_run)
    else:
        ddg_process_ids = []
        for index, sub_ddg_folder in enumerate(folder.ddG_input):
            #Launching Rosetta_ddg.sbatch
            ddg_call = subprocess.Popen(f'sbatch {dependency}{parse_relax_process_id} {join(folder.ddG_input[index], "rosetta_ddg.sbatch")}', 
                stdout=subprocess.PIPE, shell=True, cwd=folder.ddG_run[index])

            #Gettin process ID                                
            ddg_process_id_info = ddg_call.communicate()
            logger.info(f'ddG process ID info: {ddg_process_id_info}')
            ddg_process_id = str(ddg_process_id_info[0]).split()[3][0:-3]
             
            with open(join(folder.ddG_run[index], f'job_id_ddg.txt'), 'w') as job_id_file:     
                job_id_file.write(ddg_process_id)                                                            
                                        
        #Launching post_parse_ddgs.sbatch
        ddg_process_ids = ':'.join(ddg_process_ids)
        parse_results_call = subprocess.Popen(f'sbatch --dependency=afterany:{ddg_process_ids} {join(folder.ddG_postparse_input, "parse_ddgs.sbatch")}', 
                stdout=subprocess.PIPE, shell=True, cwd=folder.ddG_postparse_run)

    return
