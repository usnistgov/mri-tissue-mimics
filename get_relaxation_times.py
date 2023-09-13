from models.tissue_lorentzian_models import get_predictions
import pandas as pd
import argparse
import sys
import numpy as np


def parse_args(args):
    parser = argparse.ArgumentParser(description='Find T1 and T2 relaxation times for a given field strength and tissue model.')
    parser.add_argument('--target-field', dest='target_field',
                        type=float, action="store", required=True,
                        help='Target field strength in Tesla')
    parser.add_argument('--t1-model-file', dest='t1_model_file',
                        type=str, action='store', required=True,
                        help='CSV file containing the T1 model parameters for the tissue')
    parser.add_argument('--t2-model-file', dest='t2_model_file',
                        type=str, action='store', required=True,
                        help='CSV file containing the T2 model parameters for the tissue')
    parser.add_argument('--output-file', dest='output_file',
                        type=str, action='store', required=False,
                        help='(Optional) Output file to save relaxation times to')
    return parser.parse_args(args)


def main(args):
    """Main function: Given target field strength and field-dependent tissue model, find tissue T1 and T2 relaxation times.
    """
    target_field = args.target_field
    t1_model_file = args.t1_model_file
    t2_model_file = args.t2_model_file

    print("------------------------------------------------")
    print("Solving for target field", target_field, "T")
    print("Using t1 model:", t1_model_file)
    print("Using t2 model:", t2_model_file)
    print("------------------------------------------------")

    # Get tissue values and add it to the dataframe
    t1_params_df = pd.read_csv(t1_model_file)
    t2_params_df = pd.read_csv(t2_model_file)
    t1_tissue = get_predictions(t1_params_df, target_field)
    t1_tissue = np.round(t1_tissue, decimals=3)
    t2_tissue = get_predictions(t2_params_df, target_field)
    t2_tissue = np.round(t2_tissue, decimals=3)

    print("Finished.")
    print("Solution:\n\tTissue T1 (s):", t1_tissue, "T2 (s):", t2_tissue)

    if args.output_file is not None:
        print("Saving to:", args.output_file)
        df = pd.DataFrame({
            "t1__s": [t1_tissue],
            "t2__s": t2_tissue,
            "target_field__t": target_field,
            "t1_model_file": t1_model_file,
            "t2_model_file": t2_model_file
        })
        df.to_csv(args.output_file, index=False)


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    main(args)