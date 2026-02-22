#!/bin/bash
#SBATCH -J f5tts
#SBATCH -o train.out
#SBATCH -e train.err
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 12:00:00
#SBATCH --gres=gpu:1

module load cuda
source ~/F5-TTS/venv/bin/activate
cd ~/F5-TTS

python src/f5_tts/train/train.py \
  --config configs/base.yaml

