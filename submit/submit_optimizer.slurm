#!/bin/bash
#
# based on Slurm workload manager
#
# ==== Job Attributes
#SBATCH --output=submit/out/optimizer.o
#SBATCH --error=submit/out/optimizer.e
#SBATCH --gres=gpu:p100
#SBATCH --partition=gpu2
#SBATCH --job-name=optimize
#
# ==== Resource Requirements and Limits
#SBATCH --ntasks=1
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=4GB
#SBATCH --cpus-per-task=1
#
# ==== Standard Environment
export TMPDIR=/tmp/slurm.${SLURM_JOBID}
# ==== end of preamble

python3 -u -m optimize $SLURM_ARRAY_TASK_ID --verbose 0 --name 'final' -b 1