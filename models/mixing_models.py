import sympy


def get_mixing_model(params, agarose_concentration, other_concentration, datatype):
    a1 = params["a1"].value
    param_ag_1 = params["param_ag_1"].value
    param_oth_1 = params["param_oth_1"].value
    param_mix_1 = params["param_mix_1"].value
    param_ag_2 = params["param_ag_2"].value
    param_oth_2 = params["param_oth_2"].value
    param_mix_2 = params["param_mix_2"].value
    param_mix_3 = params["param_mix_3"].value
    param_mix_4 = params["param_mix_4"].value

    if datatype == "t1__s":
        model = a1 + (param_ag_1 * agarose_concentration) + (
                param_oth_1 * other_concentration) + (
                        param_mix_1 * agarose_concentration * other_concentration) + (
                        param_ag_2 * agarose_concentration ** 2) + (
                        param_oth_2 * other_concentration ** 2) + (
                        param_mix_2 * other_concentration * (agarose_concentration ** 2)) + (
                        param_mix_3 * agarose_concentration * (other_concentration ** 2)) + (
                        param_mix_4 * (agarose_concentration ** 2) * (other_concentration ** 2))
    elif datatype == "t2_1__s":
        model = a1 + (param_ag_1 * agarose_concentration) + (
                param_oth_1 * other_concentration) + (
                        param_mix_1 * agarose_concentration * other_concentration) + (
                        param_ag_2 * agarose_concentration ** 2) + (
                        param_oth_2 * other_concentration ** 2) + (
                        param_mix_2 * other_concentration * (agarose_concentration ** 2)) + (
                        param_mix_3 * agarose_concentration * (other_concentration ** 2)) + (
                        param_mix_4 * (agarose_concentration ** 2) * (other_concentration ** 2))
    else:
        raise Exception(f"Unknown datatype: {datatype}")

    model = 1 / model  # Invert R1 to get T1

    return model


def get_mixing_model_equation(params, agarose_concentration, other_concentration, target_value, datatype):
    model_eq = get_mixing_model(params, agarose_concentration, other_concentration, datatype)
    eq1 = sympy.Eq(model_eq, target_value)

    return eq1


def get_mixing_model_quadratic_params(params, tissue_target, conc_type):
    if conc_type == "agarose":
        c = params["a1"].value - (1 / tissue_target)
        b = params["param_ag_1"].value
        a = params["param_ag_2"].value
    elif conc_type == "salt":
        c = params["a1"].value - (1 / tissue_target)
        b = params["param_oth_1"].value
        a = params["param_oth_2"].value
    else:
        raise Exception(f"Unknown conc type {conc_type}")
    return a, b, c

