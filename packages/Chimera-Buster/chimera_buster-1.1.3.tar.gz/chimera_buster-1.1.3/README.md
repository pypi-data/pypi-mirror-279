# Chimera_Buster
### Overview
This package takes concensus fasta files from the MrHamer pipeline and eliminates chimeric reads by comparing the UMI sequences and finding any matches in the 5' or 3' UMIs and keeping the sequence that has the highest prevalence.
******************
## Installation
##### Requires python<=3.10
### Quick Install
```bash
pip install Chimera_Buster
```
### Manual Install
```bash
git clone https://github.com/JessicaA2019/Chimera_Buster.git 
cd Chimera_Buster
python setup.py install
```
### Dependencies
Some dependencies currently do not install with Chimera_Buster. Please pip install the following dependencies:
* edlib
* pandas
* multiprocessing
* argparse

### Testing
To test if the installation was successful run the following command with the test files provided:
```bash
Chimera_Buster CB_test_files CB_test
 ```
******************
## Usage
    Chimera_Buster [options] {input_folder_name} {output_file_prefix}
### Inputs
To run the pipeline the following input files are required:
| Input | Description |
| ------ | ------ |
|input_folder_name  |    Designates MrHAMER folder to be filtered. This is required.|
|  output_file_prefix  |  Designates output file prefix. This is required.|
The following input files are optional:
| Arguement | Function |
| ------ | ------ |
|-h, --help |  Prints help message to terminal. |
|-m int, --mismatch int|  Designates the maximum number of mismatched/indel bases allowed when comparing UMIs. Default is 1. |
### Outputs
 The main output files created by the pipeline are:
| Output | Description |
|--------|-------------|
| {output_file_prefix}_chimera_list.txt | A list of all chimeric sample IDs. |
| {output_file_prefix}_nonchimera_list.txt | A list of all nonchimeric sample IDs. |
| {output_file_prefix}_chimeras.csv | A csv of the sample ID, UMI sequences, and cluster counts for each chimeric read. |
| {output_file_prefix}_nonchimeras.csv |  A csv of the sample ID, UMI sequences, and cluster counts for each nonchimeric read. |

**************************
## Help
For issues or bugs, please report them on the [issues page][issues]. 

## License

MIT - Copyright (c) 2024 Jessica Lauren Albert

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [issues]: <https://github.com/JessicaA2019/Chimera_Buster/issues>