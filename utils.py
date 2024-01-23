def best_to_consume(current_energy, current_hydration, goal_energy, goal_hydration, reference_dict):
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

        


