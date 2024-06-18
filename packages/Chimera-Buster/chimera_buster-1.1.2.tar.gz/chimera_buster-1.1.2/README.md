# Chimera_Buster

This package takes concensus fasta files from the MrHamer pipeline and eliminates chimeric reads by comparing the UMI sequences and finding any matches in the 5' or 3' UMIs and keeping the sequence that has the highest prevalence.

## Installation

    pip install Chimera_Buster

## Usage
    Chimera_Buster [options] input_folder_name output_file_prefix

positional arguments:
| Arguement | Function |
| ------ | ------ |
|input_folder_name  |    Designates MrHAMER folder to be filtered. This is required.|
|  output_file_prefix  |  Designates output file prefix. This is required.|

options:
| Arguement | Function |
| ------ | ------ |
|-h, --help |  show this help message and exit |
|-m int, --mismatch int|  Designates the maximum number of mismatched/indel bases allowed. Default is 1. |

## License

MIT - Copyright (c) 2024 Jessica Lauren Albert

