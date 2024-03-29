

def best_to_consume1(current_energy, current_hydration, goal_energy, goal_hydration, reference_dict):
    """
    Returns the best item to consume based on the current energy and hydration levels.
    """

    #set up the re-used variables and the DP array
    energy_difference = goal_energy - current_energy
    hydration_difference = goal_hydration - current_hydration
    total_energy_rows = energy_difference + 100
    total_hydration_columns = hydration_difference + 100


    dp_arr = [[float('inf') for i in range(total_hydration_columns)] for j in range(total_energy_rows)]
    dp_arr[0][0] = 0
    dp_provisions_arr = [[[] for i in range(total_hydration_columns)] for j in range(total_energy_rows)]
    valid_start_points = [(0,0)]


    while valid_start_points:
        start_energy_row, start_hydration_column = valid_start_points.pop(0)
        #print(f"trying starting point (e,h): {start_energy_row}, {start_hydration_column}")

        if start_energy_row >= energy_difference and start_hydration_column >= hydration_difference:
            #print(f"  starting point too far, removing (e,h): {start_energy_row}, {start_hydration_column}")
            continue
        
        for name, provision_attributes in reference_dict.items():
            price, energy, hydration = provision_attributes[0], provision_attributes[1], provision_attributes[2]
        
            #print(f"  starting point valid, jumping from (e,h): {start_energy_row}, {start_hydration_column}")
            result_energy_row = start_energy_row + energy
            result_hydration_column = start_hydration_column + hydration

            #check for out of bounds/negative effects
            if result_energy_row >= total_energy_rows or result_hydration_column >= total_hydration_columns or result_energy_row < 0 or result_hydration_column < 0:
                #print(f"  provision lands out of bounds, skipping (e,h): {result_energy_row}, {result_hydration_column}. name: {name}, price: {price}, energy: {energy}, hydration: {hydration}")
                continue
            
            curr_combo_price = dp_arr[start_energy_row][start_hydration_column] + price
            if dp_arr[result_energy_row][result_hydration_column] > curr_combo_price:
                dp_arr[result_energy_row][result_hydration_column] = curr_combo_price
                curr_combo_provisions = dp_provisions_arr[start_energy_row][start_hydration_column] + [name]
                dp_provisions_arr[result_energy_row][result_hydration_column] = curr_combo_provisions

                valid_start_points.append((result_energy_row, result_hydration_column))

                for energy_row in range(0, result_energy_row):
                    for hydration_column in range(0, result_hydration_column):
                        if energy_row < start_energy_row and hydration_column < start_hydration_column:
                            continue
                        if dp_arr[energy_row][hydration_column] > curr_combo_price:
                            dp_arr[energy_row][hydration_column] = curr_combo_price
                            dp_provisions_arr[energy_row][hydration_column] = curr_combo_provisions
    print(f"starting energy: {current_energy}, starting hydration: {current_hydration}")
    print(f"target energy: {goal_energy}, target hydration: {goal_hydration}")
    print(f"need to consume {energy_difference} energy and {hydration_difference} hydration")
    print(f"minimal price price to reach the goal: {dp_arr[energy_difference][hydration_difference]}")
    print(f"achieved by: ")
    for provision_name in dp_provisions_arr[energy_difference][hydration_difference]:
        print(f"    name: {provision_name}, price: {reference_dict[provision_name][0]}, energy: {reference_dict[provision_name][1]}, hydration: {reference_dict[provision_name][2]}")
    print(f"final energy: {current_energy + sum([reference_dict[provision_name][1] for provision_name in dp_provisions_arr[energy_difference][hydration_difference]])}")
    print(f"final hydration: {current_hydration + sum([reference_dict[provision_name][2] for provision_name in dp_provisions_arr[energy_difference][hydration_difference]])}")


def best_to_consume_df(current_energy, current_hydration, goal_energy, goal_hydration, df):
    """
    Returns the best item to consume based on the current energy and hydration levels.
    """
    try:
        #set up the re-used variables and the DP array
        energy_difference = goal_energy - current_energy
        hydration_difference = goal_hydration - current_hydration
        total_energy_rows = energy_difference + 100
        total_hydration_columns = hydration_difference + 100


        dp_arr = [[float('inf') for i in range(total_hydration_columns)] for j in range(total_energy_rows)]
        dp_arr[0][0] = 0
        dp_provisions_arr = [[[] for i in range(total_hydration_columns)] for j in range(total_energy_rows)]
        valid_start_points = [(0,0)]


        while valid_start_points:
            start_energy_row, start_hydration_column = valid_start_points.pop(0)
            #print(f"trying starting point (e,h): {start_energy_row}, {start_hydration_column}")

            if start_energy_row >= energy_difference and start_hydration_column >= hydration_difference:
                #print(f"  starting point too far, removing (e,h): {start_energy_row}, {start_hydration_column}")
                continue
            
            for index, row in df.iterrows():
                price = int(row['price'])
                energy = int(row['energy'])
                hydration = int(row['hydration'])
                name = row['name']
            
                #print(f"  starting point valid, jumping from (e,h): {start_energy_row}, {start_hydration_column}")
                result_energy_row = start_energy_row + energy
                result_hydration_column = start_hydration_column + hydration

                #check for out of bounds/negative effects
                if result_energy_row >= total_energy_rows or result_hydration_column >= total_hydration_columns or result_energy_row < 0 or result_hydration_column < 0:
                    #print(f"  provision lands out of bounds, skipping (e,h): {result_energy_row}, {result_hydration_column}. name: {name}, price: {price}, energy: {energy}, hydration: {hydration}")
                    continue
                
                curr_combo_price = dp_arr[start_energy_row][start_hydration_column] + price
                if dp_arr[result_energy_row][result_hydration_column] > curr_combo_price:
                    dp_arr[result_energy_row][result_hydration_column] = curr_combo_price
                    curr_combo_provisions = dp_provisions_arr[start_energy_row][start_hydration_column] + [name]
                    dp_provisions_arr[result_energy_row][result_hydration_column] = curr_combo_provisions

                    valid_start_points.append((result_energy_row, result_hydration_column))

                    for energy_row in range(0, result_energy_row):
                        for hydration_column in range(0, result_hydration_column):
                            if energy_row < start_energy_row and hydration_column < start_hydration_column:
                                continue
                            if dp_arr[energy_row][hydration_column] > curr_combo_price:
                                dp_arr[energy_row][hydration_column] = curr_combo_price
                                dp_provisions_arr[energy_row][hydration_column] = curr_combo_provisions
        
        
        provisions = [{col: row[col] for col in df.columns} for index, row in df.iterrows() if row['name'] in dp_provisions_arr[energy_difference][hydration_difference]]
        
        response = {
            'min_price': dp_arr[energy_difference][hydration_difference],
            'provisions': provisions,
            'final_energy': current_energy + sum([provision['energy'] for provision in provisions]),
            'final_hydration': current_hydration + sum([provision['hydration'] for provision in provisions])
        }
    except:
        response = "failed"
    return response

def best_to_consume_dict(current_energy, current_hydration, goal_energy, goal_hydration, df):
    """
    Returns the best item to consume based on the current energy and hydration levels.
    """

    #set up the re-used variables and the DP array
    energy_difference = goal_energy - current_energy
    hydration_difference = goal_hydration - current_hydration
    
    storage_dict = {(0,0): [0,[]]}

    contenders_dict = {}

    valid_start_points = [(0,0)]



    while valid_start_points:
        current_start_energy, current_start_hydration = valid_start_points.pop(0)
        print(f"trying starting point (e,h): {current_start_energy}, {current_start_hydration}")

        if (current_start_energy >= energy_difference and current_start_hydration >= hydration_difference) or (current_start_energy < -50 and current_start_hydration < -50):
            #print(f"  starting point too far, removing (e,h): {start_energy_row}, {start_hydration_column}")
            continue
        
        for index, row in df.iterrows():
            price = int(row['price'])
            energy = int(row['energy'])
            hydration = int(row['hydration'])
            name = row['name']
        
            #print(f"  starting point valid, jumping from (e,h): {start_energy_row}, {start_hydration_column}")
            current_result_energy= current_start_energy + energy
            current_result_hydration = current_start_hydration + hydration

            
            curr_combo_price = storage_dict[(current_start_energy, current_start_hydration)][0] + price
            curr_combo_names = storage_dict[(current_start_energy, current_start_hydration)][1] + [name]

            if (current_result_energy, current_result_hydration) not in storage_dict:
                storage_dict[(current_result_energy, current_result_hydration)] = [curr_combo_price, [name]]
                if (current_result_energy >= energy_difference and current_result_hydration >= hydration_difference):
                    contenders_dict[(current_result_energy, current_result_hydration)] = storage_dict[(current_result_energy, current_result_hydration)]
                    continue
                elif (current_result_energy > -50 and current_result_hydration > -50 and current_result_energy < goal_energy + 50 and current_result_hydration < goal_hydration + 50):
                    valid_start_points.append((current_result_energy, current_result_hydration))
                    continue
            else:
                if storage_dict[(current_result_energy, current_result_hydration)][0] > curr_combo_price:
                    storage_dict[(current_result_energy, current_result_hydration)] = [curr_combo_price, curr_combo_names]
                    #curr_combo_provisions = storage_dict[(current_result_energy, current_result_hydration)][1] + [name]
                    if (current_result_energy >= energy_difference and current_result_hydration >= hydration_difference):
                        contenders_dict[(current_result_energy, current_result_hydration)] = storage_dict[(current_result_energy, current_result_hydration)]
                        continue
                    elif (current_result_energy > -50 and current_result_hydration > -50 and current_result_energy < goal_energy + 50 and current_result_hydration < goal_hydration + 50):
                        valid_start_points.append((current_result_energy, current_result_hydration))
                        continue

    min_price = float('inf')
    min_price_key = None
    for key, value in contenders_dict.items():
        if value[0] < min_price:
            min_price = value[0]
            min_price_key = key
    
    provisions = [{col: row[col] for col in df.columns} for index, row in df.iterrows() if row['name'] in contenders_dict[min_price_key][1]]
    
    response = {
        'min_price': min_price,
        'provisions': provisions,
        'final_energy': current_energy + min_price_key[0],
        'final_hydration': current_hydration + min_price_key[1]
    }
    return response

def best_to_consume_pulp(current_energy, current_hydration, goal_energy, goal_hydration, df):
    import pulp

    # Data
    items = []#["item1", "item2", ...]   List of item names
    costs = {}#{"item1": cost1, "item2": cost2, ...}  # Dict of costs
    energy = {}#{"item1": energy1, "item2": energy2, ...}  # Dict of energy values
    hydration = {}#{"item1": hydration1, "item2": hydration2, ...}  # Dict of hydration values

    for idx, row in df.iterrows():
        #print(row)
        #print(f'item: {row["name"]}')
        items.append(row['name'])
        #print(f'cost: {row["price"]}')
        costs[row['name']] = row['price']
        #print(f'energy: {row["energy"]}')
        energy[row['name']] = row['energy']
        #print(f'hydration: {row["hydration"]}')
        hydration[row['name']] = row['hydration']

    required_energy = goal_energy - current_energy  # Required energy to reach full
    required_hydration = goal_hydration - current_hydration  # Required hydration to reach full

    # Problem
    prob = pulp.LpProblem("TarkovFoodProblem", pulp.LpMinimize)

    # Variables (non-negative)
    item_vars = pulp.LpVariable.dicts("Items", items, lowBound=0, cat='Continuous')

    # Objective Function
    prob += pulp.lpSum([costs[i] * item_vars[i] for i in items]), "Total Cost"

    # Constraints
    prob += pulp.lpSum([energy[i] * item_vars[i] for i in items]) >= required_energy, "Total Energy"
    prob += pulp.lpSum([hydration[i] * item_vars[i] for i in items]) >= required_hydration, "Total Hydration"

    # Solve the problem
    prob.solve()

    # Output results
    for v in prob.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
    print("Total Cost = ", pulp.value(prob.objective))

def best_to_comusme_fast(start_energy, start_hydration, goal_energy, goal_hydration, df):
    #(energy, hydration) -> [price, [provision_names]]
    error_bound = 30
    main_grid_dict = {}
    main_grid_dict[(start_energy, start_hydration)] = [0,[]]
    valid_start_points = [(start_energy, start_hydration)]

    while valid_start_points:
        current_energy, current_hydration = valid_start_points.pop(0)
        for index, row in df.iterrows():
            price = int(row['price'])
            energy = int(row['energy'])
            hydration = int(row['hydration'])
            name = row['name']


            result_energy = max(current_energy + energy, 0)
            result_hydration = max(current_hydration + hydration, 0)



            if (result_energy, result_hydration) not in main_grid_dict.keys():
                if result_energy < start_energy - error_bound or result_hydration < start_hydration - error_bound or result_energy > goal_energy + error_bound or result_hydration > goal_hydration + error_bound:
                    continue
                main_grid_dict[(result_energy, result_hydration)] = [main_grid_dict[(current_energy, current_hydration)][0] + price, main_grid_dict[(current_energy, current_hydration)][1] + [name]]
                valid_start_points.append((result_energy, result_hydration))
            else:
                if main_grid_dict[(result_energy, result_hydration)][0] > main_grid_dict[(current_energy, current_hydration)][0] + price:
                    main_grid_dict[(result_energy, result_hydration)] = [main_grid_dict[(current_energy, current_hydration)][0] + price, main_grid_dict[(current_energy, current_hydration)][1] + [name]]
                    if result_energy < start_energy - error_bound or result_hydration < start_hydration - error_bound or result_energy > goal_energy + error_bound or result_hydration > goal_hydration + error_bound:
                        continue
                    valid_start_points.append((result_energy, result_hydration))
    
    answer = []
    for key in main_grid_dict.keys():
        #print(f"key: {key}, value: {main_grid_dict[key]}")
        if key[0] <= goal_energy + error_bound and key[1] <= goal_hydration + error_bound and key[0] >= goal_energy and key[1] >= goal_hydration:
            print(f"not final key: {key}, value: {main_grid_dict[key]}")
            if answer == [] or main_grid_dict[key][0] < answer[0]:
                answer = main_grid_dict[key]
            #answer.append(main_grid_dict[key])
    return answer