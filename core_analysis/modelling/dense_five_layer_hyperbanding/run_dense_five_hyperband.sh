#!/bin/bash -l
#SBATCH -c 10
#SBATCH --mem=10G
#SBATCH --job-name=dense_5_hyperbanding
#SBATCH --time=0-48:00:00
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --output=$log/core_analysis/modelling/dense_branch/dense_5_hyperbanding/dense_5_hyperbanding-%j.output
#SBATCH --error=$log/core_analysis/modelling/dense_branch/dense_5_hyperbanding/dense_5_hyperbanding-%j.error

wd=$modelling/core_analysis/modelling/dense_branch/dense_5_hyperbanding


source ~/.bashrc
eval "$(conda shell.bash hook)"
conda activate python3710

cd $wd || exit
python3 main.py

