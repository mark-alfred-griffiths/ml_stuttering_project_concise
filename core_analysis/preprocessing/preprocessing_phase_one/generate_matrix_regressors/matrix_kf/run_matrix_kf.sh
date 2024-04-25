#!/bin/bash -l
#SBATCH --exclusive
#SBATCH -c 6
#SBATCH --mem=59000
#SBATCH --job-name=matrix_kf
#SBATCH --time=0-00:05:00
#SBATCH --partition=partition-1
#SBATCH --ntasks=1
#SBATCH --output=/home/markgreenneuroscience_gmail_com/LOG/TS_KF_TRANSFORMS/generate_matrix_regressors/matrix_kf/matrix_kf-%j.output
#SBATCH --error=/home/markgreenneuroscience_gmail_com/LOG/TS_KF_TRANSFORMS/generate_matrix_regressors/matrix_kf/matrix_kf-%j.error

wd=/home/markgreenneuroscience_gmail_com/TS_KF_TRANSFORMS/GENERATE_MATRIX_REGRESSORS/MATRIX_KF

control_file_dir=/home/markgreenneuroscience_gmail_com/TS_KF_TRANSFORMS/GENERATE_MATRIX_REGRESSORS/MATRIX_REGRESSORS_CF
matrix_control_file=${control_file_dir}/MATRIX_CONTROL_FILE.txt
feat_num=$(sed -n "${SLURM_ARRAY_TASK_ID}"p ${matrix_control_file} | awk '{print $1}')

source /etc/bash.bashrc
eval "$(conda shell.bash hook)"
conda activate python3710

cd $wd || exit
python3 MATRIX_KF.py "$feat_num"
