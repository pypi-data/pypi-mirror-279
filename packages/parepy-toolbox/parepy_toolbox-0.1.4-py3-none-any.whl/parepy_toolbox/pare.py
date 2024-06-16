"""Parepy toolbox: Probabilistic Approach Reliability Engineering"""
import time
from datetime import datetime
from multiprocessing import Pool

import numpy as np
import pandas as pd

import parepy_toolbox.common_library as parepyco


def sampling_algorithm_structural_analysis(setup):
    """
    This function creates the samples and evaluates the limit state functions in structural reliability problems.

    Args:
        setup (dict): Setup settings.
        'number of samples' (Integer): Number of samples (key in setup dictionary)
        'dimension' (Integer): Number of dimensions (key in setup dictionary)
        'numerical model' (Dictionary): Numerical model settings (key in setup dictionary)
        'variables settings' (List): Variables settings (key in setup dictionary)
        'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints  
        'none_variable' (None, list, float, dictionary, str or any): None variable. Default is None. User can use this variable in objective function (key in setup dictionary)           
        'objective function' (Python function [def]): Objective function. The Parepy user defined this function (key in setup dictionary)
        'type process' (String): Type process. Options: 'auto', 'parallel' or 'serial' (key in setup dictionary)
        'name simulation' (String): Output filename (key in setup dictionary)
    
    Returns:    
        results_about_data (Dataframe): Results about reliability analysis
        failure_prob_list (List): Failure probability list
        beta_list (List): Beta list
    """

    try:
        if not isinstance(setup, dict):
            raise TypeError('The setup parameter must be a dictionary.')

        # Keys verification
        for key in setup.keys():
            if key not in ['objective function', 'number of samples', 'number of dimensions', 'numerical model', 'variables settings', 'number of state limit functions or constraints', 'none variable', 'type process', 'name simulation']:
                raise ValueError('The setup parameter must have the following keys:\n- objective function;\n- number of samples;\n- number of dimensions;\n- numerical model;\n- variables settings;\n- number of state limit functions or constraints;\n- none variable;\n - type process;\n- name simulation.') 

        # Objective function verification
        if not callable(setup['objective function']):
            raise TypeError('The objective function parameter must be a function (def).')

        # Number of samples verification
        if not isinstance(setup['number of samples'], int):
            raise TypeError('The Number of samples parameter must be an integer.')

        # Dimension verification
        if not isinstance(setup['number of dimensions'], int):
            raise TypeError('The Dimension parameter must be an integer.')

        # Numerical model verification
        if not isinstance(setup['numerical model'], dict):
            raise TypeError('The Numerical model parameter must be a dictionary.')

        # Variables settings verification
        if not isinstance(setup['variables settings'], list):
            raise TypeError('The Variables settings parameter must be a list.')

        # Number of state limit functions or constraints verification
        if not isinstance(setup['number of state limit functions or constraints'], int):
            raise TypeError('The Number of state limit functions or constraints parameter must be an integer.')

        # General settings
        initial_time = time.time()
        obj = setup['objective function']
        n_samples = setup['number of samples']
        n_dimensions = setup['number of dimensions']
        variables_settings = setup['variables settings']
        n_constraints = setup['number of state limit functions or constraints']
        none_variable = setup['none variable']
        type_process = setup['type process']
        name_simulation = setup['name simulation']

        # Algorithm settings
        model = setup['numerical model']
        algorithm = model['model sampling']
        if algorithm.upper() == 'MCS-TIME':
            time_analysis = model['time steps']
        else:
            pass

        # Creating samples
        dataset_x = parepyco.sampling(n_samples=n_samples,
                                        d=n_dimensions,
                                        model=model,
                                        variables_setup=variables_settings)

        # Starting variables
        capacity = np.zeros((len(dataset_x), n_constraints))
        demand = np.zeros((len(dataset_x), n_constraints))
        state_limit = np.zeros((len(dataset_x), n_constraints))
        indicator_function = np.zeros((len(dataset_x), n_constraints))

        # Selecting type process
        if type_process.upper() == 'AUTO':
            type_process, _ = type_process_run(dataset_x, obj, none_variable, n_constraints)

        # Multiprocess Objective Function evaluation
        if type_process.upper() == 'PARALLEL':
            parts = np.array_split(dataset_x, 1000)
            tam = []
            for k in range(len(parts)):
                tam.append(len(parts[k]))
            information_model = [[i, obj, none_variable] for i in parts]
            with Pool() as p:
                result = p.map_async(func=parepyco.evaluation_model_parallel, iterable=information_model)
                result = result.get()
            cont = 0
            for i in range(len(parts)):
                for j in range(tam[i]):
                    capacity[cont, :] = result[i][0][j].copy()
                    demand[cont, :] = result[i][1][j].copy()
                    state_limit[cont, :] = result[i][2][j].copy()
                    indicator_function[cont, :] = [0 if value <= 0 else 1 for value in result[i][2][j]]
                    cont += 1
        # Singleprocess Objective Function evaluation
        elif type_process.upper() == 'SERIAL':
            for id, sample in enumerate(dataset_x):
                sample_id = sample.copy()
                information_model = [sample_id, obj, none_variable]
                capacity_i, demand_i, state_limit_i = parepyco.evaluation_model(information_model)
                capacity[id, :] = capacity_i.copy()
                demand[id, :] = demand_i.copy()
                state_limit[id, :] = state_limit_i.copy()
                indicator_function[id, :] = [0 if value <= 0 else 1 for value in state_limit_i]

        # Storage all results (horizontal stacking)
        results = np.hstack((dataset_x, capacity, demand, state_limit, indicator_function))

        # Transforming time results in dataframe X_i T_i R_i S_i G_i I_i
        if algorithm.upper() == 'MCS-TIME' or  \
                        algorithm.upper() == 'MCS_TIME' or \
                        algorithm.upper() == 'MCS TIME':
            tam = int(len(results) / n_samples)
            line_i = 0
            line_j = tam
            result_all = []
            for i in range(n_samples):
                i_sample_in_temp = results[line_i:line_j, :]
                i_sample_in_temp = i_sample_in_temp.T
                line_i += tam
                line_j += tam
                i_sample_in_temp = i_sample_in_temp.flatten().tolist()
                result_all.append(i_sample_in_temp)
            results_about_data = pd.DataFrame(result_all)
        else:
            results_about_data = pd.DataFrame(results)

        # Rename columns in dataframe
        column_names = []
        for i in range(n_dimensions):
            if algorithm.upper() == 'MCS-TIME' or  \
                                        algorithm.upper() == 'MCS_TIME' or \
                                        algorithm.upper() == 'MCS TIME':
                for j in range(time_analysis):
                    column_names.append('X_' + str(i) + '_t=' + str(j))
            else:
                column_names.append('X_' + str(i))
        if algorithm.upper() == 'MCS-TIME' or \
                                        algorithm.upper() == 'MCS_TIME' or \
                                        algorithm.upper() == 'MCS TIME':
            for i in range(time_analysis):
                column_names.append('STEP_t_' + str(i))
        for i in range(n_constraints):
            if algorithm.upper() == 'MCS-TIME' or \
                                        algorithm.upper() == 'MCS_TIME' or \
                                        algorithm.upper() == 'MCS TIME':
                for j in range(time_analysis):
                    column_names.append('R_' + str(i) + '_t=' + str(j))
            else:
                column_names.append('R_' + str(i))
        for i in range(n_constraints):
            if algorithm.upper() == 'MCS-TIME' or \
                                        algorithm.upper() == 'MCS_TIME' or \
                                        algorithm.upper() == 'MCS TIME':
                for j in range(time_analysis):
                    column_names.append('S_' + str(i) + '_t=' + str(j))
            else:
                column_names.append('S_' + str(i))
        for i in range(n_constraints):
            if algorithm.upper() == 'MCS-TIME' or \
                                        algorithm.upper() == 'MCS_TIME' or \
                                        algorithm.upper() == 'MCS TIME':
                for j in range(time_analysis):
                    column_names.append('G_' + str(i) + '_t=' + str(j))
            else:
                column_names.append('G_' + str(i)) 
        for i in range(n_constraints):
            if algorithm.upper() == 'MCS-TIME' or \
                                        algorithm.upper() == 'MCS_TIME' or \
                                        algorithm.upper() == 'MCS TIME':
                for j in range(time_analysis):
                    column_names.append('I_' + str(i) + '_t=' + str(j))
            else:
                column_names.append('I_' + str(i))
        results_about_data.columns = column_names

        # First Barrier Failure (FBF)
        if algorithm.upper() == 'MCS-TIME' or \
                                        algorithm.upper() == 'MCS_TIME' or \
                                        algorithm.upper() == 'MCS TIME':
            i_columns = []
            for i in range(n_constraints):
                aux_column_names = []
                for j in range(time_analysis):
                    aux_column_names.append('I_' + str(i) + '_t=' + str(j))
                i_columns.append(aux_column_names)

            for i in i_columns:
                matrixx = results_about_data[i].values
                for id, linha in enumerate(matrixx):
                    indice_primeiro_1 = np.argmax(linha == 1)
                    if linha[indice_primeiro_1] == 1:
                        matrixx[id, indice_primeiro_1:] = 1
                results_about_data = pd.concat([results_about_data.drop(columns=i),
                                                pd.DataFrame(matrixx, columns=i)], axis=1)
        else:
            i_columns = []
            for i in range(n_constraints):
                i_columns.append(['I_' + str(i)])

        # Probability of failure and beta index
        failure_prob_list = []
        beta_list = []

        for indicator_function_time_step_i in i_columns:
            pf_time = []
            beta_time = []
            for j in indicator_function_time_step_i:
                n_failure = results_about_data[j].sum()
                pf_value = n_failure / n_samples
                beta_value = parepyco.beta_equation(pf_value)
                pf_time.append(pf_value)
                beta_time.append(beta_value)
            failure_prob_list.append(pf_time)
            beta_list.append(beta_time)

        # Save results in .txt file
        file_name = str(datetime.now().strftime('%Y%m%d-%H%M%S'))
        file_name_txt = name_simulation + '_' + algorithm.upper() + '_' + file_name + ".txt"
        parepyco.export_to_txt(results_about_data, file_name_txt)
        end_time = time.time()
        processing_time = end_time - initial_time

        # Report in command window
        print("PARE^py Report: \n")
        print(f"- Output file name: {file_name_txt}")
        print(f"- Processing time (s): {processing_time}  ({type_process} kernel)")

        return results_about_data, failure_prob_list, beta_list

    except TypeError as te:
        print(f'Error: {te}')

    except ValueError as ve:
        print(f'Error: {ve}')

    return None, None, None


def concatenates_txt_files_sampling_algorithm_01(files_path, n_constraints, model, name_simulation):

    # set the model
    algorithm = model['model sampling']
    time_analysis = model['time steps']

    # Start time
    initial_time = time.time()

    # Read txt files and concatenate
    results_about_data = pd.DataFrame()
    for txt_file in files_path:
        temp_df = pd.read_csv(txt_file, delimiter='\t')
        results_about_data = pd.concat([results_about_data, temp_df], ignore_index=True)
    n_samples = results_about_data.shape[0]

    if algorithm.upper() == 'MCS-TIME' or \
                                    algorithm.upper() == 'MCS_TIME' or \
                                    algorithm.upper() == 'MCS TIME':
        i_columns = []
        for i in range(n_constraints):
            aux_column_names = []
            for j in range(time_analysis):
                aux_column_names.append('I_' + str(i) + '_t=' + str(j))
            i_columns.append(aux_column_names)
    else:
        i_columns = []
        for i in range(n_constraints):
            i_columns.append(['I_' + str(i)])

    # Probability of failure and beta index
    failure_prob_list = []
    beta_list = []

    for indicator_function_time_step_i in i_columns:
        pf_time = []
        beta_time = []
        for j in indicator_function_time_step_i:
            n_failure = results_about_data[j].sum()
            pf_value = n_failure / n_samples
            beta_value = parepyco.beta_equation(pf_value)
            pf_time.append(pf_value)
            beta_time.append(beta_value)
        failure_prob_list.append(pf_time)
        beta_list.append(beta_time)

    # Save results in .txt file
    file_name = str(datetime.now().strftime('%Y%m%d-%H%M%S'))
    file_name_txt = name_simulation + '_' + algorithm.upper() + '_' + file_name + ".txt"
    parepyco.export_to_txt(results_about_data, file_name_txt)
    end_time = time.time()
    processing_time = end_time - initial_time

    # Report in command window
    print("PARE^py Report: \n")
    print(f"- Output file name: {file_name_txt}")
    print(f"- Processing time (s): {processing_time}")

    return results_about_data, failure_prob_list, beta_list


def type_process_run(dataset, obj, none_variable, n_constraints):
    """
    This function selects the best process (parallel or serial) to run the algorithm.

    Args:
        dataset (np.array): Sampling dataset.
        objective function (Python function [def]): Objective function. The Parepy user defined this function.
        none_variable (None, list, float, dictionary, str or any): None variable. 
                                                                    User can use this variable in objective function
        n_constraints (Integer): Number of state limit functions or constraints.
    
    returns:
        type_process (String): Best type process.
        elapsed_time (Float): Elapsed time.
    """

    # Selecting a sample to test
    dataset_x = dataset[:10000]

    # Parallel test
    start_time_parallel = time.perf_counter()
    parts = np.array_split(dataset_x, 1000)
    tam = []
    for k in range(len(parts)):
        tam.append(len(parts[k]))
    capacity = np.zeros((len(dataset_x), n_constraints))
    demand = np.zeros((len(dataset_x), n_constraints))
    state_limit = np.zeros((len(dataset_x), n_constraints))
    indicator_function = np.zeros((len(dataset_x), n_constraints))
    information_model = [[i, obj, none_variable] for i in parts]
    with Pool() as p:
        result = p.map_async(func=parepyco.evaluation_model_parallel, iterable=information_model)
        result = result.get()
    cont = 0
    for i in range(len(parts)):
        for j in range(tam[i]):
            capacity[cont, :] = result[i][0][j].copy()
            demand[cont, :] = result[i][1][j].copy()
            state_limit[cont, :] = result[i][2][j].copy()
            indicator_function[cont, :] = [0 if value <= 0 else 1 for value in result[i][2][j]]
            cont += 1
    _ = np.hstack((dataset_x, capacity, demand, state_limit, indicator_function))
    end_time_parallel = time.perf_counter()
    elapsed_time_parallel = end_time_parallel - start_time_parallel

    # Serial test
    start_time_serial = time.perf_counter()
    capacity = np.zeros((len(dataset_x), n_constraints))
    demand = np.zeros((len(dataset_x), n_constraints))
    state_limit = np.zeros((len(dataset_x), n_constraints))
    indicator_function = np.zeros((len(dataset_x), n_constraints))
    for id, sample in enumerate(dataset_x):
        sample_id = sample.copy()
        information_model = [sample_id, obj, none_variable]
        capacity_i, demand_i, state_limit_i = parepyco.evaluation_model(information_model)
        capacity[id, :] = capacity_i.copy()
        demand[id, :] = demand_i.copy()
        state_limit[id, :] = state_limit_i.copy()
        indicator_function[id, :] = [0 if value <= 0 else 1 for value in state_limit_i]
    _ = np.hstack((dataset_x, capacity, demand, state_limit, indicator_function))
    end_time_serial = time.perf_counter()
    elapsed_time_serial = end_time_serial - start_time_serial

    if elapsed_time_parallel < elapsed_time_serial:
        type_process = 'parallel'
        elapsed_time = elapsed_time_parallel
    else:
        type_process = 'serial'
        elapsed_time = elapsed_time_serial

    return type_process, elapsed_time