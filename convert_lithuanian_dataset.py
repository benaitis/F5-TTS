#!/usr/bin/env python3
"""
Convert Lithuanian dataset from filelist format to CSV format for F5-TTS training.
Handles pronunciation markings and creates proper directory structure.
"""

import os
import shutil
from pathlib import Path
import csv


def clean_lithuanian_text(text):
    """
    Clean Lithuanian text by removing pronunciation markings.
    
    Pronunciation markings in your data:
    ^ - primary stress
    ~ - secondary stress  
    ` - other stress marking
    """
    # Remove pronunciation markings
    cleaned = text.replace('^', '').replace('~', '').replace('`', '')
    
    # Clean up any double spaces that might result
    cleaned = ' '.join(cleaned.split())
    
    return cleaned


def convert_filelist_to_csv(input_dir, output_dir):
    """
    Convert filelist format to CSV format expected by F5-TTS.
    
    Args:
        input_dir: Directory containing filelist_A.txt and filelist_V.txt
        output_dir: Output directory for converted dataset
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory structure
    output_path.mkdir(parents=True, exist_ok=True)
    wavs_dir = output_path / "wavs"
    wavs_dir.mkdir(exist_ok=True)
    
    # Collect all audio-text pairs
    all_pairs = []
    audio_counter = 1
    
    # Process both speaker files
    for txt_file in ["filelist_A.txt", "filelist_V.txt"]:
        txt_path = input_path / txt_file
        
        if not txt_path.exists():
            print(f"Warning: {txt_file} not found, skipping...")
            continue
            
        print(f"Processing {txt_file}...")
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                # Split on pipe character
                if '|' not in line:
                    print(f"Warning: Line {line_num} in {txt_file} missing '|' separator, skipping")
                    continue
                    
                parts = line.split('|', 1)  # Split only on first pipe
                if len(parts) != 2:
                    print(f"Warning: Line {line_num} in {txt_file} has incorrect format, skipping")
                    continue
                    
                audio_path, text = parts
                audio_path = audio_path.strip()
                text = text.strip()
                
                # Check if source audio file exists
                # The filelist might have paths like "Aiste/wav/filename.wav" but actual files are in "wav/filename.wav"
                source_audio = input_path / audio_path
                if not source_audio.exists():
                    # Try alternative path structure - extract just the filename and look in wav/
                    filename_only = Path(audio_path).name
                    alternative_source = input_path / "wav" / filename_only
                    if alternative_source.exists():
                        source_audio = alternative_source
                    else:
                        print(f"Warning: Audio file {source_audio} not found, skipping")
                        continue
                
                # Clean the text (remove pronunciation markings)
                cleaned_text = clean_lithuanian_text(text)
                
                # Create new filename with counter (to avoid conflicts between speakers)
                file_extension = source_audio.suffix
                new_filename = f"audio_{audio_counter:05d}{file_extension}"
                target_audio = wavs_dir / new_filename
                
                # Copy audio file to new location
                try:
                    shutil.copy2(source_audio, target_audio)
                    print(f"  Copied: {audio_path} -> wavs/{new_filename}")
                except Exception as e:
                    print(f"Error copying {source_audio}: {e}")
                    continue
                
                # Add to pairs list
                all_pairs.append((f"wavs/{new_filename}", cleaned_text))
                audio_counter += 1
    
    # Write metadata.csv
    metadata_path = output_path / "metadata.csv"
    with open(metadata_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        
        # Write header
        writer.writerow(['audio_file', 'text'])
        
        # Write all pairs
        for audio_file, text in all_pairs:
            writer.writerow([audio_file, text])
    
    print(f"\nConversion complete!")
    print(f"Total audio files processed: {len(all_pairs)}")
    print(f"Dataset saved to: {output_path}")
    print(f"Metadata file: {metadata_path}")
    
    return output_path


def main():
    # Configuration
    input_dir = "/Users/a1/Downloads/Aistės_Vlado_balsai"
    output_dir = "/Users/a1/Documents/F5-TTS/data/lithuanian_dataset"
    
    print("Converting Lithuanian dataset to F5-TTS format...")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Convert the dataset
    converted_path = convert_filelist_to_csv(input_dir, output_dir)
    
    print(f"\nNext steps:")
    print(f"1. Verify the conversion by checking: {converted_path}/metadata.csv")
    print(f"2. Run the F5-TTS preparation script:")
    print(f"   python src/f5_tts/train/datasets/prepare_csv_wavs.py \\")
    print(f"       {converted_path} \\")
    print(f"       data/lithuanian_processed \\")
    print(f"       --tokenizer char \\")
    print(f"       --workers 4")


if __name__ == "__main__":
    main()