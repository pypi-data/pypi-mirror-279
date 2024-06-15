# Symbolic Modeling Tool

This package converts symbolic functions written in sympy to their numerical versions and also generates the Jacobian matrix.

## Features

- Convert symbolic functions to numerical versions
- Generate the Jacobian matrix for the functions

## Installation

To install the package, use pip:

```sh
pip install ps_symbolic_modeling_tool
```

## Usage Example

Put your symbolic code and model information into a folder (suppose the folder is named `sym_files`).

<!-- 2. Run the converter script:

```sh
python3 -m my_tool --folder_name sym_files
``` -->

### From another Python script

```python
import ps_symbolic_modeling_tool

# Define the paths
folder_path_for_files_to_be_converted = 'sym_files'
num_output_folder_path = 'num_files'
jac_output_folder_path = 'jac_files'

# Generate numerical functions
ps_symbolic_modeling_tool.to_num(folder_path_for_files_to_be_converted, num_output_folder_path)

# Generate Jacobian functions
ps_symbolic_modeling_tool.to_jac(folder_path_for_files_to_be_converted, jac_output_folder_path)
```

### From the CLI

```sh
ps_symbolic_modeling_tool num --folder_name sym_files --output_folder num_files
ps_symbolic_modeling_tool jac --folder_name sym_files --output_folder jac_files

```

## Licence
This project is licensed under the GNU Lesser General Public License v3.0 (LGPL-3.0) [LICENCE](COPYING.LESSER).

## Contact

If you have any questions or feedback, please contact [tianqi.hong@uga.edu](mailto:tianqi.hong@uga.edu).
