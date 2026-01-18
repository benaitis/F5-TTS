# Lithuanian Training Guide for F5-TTS

This guide explains how to train F5-TTS with Lithuanian language data, including the necessary code modifications and training procedures.

## Overview

F5-TTS was originally designed for Chinese and English, using pinyin conversion for Chinese text. To support Lithuanian, we need to modify the text processing pipeline to use character-based tokenization instead of pinyin conversion, as Lithuanian has more regular orthography.

## Required Files

### 1. Lithuanian Vocabulary File

- **Location**: `/data/vocab_lithuanian.txt`
- **Content**: Contains Lithuanian alphabet including diacritics (ą, ę, ė, į, ų, ū, č, š, ž)
- **Format**: One character per line, including punctuation and symbols

### 2. Modified Processing Script

- **File**: `src/f5_tts/train/datasets/prepare_csv_wavs.py`
- **Changes**: Added `--tokenizer` parameter supporting character-based tokenization

### 3. Lithuanian Utilities (Optional)

- **File**: `src/f5_tts/utils/lithuanian.py`
- **Purpose**: Contains Lithuanian-specific text processing functions

## Code Modifications Made

### 1. Updated `prepare_csv_wavs.py`

The script now supports different tokenization methods:

```python
# Added tokenizer parameter support
def batch_convert_texts(texts, tokenizer="pinyin", polyphone=True, batch_size=BATCH_SIZE):
    if tokenizer == "pinyin":
        converted_batch = convert_char_to_pinyin(batch, polyphone=polyphone)
    elif tokenizer == "char":
        # Character-based tokenization (no conversion needed)
        converted_batch = batch
    else:
        raise ValueError(f"Unsupported tokenizer: {tokenizer}")
```

### 2. Updated Vocabulary Path

```python
# Changed from Chinese vocab to Lithuanian vocab
PRETRAINED_VOCAB_PATH = files("f5_tts").joinpath("../../data/vocab_lithuanian.txt")
```

### 3. Added CLI Parameters

```bash
--tokenizer char  # For Lithuanian character-based tokenization
--tokenizer pinyin  # For Chinese pinyin conversion (default)
```

## Training Procedure

### Step 1: Prepare Your Dataset

Organize your Lithuanian dataset in the required CSV format:

```
/your_lithuanian_dataset/
├── metadata.csv
└── wavs/
    ├── audio_0001.wav
    ├── audio_0002.wav
    └── ...
```

**metadata.csv format:**

```csv
audio_file|text
wavs/audio_0001.wav|Labas rytas! Kaip jūs šiandien jaučiatės?
wavs/audio_0002.wav|Lietuvių kalba yra labai graži kalba.
```

### Step 2: Process the Dataset

Run the modified preparation script with character-based tokenization:

```bash
python src/f5_tts/train/datasets/prepare_csv_wavs.py \
    /path/to/your/lithuanian/dataset \
    /path/to/output/dataset \
    --tokenizer char \
    --workers 4
```

**Parameters explained:**

- `--tokenizer char`: Use character-based tokenization (essential for Lithuanian)
- `--workers 4`: Number of parallel workers for processing
- `--pretrain`: Add this flag if training from scratch (optional)

### Step 3: Training Configuration

Update your training configuration file:

```yaml
model:
  tokenizer: custom # Use custom tokenizer
  tokenizer_path: /path/to/F5-TTS/data/vocab_lithuanian.txt # Point to Lithuanian vocab

datasets:
  name: your_lithuanian_dataset # Your dataset name
  # ... other dataset parameters
```

### Step 4: Start Training

```bash
python train.py --config your_lithuanian_config.yaml
```

## Key Differences from Chinese Training

| Aspect              | Chinese                                  | Lithuanian                       |
| ------------------- | ---------------------------------------- | -------------------------------- |
| **Tokenizer**       | `pinyin`                                 | `char`                           |
| **Text Processing** | Chinese segmentation + pinyin conversion | Direct character tokenization    |
| **Vocabulary**      | Pinyin syllables + characters            | Lithuanian alphabet + diacritics |
| **Preprocessing**   | `convert_char_to_pinyin()`               | Direct character mapping         |

## Why Character-Based Tokenization Works for Lithuanian

1. **Regular Orthography**: Lithuanian spelling closely matches pronunciation
2. **Phonetic Alphabet**: Lithuanian uses a mostly phonetic writing system
3. **Diacritic Support**: The vocabulary includes all Lithuanian diacritical marks
4. **Simplicity**: No need for complex phonetic conversion like Chinese pinyin

## Troubleshooting

### Common Issues

1. **Missing Characters Error**

   - **Problem**: Vocabulary doesn't contain all Lithuanian characters
   - **Solution**: Check and update `vocab_lithuanian.txt` to include missing characters

2. **Wrong Tokenizer**

   - **Problem**: Using `--tokenizer pinyin` for Lithuanian text
   - **Solution**: Always use `--tokenizer char` for Lithuanian

3. **Encoding Issues**
   - **Problem**: Lithuanian diacritics not displaying correctly
   - **Solution**: Ensure all files use UTF-8 encoding

### Validation

Check if your vocabulary covers your text:

```python
# Read your vocabulary
with open('data/vocab_lithuanian.txt', 'r', encoding='utf-8') as f:
    vocab_chars = set(char.strip() for char in f)

# Check your text
text = "Jūsų lietuviškas tekstas čia"
missing_chars = set(text) - vocab_chars
if missing_chars:
    print(f"Missing characters: {missing_chars}")
```

## Advanced Features

### Lithuanian Phonetic Rules (Optional)

The `src/f5_tts/utils/lithuanian.py` file includes optional phonetic normalization:

```python
from f5_tts.utils.lithuanian import apply_lithuanian_phonetic_rules

# Apply phonetic rules if needed
normalized_text = apply_lithuanian_phonetic_rules(raw_text)
```

### Multi-language Support

To train on both Lithuanian and English:

1. Include English characters in vocabulary
2. Mix Lithuanian and English audio in dataset
3. Use character-based tokenization for both languages

## Performance Tips

1. **Audio Quality**: Use high-quality, clean audio recordings
2. **Duration**: Keep audio clips between 3-30 seconds
3. **Transcription Accuracy**: Ensure perfect transcription alignment
4. **Speaker Diversity**: Include multiple speakers for better generalization

## References

- [Original GitHub Discussion](https://github.com/SWivid/F5-TTS/discussions/57#discussioncomment-10959029)
- [F5-TTS Documentation](https://github.com/SWivid/F5-TTS)
- Lithuanian Language Resources for TTS training

## Support

For issues specific to Lithuanian training:

1. Check that vocabulary file contains all required characters
2. Verify tokenizer is set to "char" not "pinyin"
3. Ensure dataset format matches requirements
4. Test with small dataset first before full training
