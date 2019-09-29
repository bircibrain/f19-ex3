#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=briana.oshiro@uconn.edu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2gb
#SBATCH --time=10:00:00    
#SBATCH -e error_part2.log    
#SBATCH -o output_part2.log
#SBATCH --job-name=part2
#SBATCH --partition=serial
##### END OF JOB DEFINITION  #####

module load singularity
singularity run \
--bind /scratch/psyc5171/$USER/f19-ex3:/data \
/scratch/psyc5171/containers/neurodesign_latest.sif \
/data/optimize_part2.py
