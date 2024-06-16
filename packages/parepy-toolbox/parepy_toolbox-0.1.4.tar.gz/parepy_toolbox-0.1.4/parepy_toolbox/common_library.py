"""Common library for PARE^py toolbox"""
from scipy.stats.distributions import norm
from scipy.stats.distributions import gumbel_r
from scipy.stats.distributions import gumbel_l
from scipy.stats.distributions import dweibull
from scipy.stats.distributions import gamma
from scipy.stats.distributions import beta
from scipy.stats.distributions import triang
import numpy as np
import pandas as pd
from numpy import sqrt, pi, exp


def sampling(n_samples, d, model, variables_setup):
    """
    This algorithm generates a set of random numbers according to a type of distribution.

    Args:
        n_samples (Integer): Number of samples.
        d (Integer): Number of dimensions.
        model (Dictionary): Model parameters.
        variables_setup (List): Random variable parameters (list of dictionary format). See the example.
    
    Returns:
        random_sampling (np.array): Random samples.
    """

    # Model settnigs
    model_sampling = model['model sampling'].upper()

    if model_sampling == 'MCS TIME' or model_sampling == 'MCS-TIME' or model_sampling == 'MCS_TIME':
        # Time analysis
        time_analysis = model['time steps']

        # Generating n_samples samples
        random_sampling = np.empty((0, d))
        for _ in range(n_samples):

            # Generating a temporal sample
            temporal_sampling = np.zeros((time_analysis, d))
            for i in range(d):

                # Setup pdf
                type_dist = variables_setup[i]['type'].upper()
                seed_dist = variables_setup[i]['seed']
                n_samples_in_temporal_aux = variables_setup[i]['stochastic variable']
                if n_samples_in_temporal_aux:
                    n_samples_in_temporal = time_analysis
                else:
                    n_samples_in_temporal = 1
                
                # Normal or Gaussian
                if type_dist == 'GAUSSIAN' or type_dist == 'NORMAL':
                    mean_dist = variables_setup[i]['loc']
                    stda_dist = variables_setup[i]['scale']
                    temporal_sampling[:, i] = norm.rvs(loc=mean_dist,
                                                       scale=stda_dist,
                                                       size=n_samples_in_temporal,
                                                       random_state=seed_dist)
                # Gumbel right or Gumbel maximum
                elif type_dist == 'GUMBEL MAX':
                    mean_dist = variables_setup[i]['loc']
                    stda_dist = variables_setup[i]['scale']
                    temporal_sampling[:, i] = gumbel_r.rvs(loc=mean_dist,
                                                           scale=stda_dist,
                                                           size=n_samples_in_temporal,
                                                           random_state=seed_dist)
                # Gumbel left or Gumbel minimum
                elif type_dist == 'GUMBEL MIN':
                    mean_dist = variables_setup[i]['loc']
                    stda_dist = variables_setup[i]['scale']
                    temporal_sampling[:, i] = gumbel_l.rvs(loc=mean_dist,
                                                           scale=stda_dist,
                                                           size=n_samples_in_temporal,
                                                           random_state=seed_dist)
                # Weibull
                elif type_dist == 'WEIBULL':
                    shape_dist = variables_setup[i]['shape']
                    mean_dist = variables_setup[i]['loc']
                    stda_dist = variables_setup[i]['scale']
                    temporal_sampling[:, i] = dweibull.rvs(shape_dist,
                                                           loc=mean_dist,
                                                           scale=stda_dist,
                                                           size=n_samples_in_temporal,
                                                           random_state=seed_dist)
                # Lognormal
                elif type_dist == 'LOGNORMAL':
                    # https://shivamrana.me/2024/01/lognormal-to-normal/
                    mean_dist = variables_setup[i]['loc']
                    stda_dist = variables_setup[i]['scale']
                    rng = np.random.default_rng()
                    lognorm_samples = rng.lognormal(mean_dist,
                                                    stda_dist,
                                                    n_samples_in_temporal)
                    norm_samples = np.log(lognorm_samples)
                    temporal_sampling[:, i] = norm.rvs(loc=norm_samples.mean(),
                                                       scale=norm_samples.std(),
                                                       size=n_samples_in_temporal,
                                                       random_state=seed_dist)
                # Gamma
                elif type_dist == 'GAMMA':
                    shape_dist = variables_setup[i]['shape']
                    mean_dist = variables_setup[i]['loc']
                    stda_dist = variables_setup[i]['scale']
                    temporal_sampling[:, i] = gamma.rvs(shape_dist,
                                                        loc=mean_dist,
                                                        scale=stda_dist,
                                                        size=n_samples_in_temporal,
                                                        random_state=seed_dist)
                # Beta
                elif type_dist == 'BETA':
                    a = variables_setup[i]['a']
                    b = variables_setup[i]['b']
                    mean_dist = variables_setup[i]['loc']
                    stda_dist = variables_setup[i]['scale']
                    temporal_sampling[:, i] = beta.rvs(a,
                                                        b,
                                                        loc=mean_dist,
                                                        scale=stda_dist,
                                                        size=n_samples_in_temporal,
                                                        random_state=seed_dist)
                # Triangular
                elif type_dist == 'TRIANGULAR':
                    loc = variables_setup[i]['loc']
                    a = variables_setup[i]['min']
                    b = variables_setup[i]['max']
                    std = b - a
                    c = (loc - a) / (b - a)
                    temporal_sampling[:, i] = triang.rvs(c=c,
                                                        loc=a,
                                                        scale=std,
                                                        size=n_samples_in_temporal,
                                                        random_state=seed_dist)
            random_sampling = np.concatenate((random_sampling, temporal_sampling), axis=0)

        # convert time dataset
        time_sampling = np.zeros((time_analysis * n_samples, 1))
        cont = 0
        for _ in range(n_samples):
            for m in range(time_analysis):
                time_sampling[cont, 0] = int(m)
                cont += 1
        random_sampling = np.concatenate((random_sampling, time_sampling), axis=1)

    elif model_sampling == 'MCS' or model_sampling == 'CRUDE MONTE CARLO':
        random_sampling = np.zeros((n_samples, d))
        
        for j in range(d):
            # Setup pdf
            type_dist = variables_setup[j]['type'].upper()
            seed_dist = variables_setup[j]['seed']

            # Normal or Gaussian
            if type_dist == 'GAUSSIAN' or type_dist == 'NORMAL':
                mean_dist = variables_setup[j]['loc']
                stda_dist = variables_setup[j]['scale']
                random_sampling[:, j] = norm.rvs(loc=mean_dist,
                                                    scale=stda_dist,
                                                    size=n_samples,
                                                    random_state=seed_dist)
            # Gumbel right or Gumbel maximum
            elif type_dist == 'GUMBEL MAX':
                mean_dist = variables_setup[j]['loc']
                stda_dist = variables_setup[j]['scale']
                random_sampling[:, j] = gumbel_r.rvs(loc=mean_dist,
                                                        scale=stda_dist,
                                                        size=n_samples,
                                                        random_state=seed_dist)
            # Gumbel left or Gumbel minimum
            elif type_dist == 'GUMBEL MIN':
                mean_dist = variables_setup[j]['loc']
                stda_dist = variables_setup[j]['scale']
                random_sampling[:, j] = gumbel_l.rvs(loc=mean_dist,
                                                     scale=stda_dist,
                                                     size=n_samples,
                                                     random_state=seed_dist)
            # Weibull
            elif type_dist == 'WEIBULL':
                shape_dist = variables_setup[j]['shape']
                mean_dist = variables_setup[j]['loc']
                stda_dist = variables_setup[j]['scale']
                random_sampling[:, j] = dweibull.rvs(shape_dist,
                                                        loc=mean_dist,
                                                        scale=stda_dist,
                                                        size=n_samples,
                                                        random_state=seed_dist)
            # Lognormal
            elif type_dist == 'LOGNORMAL':
                # https://shivamrana.me/2024/01/lognormal-to-normal/
                mean_dist = variables_setup[j]['loc']
                stda_dist = variables_setup[j]['scale']
                rng = np.random.default_rng()
                lognorm_samples = rng.lognormal(mean_dist, stda_dist, n_samples)
                norm_samples = np.log(lognorm_samples)
                random_sampling[:, j] = norm.rvs(loc=norm_samples.mean(),
                                                    scale=norm_samples.std(),
                                                    size=n_samples,
                                                    random_state=seed_dist)
            # Gamma
            elif type_dist == 'GAMMA':
                shape_dist = variables_setup[j]['shape']
                mean_dist = variables_setup[j]['loc']
                stda_dist = variables_setup[j]['scale']
                random_sampling[:, j] = gamma.rvs(shape_dist,
                                                    loc=mean_dist,
                                                    scale=stda_dist,
                                                    size=n_samples,
                                                    random_state=seed_dist)
            # Beta
            elif type_dist == 'BETA':
                mean_dist = variables_setup[i]['loc']
                stda_dist = variables_setup[i]['scale']
                a = variables_setup[i]['a']
                b = variables_setup[i]['b']
                random_sampling[:, j] = beta.rvs(a,
                                                    b,
                                                    loc=mean_dist,
                                                    scale=stda_dist,
                                                    size=n_samples,
                                                    random_state=seed_dist)
            # Triangular
            elif type_dist == 'TRIANGULAR':
                loc = variables_setup[j]['loc']
                a = variables_setup[j]['min']
                b = variables_setup[j]['max']
                std = b - a
                c = (loc - a) / (b - a)
                random_sampling[:, j] = triang.rvs(c=c,
                                                   loc=a,
                                                   scale=std,
                                                   size=n_samples,
                                                   random_state=seed_dist)

    return random_sampling


def evaluation_model_parallel(modeling_info):
    """
    This function evaluates the limit state functions.

    Args:
        modeling_info (List): List with information for modeling.
            [0] i_sample (List or np.array): i sample of the 
                random sampling generated in the function sampling.
            [1] objective function (Python function [def]): Objective function. The Parepy user defined this function.
            [2] none_variable (None, list, float, dictionary, str or any): None variable. Default is None. 
                                                                            User can use this variable in objective function 
    
    Returns:
        capacity_i_sample (List): Capacity values.
        demand_i_sample (List): Demand values.
        state_limit_function_i_sample (List): State limit function values.
    """

    # Evaluation of the limit state functions
    i_sample = modeling_info[0]
    obj = modeling_info[1]
    none_variable = modeling_info[2]
    capacity_i_sample = []
    demand_i_sample = []
    state_limit_function_i_sample = []
    for i in i_sample:
        capacity_i_aux, demand_i_aux, state_limit_function_i_aux = obj(list(i), none_variable)
        capacity_i_sample.append(capacity_i_aux)
        demand_i_sample.append(demand_i_aux)
        state_limit_function_i_sample.append(state_limit_function_i_aux)

    return capacity_i_sample, demand_i_sample, state_limit_function_i_sample


def evaluation_model(modeling_info):
    """
    This function evaluates the limit state functions.

    Args:
        modeling_info (List): List with information for modeling.
            [0] i_sample (List or np.array): i sample of the 
                random sampling generated in the function sampling.
            [1] objective function (Python function [def]): Objective function. The Parepy user defined this function.
            [2] none_variable (None, list, float, dictionary, str or any): None variable. Default is None. 
                                                                            User can use this variable in objective function 
    
    Returns:
        capacity_i_sample (List): Capacity values.
        demand_i_sample (List): Demand values.
        state_limit_function_i_sample (List): State limit function values.
    """

    # Evaluation of the limit state functions
    i_sample = modeling_info[0]
    obj = modeling_info[1]
    none_variable = modeling_info[2]
    capacity_i_sample, demand_i_sample, state_limit_function_i_sample = obj(i_sample, none_variable)

    return capacity_i_sample, demand_i_sample, state_limit_function_i_sample


def newton_raphson(f, df, x0, tol):
    """
    This function calculates the root of a function using the Newton-Raphson method.

    Args:
        f (Python function [def]): Function.
        df (Python function [def]): Derivative of the function.
        x0 (Float): Initial value.
        tol (Float): Tolerance.
    
    Returns:
        x0 (Float): Root of the function.
    """

    if abs(f(x0)) < tol:
        return x0
    else:
        return newton_raphson(f, df, x0 - f(x0)/df(x0), tol)


def beta_equation(pf):
    """
    This function calculates the beta value for a given probability of failure.

    Args:
        pf (Float): Probability of failure.
    
    Returns:
        beta_value (Float): Beta value.
    """

    if pf > 0.5:
        beta_value = "minus infinity"
    else:
        F = lambda BETA: BETA*(0.00569689925051199*sqrt(2)*exp(-0.497780952459929*BETA**2)/sqrt(pi) + 0.0131774933075162*sqrt(2)*exp(-0.488400032299965*BETA**2)/sqrt(pi) + 0.0204695783506533*sqrt(2)*exp(-0.471893773055302*BETA**2)/sqrt(pi) + 0.0274523479879179*sqrt(2)*exp(-0.448874334002837*BETA**2)/sqrt(pi) + 0.0340191669061785*sqrt(2)*exp(-0.42018898411968*BETA**2)/sqrt(pi) + 0.0400703501675005*sqrt(2)*exp(-0.386874144322843*BETA**2)/sqrt(pi) + 0.045514130991482*sqrt(2)*exp(-0.350103048710684*BETA**2)/sqrt(pi) + 0.0502679745335254*sqrt(2)*exp(-0.311127540182165*BETA**2)/sqrt(pi) + 0.0542598122371319*sqrt(2)*exp(-0.271217130855817*BETA**2)/sqrt(pi) + 0.0574291295728559*sqrt(2)*exp(-0.231598755762806*BETA**2)/sqrt(pi) + 0.0597278817678925*sqrt(2)*exp(-0.19340060305222*BETA**2)/sqrt(pi) + 0.0611212214951551*sqrt(2)*exp(-0.157603139738968*BETA**2)/sqrt(pi) + 0.0615880268633578*sqrt(2)*exp(-0.125*BETA**2)/sqrt(pi) + 0.0611212214951551*sqrt(2)*exp(-0.0961707934336129*BETA**2)/sqrt(pi) + 0.0597278817678925*sqrt(2)*exp(-0.0714671611917261*BETA**2)/sqrt(pi) + 0.0574291295728559*sqrt(2)*exp(-0.0510126028581118*BETA**2)/sqrt(pi) + 0.0542598122371319*sqrt(2)*exp(-0.0347157651329596*BETA**2)/sqrt(pi) + 0.0502679745335254*sqrt(2)*exp(-0.0222960750615538*BETA**2)/sqrt(pi) + 0.045514130991482*sqrt(2)*exp(-0.0133198644739499*BETA**2)/sqrt(pi) + 0.0400703501675005*sqrt(2)*exp(-0.00724451280416452*BETA**2)/sqrt(pi) + 0.0340191669061785*sqrt(2)*exp(-0.00346766973926267*BETA**2)/sqrt(pi) + 0.0274523479879179*sqrt(2)*exp(-0.00137833506369952*BETA**2)/sqrt(pi) + 0.0204695783506533*sqrt(2)*exp(-0.000406487440814915*BETA**2)/sqrt(pi) + 0.0131774933075162*sqrt(2)*exp(-6.80715702059458e-5*BETA**2)/sqrt(pi) + 0.00569689925051199*sqrt(2)*exp(-2.46756468031828e-6*BETA**2)/sqrt(pi))/2 + pf - 0.5
        F_PRIME = lambda BETA: BETA*(-0.00567161586997623*sqrt(2)*BETA*exp(-0.497780952459929*BETA**2)/sqrt(pi) - 0.0128717763140469*sqrt(2)*BETA*exp(-0.488400032299965*BETA**2)/sqrt(pi) - 0.0193189331214818*sqrt(2)*BETA*exp(-0.471893773055302*BETA**2)/sqrt(pi) - 0.0246453088397815*sqrt(2)*BETA*exp(-0.448874334002837*BETA**2)/sqrt(pi) - 0.0285889583658099*sqrt(2)*BETA*exp(-0.42018898411968*BETA**2)/sqrt(pi) - 0.0310043648675369*sqrt(2)*BETA*exp(-0.386874144322843*BETA**2)/sqrt(pi) - 0.0318692720390705*sqrt(2)*BETA*exp(-0.350103048710684*BETA**2)/sqrt(pi) - 0.031279502533111*sqrt(2)*BETA*exp(-0.311127540182165*BETA**2)/sqrt(pi) - 0.0294323811914605*sqrt(2)*BETA*exp(-0.271217130855817*BETA**2)/sqrt(pi) - 0.0266010299072288*sqrt(2)*BETA*exp(-0.231598755762806*BETA**2)/sqrt(pi) - 0.0231028167058843*sqrt(2)*BETA*exp(-0.19340060305222*BETA**2)/sqrt(pi) - 0.0192657928246347*sqrt(2)*BETA*exp(-0.157603139738968*BETA**2)/sqrt(pi) - 0.0153970067158395*sqrt(2)*BETA*exp(-0.125*BETA**2)/sqrt(pi) - 0.0117561527336413*sqrt(2)*BETA*exp(-0.0961707934336129*BETA**2)/sqrt(pi) - 0.00853716430789267*sqrt(2)*BETA*exp(-0.0714671611917261*BETA**2)/sqrt(pi) - 0.00585921875877428*sqrt(2)*BETA*exp(-0.0510126028581118*BETA**2)/sqrt(pi) - 0.00376734179556552*sqrt(2)*BETA*exp(-0.0347157651329596*BETA**2)/sqrt(pi) - 0.00224155706678351*sqrt(2)*BETA*exp(-0.0222960750615538*BETA**2)/sqrt(pi) - 0.00121248411291229*sqrt(2)*BETA*exp(-0.0133198644739499*BETA**2)/sqrt(pi) - 0.000580580329711626*sqrt(2)*BETA*exp(-0.00724451280416452*BETA**2)/sqrt(pi) - 0.000235934471270962*sqrt(2)*BETA*exp(-0.00346766973926267*BETA**2)/sqrt(pi) - 7.56770676252561e-5*sqrt(2)*BETA*exp(-0.00137833506369952*BETA**2)/sqrt(pi) - 1.66412530366349e-5*sqrt(2)*BETA*exp(-0.000406487440814915*BETA**2)/sqrt(pi) - 1.79402532164194e-6*sqrt(2)*BETA*exp(-6.80715702059458e-5*BETA**2)/sqrt(pi) - 2.81149347557902e-8*sqrt(2)*BETA*exp(-2.46756468031828e-6*BETA**2)/sqrt(pi))/2 + 0.002848449625256*sqrt(2)*exp(-0.497780952459929*BETA**2)/sqrt(pi) + 0.00658874665375808*sqrt(2)*exp(-0.488400032299965*BETA**2)/sqrt(pi) + 0.0102347891753266*sqrt(2)*exp(-0.471893773055302*BETA**2)/sqrt(pi) + 0.0137261739939589*sqrt(2)*exp(-0.448874334002837*BETA**2)/sqrt(pi) + 0.0170095834530893*sqrt(2)*exp(-0.42018898411968*BETA**2)/sqrt(pi) + 0.0200351750837502*sqrt(2)*exp(-0.386874144322843*BETA**2)/sqrt(pi) + 0.022757065495741*sqrt(2)*exp(-0.350103048710684*BETA**2)/sqrt(pi) + 0.0251339872667627*sqrt(2)*exp(-0.311127540182165*BETA**2)/sqrt(pi) + 0.027129906118566*sqrt(2)*exp(-0.271217130855817*BETA**2)/sqrt(pi) + 0.028714564786428*sqrt(2)*exp(-0.231598755762806*BETA**2)/sqrt(pi) + 0.0298639408839463*sqrt(2)*exp(-0.19340060305222*BETA**2)/sqrt(pi) + 0.0305606107475775*sqrt(2)*exp(-0.157603139738968*BETA**2)/sqrt(pi) + 0.0307940134316789*sqrt(2)*exp(-0.125*BETA**2)/sqrt(pi) + 0.0305606107475775*sqrt(2)*exp(-0.0961707934336129*BETA**2)/sqrt(pi) + 0.0298639408839463*sqrt(2)*exp(-0.0714671611917261*BETA**2)/sqrt(pi) + 0.028714564786428*sqrt(2)*exp(-0.0510126028581118*BETA**2)/sqrt(pi) + 0.027129906118566*sqrt(2)*exp(-0.0347157651329596*BETA**2)/sqrt(pi) + 0.0251339872667627*sqrt(2)*exp(-0.0222960750615538*BETA**2)/sqrt(pi) + 0.022757065495741*sqrt(2)*exp(-0.0133198644739499*BETA**2)/sqrt(pi) + 0.0200351750837502*sqrt(2)*exp(-0.00724451280416452*BETA**2)/sqrt(pi) + 0.0170095834530893*sqrt(2)*exp(-0.00346766973926267*BETA**2)/sqrt(pi) + 0.0137261739939589*sqrt(2)*exp(-0.00137833506369952*BETA**2)/sqrt(pi) + 0.0102347891753266*sqrt(2)*exp(-0.000406487440814915*BETA**2)/sqrt(pi) + 0.00658874665375808*sqrt(2)*exp(-6.80715702059458e-5*BETA**2)/sqrt(pi) + 0.002848449625256*sqrt(2)*exp(-2.46756468031828e-6*BETA**2)/sqrt(pi)
        beta_value = newton_raphson(F, F_PRIME, 0.0, 1E-15)

        return beta_value


def export_to_txt(df, file_name):
    """
    This function exports a DataFrame to a text file (.txt).

    Args:
        df (Dataframe): DataFrame.
        file_name (String): Name of the output file.

    Returns:
        None
    """

    df.to_csv(file_name, sep='\t', index=False)


def read_txt_to_dataframe(file_name):
    """
    Reads a text file (.txt) and returns a DataFrame.

    Args
        file_name (String): Path and name of the input file in .txt format.

    Returns:
        df (Dataframe): DataFrame created from the input file.
    """

    df = pd.read_csv(file_name, sep='\t')

    return df

"""
        # Uniform
        elif type_dist == 'UNIFORM':
            random_sampling[:, i] = uniform.rvs(loc = mean_dist, scale=stda_dist, size = n_samples, random_state = seed)
        # Triangular
        elif type_dist == 'TRIANGULAR':
            LOC = variables_settings[i][1]
            SCALE = variables_settings[i][2]
            C = variables_settings[i][3]
            #loc is the start, scale is the base width, c is the mode percentage
            random_sampling[:, i] = triang.rvs(loc = LOC, scale = SCALE, c = (C - LOC) / (SCALE - LOC), size = n_samples, random_state = seed)
        RANDOM_STATE.append(seed)

return random_sampling, RANDOM_STATE
"""
