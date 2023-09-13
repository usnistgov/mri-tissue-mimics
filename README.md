# MRI Tissue Mimics

This repository is used to aid in finding MRI tissue relaxation times for a target field strength, and to provide functionality to solve for tissue mimic composition given target tissue relaxation times.

## 0. Setup, Requirements, and Command Line Calls

The `requirements.txt` file has the required packages that need to be installed to run the code in this repository. 

The recommended way to setup the requirements for this repository is to create a virtual environment, and to install the required packages there. The user may choose to use their package manager and interface of choice.

One way to create and manage virtual environments is to use 
[Conda](https://conda.io/projects/conda/en/latest/index.html#), a package management system that runs on Windows, macOS, and Linux. You can follow the installation guide to install Conda
 [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

Once Conda is installed, you can create a Python virtual environment called `myenv` (choose any name of your liking), activate the environment, and install the required packages into the environment by executing these commands in the terminal (for macOS) or in the command line (for Windows):
```
conda create --name myenv python
conda activate myenv
pip install -r requirements.txt
```

You are now set up to run the rest of the commands in this README. Remember, in order to run any of the commands below in the terminal/command line, you must first activate 
your visrtual environment. If using conda, this amounts to running: `conda activate myenv`. When finished executing code, you can exit the conda environment
using `conda deactivate`.

## 1. Get Tissue Relaxation Times
The `get_relaxation_times.py` file allows users to get T1 and T2 relaxation times for a given field strength for a tissue's field-dependent model. As inputs, this function requires the target field strength (given in T), as well as names of csv files that hold the tissue dispersion model parameters. 

Example T1 and T2 csv files for white matter dispersion models are included in the `examples/configs` folder. The required parameters are: 
```
['n_lorentzian', 'big_a', 'numerator_0', 'numerator_1', 'numerator_2', 
 'tau_0', 'beta_0', 'c_0', 'tau_1', 'beta_1', 'c_1', 'tau_2', 'beta_2', 'c_2']
```

For an example command line call with an optional output file name, run:
<details> <summary> <em> Mac OS Terminal </em> </summary>

```
python get_relaxation_times.py \
--target-field 0.55 \
--t1-model-file examples/configs/white_matter_t1.csv \
--t2-model-file examples/configs/white_matter_t2.csv \
--output-file examples/output_test_relaxation.csv
```
</details>
<details> <summary> <em> Windows Powershell </em> </summary>

```
python get_relaxation_times.py `
--target-field 0.55 `
--t1-model-file examples/configs/white_matter_t1.csv `
--t2-model-file examples/configs/white_matter_t2.csv `
--output-file examples/output_test_relaxation.csv
```
</details>
<details> <summary> <em> Windows Command Line </em> </summary>

```
python get_relaxation_times.py ^
--target-field 0.55 ^
--t1-model-file examples/configs/white_matter_t1.csv ^
--t2-model-file examples/configs/white_matter_t2.csv ^
--output-file examples/output_test_relaxation.csv
```
</details>

### 1.1 Get Tissue Relaxation Times -- Function Arguments
The function arguments for `get_relaxation_times.py.py` are:
```
  -h, --help            Show Help message and exit
  --target-field TARGET_FIELD
                        Target field strength in Tesla
  --t1-model-file T1_MODEL_FILE
                        CSV file containing the T1 model parameters for the tissue
  --t2-model-file T2_MODEL_FILE
                        CSV file containing the T2 model parameters for the tissue
  --output-file OUTPUT_FILE
                        (Optional) Output file to save relaxation times to
```

## 2. Get Mimic Composition Concentration

The `get_concentrations.py` file allows users to calculate the composition (salt and agarose concentrations) for a target (T1, T2) pair, given a particular parametric salt mixing model. As inputs, this function requires the target T1 and T2 times (given in seconds), as well as names of csv files that hold the mixing model parameters for the chosen parametric salt. 

Example T1 and T2 csv files for manganese and agarose mixing models at 0.55 T are included in the `examples/configs` folder. The required model parameters are:
```
['dim', 'a1', 'param_ag_1', 'param_oth_1', 'param_mix_1', 'param_ag_2', 
 'param_oth_2', 'param_mix_2', 'param_mix_3', 'param_mix_4']
```

For an example command line call for target T1 and T2 times that lie within the mixing model range, run:
<details> <summary> <em> Mac OS Terminal </em> </summary>

```
python get_concentrations.py \
--target-t1 1.064 \
--target-t2 0.218 \
--t1-model-file examples/configs/manganese_agarose_t1_0p55.csv \
--t2-model-file examples/configs/manganese_agarose_t2_0p55.csv
```
</details>
<details> <summary> <em> Windows Powershell </em> </summary>

```
python get_concentrations.py `
--target-t1 1.064 `
--target-t2 0.218 `
--t1-model-file examples/configs/manganese_agarose_t1_0p55.csv `
--t2-model-file examples/configs/manganese_agarose_t2_0p55.csv
```
</details>
<details> <summary> <em> Windows Command Line </em> </summary>

```
python get_concentrations.py ^
--target-t1 1.064 ^
--target-t2 0.218 ^
--t1-model-file examples/configs/manganese_agarose_t1_0p55.csv ^
--t2-model-file examples/configs/manganese_agarose_t2_0p55.csv
```
</details>

For an example command line call that demonstrates saving outputs to a file and uses target T1 and T2 times that lie outside of the mixing model range, run:
<details> <summary> <em> Mac OS Terminal </em> </summary>

```
python get_concentrations.py \
--target-t1 0.203 \
--target-t2 0.086 \
--t1-model-file examples/configs/manganese_agarose_t1_0p55.csv \
--t2-model-file examples/configs/manganese_agarose_t2_0p55.csv \
--output-file examples/output_test_concentrations.csv
```
</details>
<details> <summary> <em> Windows Powershell </em> </summary>

```
python get_concentrations.py `
--target-t1 0.203 `
--target-t2 0.086 `
--t1-model-file examples/configs/manganese_agarose_t1_0p55.csv `
--t2-model-file examples/configs/manganese_agarose_t2_0p55.csv `
--output-file examples/output_test_concentrations.csv
```
</details>
<details> <summary> <em> Windows Command Line </em> </summary>

```
python get_concentrations.py ^
--target-t1 0.203 ^
--target-t2 0.086 ^
--t1-model-file examples/configs/manganese_agarose_t1_0p55.csv ^
--t2-model-file examples/configs/manganese_agarose_t2_0p55.csv ^
--output-file examples/output_test_concentrations.csv
```
</details>

### 2.1 Get Mimic Composition Concentration -- Function Arguments
The function arguments for `get_concentrations.py` are:
```
  -h, --help            Show Help message and exit
  --target-t1 TARGET_T1
                        Target T1 value to mimic in seconds
  --target-t2 TARGET_T2
                        Target T2 value to mimic in seconds
  --t1-model-file T1_MODEL_FILE
                        CSV file containing the T1 model parameters
  --t2-model-file T2_MODEL_FILE
                        CSV file containing the T2 model parameters
  --output-file OUTPUT_FILE
                        (Optional) Output file to save concentrations for mimic to
```

---

This repository is developed and maintained
by the Magnetic Imaging group, principally:

- Kathryn Keenan, @katykeenan-nist

Please reach out with questions and comments.
