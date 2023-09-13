import lmfit


def get_lmfit_params_from_df(params_df, params_to_find=None):
    params = lmfit.Parameters()
    param_names = params_df.columns
    for param_name in param_names:
        params.add(param_name, params_df[param_name].values[0], vary=False)

    if params_to_find is not None:
        validate_params(params, params_to_find)
    return params


def validate_params(params, params_to_find):
    for param_name in params:
        if param_name in params_to_find:
            params_to_find.pop(params_to_find.index(param_name))
    assert len(params_to_find) == 0, f"Missing parameters for lmfit model: {params_to_find}"