import numpy as np
import sympy
from models.mixing_models import get_mixing_model, get_mixing_model_equation, get_mixing_model_quadratic_params
from models.equation_solvers import solve_sympy_equations, solve_quad_eq_positive_only


def get_closest_concentration_to_target(agarose_concentration_options, salt_concentration_options, 
                                        mixing_params, target_relaxation, target_datatype):
    """For given target T1 and T2 values, and using the provided T1 and T2 mixing models (given by params_t1 and params_t2),
      get the sample concentration (and its resulting t1 and t2 times).
    """
    relaxation_times = []
    relaxation_time_concentrations = []
    for salt_conc in salt_concentration_options:
        relaxation_times.append(get_mixing_model(mixing_params, 0, salt_conc, datatype=target_datatype))
        relaxation_time_concentrations.append([0, salt_conc])
    for ag_conc in agarose_concentration_options:
        relaxation_times.append(get_mixing_model(mixing_params, ag_conc, 0, datatype=target_datatype))
        relaxation_time_concentrations.append([ag_conc, 0])
    # print(relaxation_times, relaxation_time_concentrations)
    if len(relaxation_times) > 1:
        closest_t1_idx = np.argmin(np.abs(np.array(relaxation_times) - target_relaxation))
        relaxation_times = relaxation_times[closest_t1_idx]
        relaxation_time_concentrations = relaxation_time_concentrations[closest_t1_idx]

    return relaxation_times, relaxation_time_concentrations


def get_sample_concentrations(params_t1, params_t2, target_t1, target_t2):

    # Get (approximate) solution for this tissue and sample model
    agarose_concentration_eq, salt_concentration_eq = sympy.symbols("agarose_concentration salt_concentration", real=True)
    t1_eq = get_mixing_model_equation(params_t1, agarose_concentration_eq, salt_concentration_eq, target_t1,
                                            datatype="t1__s")
    t2_eq = get_mixing_model_equation(params_t2, agarose_concentration_eq, salt_concentration_eq, target_t2,
                                            datatype="t2_1__s")
    sample_concentrations = solve_sympy_equations([t1_eq, t2_eq], variables=[agarose_concentration_eq, salt_concentration_eq])
    sample_concentrations = np.round(np.asarray(sample_concentrations).reshape(2, ).astype(float), decimals=3)

    # Check that resulting T1 and T2 for these concentrations match target T1 and T2
    agarose_concentration = np.max([0, sample_concentrations[0]])
    salt_concentration = np.max([0, sample_concentrations[1]])
    t1_model_output_samp = get_mixing_model(params_t1, agarose_concentration, salt_concentration, datatype="t1__s")
    t2_model_output_samp = get_mixing_model(params_t2, agarose_concentration, salt_concentration, datatype="t2_1__s")
    found_matching = np.all(np.abs([(t1_model_output_samp - target_t1) / target_t1,
                        (t2_model_output_samp - target_t2) / target_t2]) <= 0.1)

    if found_matching:
        sample_concentrations = [sample_concentrations]  # this is the only solution
    
    else:  # Solve for optimal T1 and T2 seprately, since no combined solution exists
        print("Could not find one solution for target T1 and T2")

        print("\tSolving independently for best T1 concentration")
        t1_valid_concentrations_salt = solve_quad_eq_positive_only(*get_mixing_model_quadratic_params(params_t1, target_t1, "salt"))
        t1_valid_concentrations_ag = solve_quad_eq_positive_only(*get_mixing_model_quadratic_params(params_t1, target_t1, "agarose"))
        # Only keep the solution that has the closest T2
        t2_for_options, closest_t1_conc = get_closest_concentration_to_target(
            t1_valid_concentrations_ag, t1_valid_concentrations_salt, 
            params_t2, target_t2, target_datatype="t2_1__s")
        # print(t2_for_options, closest_t1_conc)

        print("\tSolving independently for best T2 concentration")
        t2_valid_concentrations_salt = solve_quad_eq_positive_only(*get_mixing_model_quadratic_params(params_t2, target_t2, "salt"))
        t2_valid_concentrations_ag = solve_quad_eq_positive_only(*get_mixing_model_quadratic_params(params_t2, target_t2, "agarose"))
        # Only keep the solution that has the closest T1
        t1_for_options, closest_t2_conc = get_closest_concentration_to_target(
            t2_valid_concentrations_ag, t2_valid_concentrations_salt, 
            params_t1, target_t1, target_datatype="t1__s")
        # print(t1_for_options, closest_t2_conc)

        # If neither the T1 nor the T2 search came out with anything, it means it's out of the scope for
        # both. Assing [0, 0]
        if (len(closest_t1_conc) == 0) and (len(closest_t2_conc) == 0):
            print("ASSIGNING ZERO CONCENTRATION FOR all components")
            valid_concentrations = [[0, 0]]  # 0 for ag and 0 for other component
        else:
            valid_concentrations = [closest_t1_conc, closest_t2_conc]
        sample_concentrations = valid_concentrations

    # Get T1 and T2 for the concentrations that are left
    t1_t2_for_concentrations = []
    for concentrations in sample_concentrations:
        agarose_concentration = np.max([0, concentrations[0]])
        salt_concentration = np.max([0, concentrations[1]])
        t1_model_output_samp = get_mixing_model(params_t1, agarose_concentration, salt_concentration, datatype="t1__s")
        t2_model_output_samp = get_mixing_model(params_t2, agarose_concentration, salt_concentration, datatype="t2_1__s")
        t1_t2_for_concentrations.append([np.round(t1_model_output_samp, decimals=3), np.round(t2_model_output_samp, decimals=3)])

    # Round conentrations to 3 decimals
    sample_concentrations = np.round(sample_concentrations, decimals=3)
        
    return sample_concentrations, t1_t2_for_concentrations

