from functions.concentrations_from_mixing import get_sample_concentrations
from models.utils import get_lmfit_params_from_df
import pandas as pd
import argparse
import sys


def parse_args(args):
    parser = argparse.ArgumentParser(description='Find salt and agarose concentrations to mimic T1 and T2.')
    parser.add_argument('--target-t1', dest='target_t1',
                        type=float, action="store", required=True,
                        help='Target T1 value to mimic in seconds')
    parser.add_argument('--target-t2', dest='target_t2',
                        type=float, action="store", required=True,
                        help='Target T2 value to mimic in seconds')
    parser.add_argument('--t1-model-file', dest='t1_model_file',
                        type=str, action='store', required=True,
                        help='CSV file containing the T1 model parameters')
    parser.add_argument('--t2-model-file', dest='t2_model_file',
                        type=str, action='store', required=True,
                        help='CSV file containing the T2 model parameters')
    parser.add_argument('--output-file', dest='output_file',
                        type=str, action='store', required=False,
                        help='(Optional) Output file to save concentrations for mimic to')
    return parser.parse_args(args)


def main(args):
    """Main function: Given target T1 and T2 values, and using the provided T1 and T2 mixing models,
      get the sample concentration (and its resulting t1 and t2 times).
    """
    target_t1 = args.target_t1
    target_t2 = args.target_t2
    t1_model_file = args.t1_model_file
    t2_model_file = args.t2_model_file

    print("------------------------------------------------")
    print("Solving for T1 of", target_t1, "s and T2 of", target_t2, "s")
    print("Using t1 model:", t1_model_file)
    print("Using t2 model:", t2_model_file)
    print("------------------------------------------------")

    # Get model parameters from csv files
    expected_params = [
        "dim", "a1", "param_ag_1", "param_oth_1", "param_mix_1", "param_ag_2", 
        "param_oth_2", "param_mix_2", "param_mix_3", "param_mix_4"]
    print("Loading T1 model")
    params_t1_pd = pd.read_csv(t1_model_file)
    params_t1 = get_lmfit_params_from_df(params_t1_pd, params_to_find=expected_params.copy())
    print("Loading T2 model")
    params_t2_pd = pd.read_csv(t2_model_file)
    params_t2 = get_lmfit_params_from_df(params_t2_pd, params_to_find=expected_params.copy())

    # Find concentrations for mimicking target T1 and T2
    concentrations, t1_t2_values = get_sample_concentrations(params_t1, params_t2, target_t1, target_t2)

    print("Finished.")
    print("\nTarget T1 (s):", target_t1, "T2 (s):", target_t2)
    print("Solution(s):")
    for i in range(len(concentrations)):
        print("\tAgarose (% w/v):", concentrations[i][0], "Salt (mM):", concentrations[i][1], "\tfor T1 (s):", t1_t2_values[i][0], "T2 (s):", t1_t2_values[i][1])

    if args.output_file is not None:
        print("Saving to:", args.output_file)
        df_conc = pd.DataFrame(concentrations, columns=["agarose_concentration__wv", "salt_concentration__mM"])
        df_times = pd.DataFrame(t1_t2_values, columns=["t1__s", "t2__s"])
        df = pd.concat([df_conc, df_times], axis=1)
        df["target_t1__s"] = target_t1
        df["target_t2__s"] = target_t2
        df["t1_model_file"] = t1_model_file
        df["t2_model_file"] = t2_model_file
        df.to_csv(args.output_file, index=False)


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    main(args)