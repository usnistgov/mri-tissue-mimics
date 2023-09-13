import numpy as np
from models.utils import get_lmfit_params_from_df


# CONSTANTS
GAMMA = 42.6 * 1e6  # Hz/T


def model_general_lorentzian(params, b0, debug=False):
    """Get general Lorentzian form
    """
    n_lors = params["n_lorentzian"].value
    big_a = params[f"big_a"].value
    numerators = [params[f"numerator_0"].value,
                  params[f"numerator_1"].value,
                  params[f"numerator_2"].value]

    model = big_a
    for i in range(n_lors):
        tau = params[f"tau_{i}"].value
        beta = params[f"beta_{i}"].value
        c = params[f"c_{i}"].value
        lor_to_add = lorentzian(tau, b0, numerators, c, beta)

        if debug:
            print("Modeled gen lor", tau, numerators, c, beta, np.max(lor_to_add))
            
        model = model + lor_to_add

    model = 1/model  # Invert to get T1 or T2

    return model


def lorentzian(tau, b0, numerators, c, beta=2):
    w = GAMMA * b0
    lor = (
            numerators[0] +
            (numerators[1] / (1 + pow(w * tau, beta))) +
            (numerators[2] / (1 + pow(2 * w * tau, beta)))
    )
    # Multiply lorentzian by c and tau
    lor = lor * c * tau
    return lor


def get_predictions(fit_params, field_range):
    # Model lorentzian
    params_to_find = ['n_lorentzian', 'big_a', 'numerator_0', 'numerator_1', 'numerator_2',
                       'tau_0', 'beta_0', 'c_0', 
                       'tau_1', 'beta_1', 'c_1',
                       'tau_2', 'beta_2', 'c_2']
    
    # Get and validate parameters
    fit_params = get_lmfit_params_from_df(fit_params, params_to_find=params_to_find)
    model_output = model_general_lorentzian(fit_params, field_range)

    return model_output
