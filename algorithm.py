import sys
import csv
import json
import warnings
import pandas as pd

def process_csv(input_csv_path, output_csv_path):
    # Read the input CSV into a DataFrame
    df = pd.read_csv(input_csv_path)

        # Define seat allocations
    seats = {
        'CSE': {
            'ur': {'female': 3, 'ex_serviceman': 1, 'freedom_fighter': 0, 'pwd': 1, 'open': 7},
            'sc': {'female': 1, 'ex_serviceman': 0, 'freedom_fighter': 0, 'pwd': 1, 'open': 2},
            'st': {'female': 3, 'ex_serviceman': 0, 'freedom_fighter': 1, 'pwd': 0, 'open': 6},
            'obc': {'female': 2, 'ex_serviceman': 0, 'freedom_fighter': 0, 'pwd': 0, 'open': 2}
        },
        'DSAI': {
            'ur': {'female': 4, 'ex_serviceman': 1, 'freedom_fighter': 1, 'pwd': 0, 'open': 7},
            'sc': {'female': 1, 'ex_serviceman': 0, 'freedom_fighter': 0, 'pwd': 0, 'open': 2},
            'st': {'female': 3, 'ex_serviceman': 0, 'freedom_fighter': 0, 'pwd': 1, 'open': 6},
            'obc': {'female': 1, 'ex_serviceman': 0, 'freedom_fighter': 0, 'pwd': 1, 'open': 2}
        },
        'ECE': {
            'ur': {'female': 4, 'ex_serviceman': 0, 'freedom_fighter': 0, 'pwd': 1, 'open': 8},
            'sc': {'female': 1, 'ex_serviceman': 1, 'freedom_fighter': 0, 'pwd': 0, 'open': 2},
            'st': {'female': 3, 'ex_serviceman': 1, 'freedom_fighter': 0, 'pwd': 0, 'open': 5},
            'obc': {'female': 1, 'ex_serviceman': 1, 'freedom_fighter': 0, 'pwd': 0, 'open': 2}
        }
    }
    # Initialize allocation tables
    allocation_tables = {}
    for branch in ['CSE', 'DSAI', 'ECE']:
        for category in ['ur', 'sc', 'st', 'obc']:
            for spec in ['female', 'ex_serviceman', 'freedom_fighter', 'pwd', 'open']:
                table_name = f"{branch}_{category}_{spec}"
                allocation_tables[table_name] = pd.DataFrame(columns=df.columns.tolist() + ['Allocated_Branch', 'Allocated_Table'])

    def can_allocate(student, table, seats):
        return len(table) < seats

    # Modify allocate_student to return only the allocated table name
    def allocate_student(student, branch, tables, seats):
        if pd.isna(branch):
            return None  # Skip allocation if branch is NaN

        gender = student['Gender']
        category = student['Category']
        percentage=student['XII_Aggregate Percentage']

        # UR Category Check
        if gender == 'Female' and percentage>=60:
            if can_allocate(student, tables.get(f"{branch}_ur_female", pd.DataFrame()), seats[branch]['ur']['female']):
                return f"{branch}_ur_female"  # Only return the table name
        if student['Wards of ex-serviceman'] == 'Yes' and percentage>=60:
            if can_allocate(student, tables.get(f"{branch}_ur_ex_serviceman", pd.DataFrame()), seats[branch]['ur']['ex_serviceman']):
                return f"{branch}_ur_ex_serviceman"
        if student['Freedom fighter'] == 'Yes' and percentage>=60:
            if can_allocate(student, tables.get(f"{branch}_ur_freedom_fighter", pd.DataFrame()), seats[branch]['ur']['freedom_fighter']):
                return f"{branch}_ur_freedom_fighter"
        if student['Physical Disabled'] != 'No' and percentage>=60:
            if can_allocate(student, tables.get(f"{branch}_ur_pwd", pd.DataFrame()), seats[branch]['ur']['pwd']):
                return f"{branch}_ur_pwd"
        if percentage>=60:
            if can_allocate(student, tables.get(f"{branch}_ur_open", pd.DataFrame()), seats[branch]['ur']['open']):
                return f"{branch}_ur_open"


        if category == 'SC' and percentage>=45:
            if gender == 'Female':
                if can_allocate(student, tables.get(f"{branch}_sc_female", pd.DataFrame()), seats[branch]['sc']['female']):
                    return f"{branch}_sc_female"
            if student['Wards of ex-serviceman'] == 'Yes':
                if can_allocate(student, tables.get(f"{branch}_sc_ex_serviceman", pd.DataFrame()), seats[branch]['sc']['ex_serviceman']):
                    return f"{branch}_sc_ex_serviceman"
            if student['Freedom fighter'] == 'Yes':
                if can_allocate(student, tables.get(f"{branch}_sc_freedom_fighter", pd.DataFrame()), seats[branch]['sc']['freedom_fighter']):
                    return f"{branch}_sc_freedom_fighter"
            if student['Physical Disabled'] != 'No':
                if can_allocate(student, tables.get(f"{branch}_sc_pwd", pd.DataFrame()), seats[branch]['sc']['pwd']):
                    return f"{branch}_sc_pwd"
            if can_allocate(student, tables.get(f"{branch}_sc_open", pd.DataFrame()), seats[branch]['sc']['open']):
                return f"{branch}_sc_open"

        elif category == 'ST' and percentage>=45:
            if gender == 'Female':
                if can_allocate(student, tables.get(f"{branch}_st_female", pd.DataFrame()), seats[branch]['st']['female']):
                    return f"{branch}_st_female"
            if student['Wards of ex-serviceman'] == 'Yes':
                if can_allocate(student, tables.get(f"{branch}_st_ex_serviceman", pd.DataFrame()), seats[branch]['st']['ex_serviceman']):
                    return f"{branch}_st_ex_serviceman"
            if student['Freedom fighter'] == 'Yes':

                if can_allocate(student, tables.get(f"{branch}_st_freedom_fighter", pd.DataFrame()), seats[branch]['st']['freedom_fighter']):
                    return f"{branch}_st_freedom_fighter"
            if student['Physical Disabled'] != 'No':
                if can_allocate(student, tables.get(f"{branch}_st_pwd", pd.DataFrame()), seats[branch]['st']['pwd']):
                    return f"{branch}_st_pwd"
            if can_allocate(student, tables.get(f"{branch}_st_open", pd.DataFrame()), seats[branch]['st']['open']):
                return f"{branch}_st_open"

        elif category == 'OBC' and percentage>=45:
            if gender == 'Female':
                if can_allocate(student, tables.get(f"{branch}_obc_female", pd.DataFrame()), seats[branch]['obc']['female']):
                    return f"{branch}_obc_female"
            if student['Wards of ex-serviceman'] == 'Yes':
                if can_allocate(student, tables.get(f"{branch}_obc_ex_serviceman", pd.DataFrame()), seats[branch]['obc']['ex_serviceman']):
                    return f"{branch}_obc_ex_serviceman"
            if student['Freedom fighter'] == 'Yes':
                if can_allocate(student, tables.get(f"{branch}_obc_freedom_fighter", pd.DataFrame()), seats[branch]['obc']['freedom_fighter']):
                    return f"{branch}_obc_freedom_fighter"
            if student['Physical Disabled'] != 'No':
                if can_allocate(student, tables.get(f"{branch}_obc_pwd", pd.DataFrame()), seats[branch]['obc']['pwd']):
                    return f"{branch}_obc_pwd"
            if can_allocate(student, tables.get(f"{branch}_obc_open", pd.DataFrame()), seats[branch]['obc']['open']):
                return f"{branch}_obc_open"

        return None
    st_to_st_open = {}
    sc_to_sc_open = {}
    obc_to_obc_open = {}

    for branch in seats:
        st_to_st_open[branch] = {
            'ex_serviceman': 0,
            'freedom_fighter': 0,
            'pwd': 0,
            'female': 0
        }
        sc_to_sc_open[branch] = {
            'ex_serviceman': 0,
            'freedom_fighter': 0,
            'pwd': 0,
            'female': 0
        }
        obc_to_obc_open[branch] = {
            'ex_serviceman': 0,
            'freedom_fighter': 0,
            'pwd': 0,
            'female': 0
        }
    def reset_seats():
        for branch in seats:
            st_to_st_open[branch] = {
                'ex_serviceman': 0,
                'freedom_fighter': 0,
                'pwd': 0,
                'female': 0
            }
            sc_to_sc_open[branch] = {
                'ex_serviceman': 0,
                'freedom_fighter': 0,
                'pwd': 0,
                'female': 0
            }
            obc_to_obc_open[branch] = {
                'ex_serviceman': 0,
                'freedom_fighter': 0,
                'pwd': 0,
                'female': 0
            }
    def calculate_remaining_seats():
        remaining_seats = {}
        for branch in seats:
            st_to_st_open[branch] = {
                'ex_serviceman': 0,
                'freedom_fighter': 0,
                'pwd': 0,
                'female': 0
            }
            sc_to_sc_open[branch] = {
                'ex_serviceman': 0,
                'freedom_fighter': 0,
                'pwd': 0,
                'female': 0
            }
            obc_to_obc_open[branch] = {
                'ex_serviceman': 0,
                'freedom_fighter': 0,
                'pwd': 0,
                'female': 0
            }
        for table_name, df in allocation_tables.items():
            branch, category, spec = table_name.split('_', 2)
            spec = spec.replace(' ', '_')
            seats_available = seats[branch][category][spec]
            seats_filled = len(df)
            remaining_seats[table_name] = seats_available - seats_filled



        for branch in seats:

            # ST to SC
            if remaining_seats[f"{branch}_st_open"] > 0:
                remaining_seats[f"{branch}_sc_open"] += remaining_seats[f"{branch}_st_open"]
                remaining_seats[f"{branch}_st_open"] = -1*remaining_seats[f"{branch}_st_open"]
            # SC to UR
            if remaining_seats[f"{branch}_sc_open"] > 0:
                remaining_seats[f"{branch}_ur_open"] += remaining_seats[f"{branch}_sc_open"]
                remaining_seats[f"{branch}_sc_open"] = -1*remaining_seats[f"{branch}_sc_open"]
            # OBC to UR
            if remaining_seats[f"{branch}_obc_open"] > 0:
                remaining_seats[f"{branch}_ur_open"] += remaining_seats[f"{branch}_obc_open"]
                remaining_seats[f"{branch}_obc_open"] = -1*remaining_seats[f"{branch}_obc_open"]

            for spec in ['female','ex_serviceman', 'freedom_fighter', 'pwd']:
                # UR Category
                if f"{branch}_ur_{spec}" in remaining_seats and remaining_seats[f"{branch}_ur_{spec}"] > 0:
                    remaining_seats[f'{branch}_ur_open'] += remaining_seats[f'{branch}_ur_{spec}']
                    remaining_seats[f'{branch}_ur_{spec}'] = -1 * remaining_seats[f'{branch}_ur_{spec}']

                # SC Category
                if f"{branch}_sc_{spec}" in remaining_seats and remaining_seats[f"{branch}_sc_{spec}"] > 0:
                    sc_to_sc_open[branch][spec] += remaining_seats[f'{branch}_sc_{spec}']
                    remaining_seats[f'{branch}_sc_open'] += remaining_seats[f'{branch}_sc_{spec}']
                    remaining_seats[f'{branch}_sc_{spec}'] = -1 * remaining_seats[f'{branch}_sc_{spec}']

                # ST Category
                if f"{branch}_st_{spec}" in remaining_seats and remaining_seats[f"{branch}_st_{spec}"] > 0:
                    st_to_st_open[branch][spec] += remaining_seats[f'{branch}_st_{spec}']
                    remaining_seats[f'{branch}_st_open'] += remaining_seats[f'{branch}_st_{spec}']
                    remaining_seats[f'{branch}_st_{spec}'] = -1 * remaining_seats[f'{branch}_st_{spec}']

                # OBC Category
                if f"{branch}_obc_{spec}" in remaining_seats and remaining_seats[f"{branch}_obc_{spec}"] > 0:
                    obc_to_obc_open[branch][spec] += remaining_seats[f'{branch}_obc_{spec}']
                    remaining_seats[f'{branch}_obc_open'] += remaining_seats[f'{branch}_obc_{spec}']
                    remaining_seats[f'{branch}_obc_{spec}'] = -1 * remaining_seats[f'{branch}_obc_{spec}']


        return remaining_seats

    remaining_seats = calculate_remaining_seats()
    def calculate_remaining_seats2():
        remaining_seats = {}
        for table_name, df in allocation_tables.items():
            branch, category, spec = table_name.split('_', 2)
            spec = spec.replace(' ', '_')  # Adjust spec to match keys in seats
            seats_available = seats[branch][category][spec]
            seats_filled = len(df)
            remaining_seats[table_name] = seats_available - seats_filled


        for branch in seats:
            count=0
            if(sc_to_sc_open[branch]['female'] > 0 and remaining_seats[f'{branch}_sc_open'] > 0):
                x = min(sc_to_sc_open[branch]['female'], remaining_seats[f'{branch}_sc_open'])
                remaining_seats[f'{branch}_ur_female'] += x
                sc_to_sc_open[branch]['female'] =0
                count += x


            if(sc_to_sc_open[branch]['pwd'] > 0 and remaining_seats[f'{branch}_sc_open'] > 0):
                x = min(sc_to_sc_open[branch]['pwd'], remaining_seats[f'{branch}_sc_open'])
                remaining_seats[f'{branch}_ur_pwd'] += x
                sc_to_sc_open[branch]['pwd'] = 0
                count += x


            if(sc_to_sc_open[branch]['freedom_fighter'] > 0 and remaining_seats[f'{branch}_sc_open'] > 0):
                x = min(sc_to_sc_open[branch]['freedom_fighter'], remaining_seats[f'{branch}_sc_open'])
                remaining_seats[f'{branch}_ur_freedom_fighter'] += x
                sc_to_sc_open[branch]['freedom_fighter'] = 0
                count += x


            if(sc_to_sc_open[branch]['ex_serviceman'] > 0 and remaining_seats[f'{branch}_sc_open'] > 0):
                x = min(sc_to_sc_open[branch]['ex_serviceman'], remaining_seats[f'{branch}_sc_open'])
                remaining_seats[f'{branch}_ur_ex_serviceman'] += x
                sc_to_sc_open[branch]['ex_serviceman'] = 0
                count += x

            remaining_seats[f'{branch}_sc_open']= -1*count
        for branch in seats:
            count1=0
            if(obc_to_obc_open[branch]['female'] > 0 and remaining_seats[f'{branch}_obc_open'] > 0):
                x = min(obc_to_obc_open[branch]['female'], remaining_seats[f'{branch}_obc_open'])
                remaining_seats[f'{branch}_ur_female'] += x
                obc_to_obc_open[branch]['female'] = 0
                count1 += x


            if(obc_to_obc_open[branch]['pwd'] > 0 and remaining_seats[f'{branch}_obc_open'] > 0):
                x = min(obc_to_obc_open[branch]['pwd'], remaining_seats[f'{branch}_obc_open'])
                remaining_seats[f'{branch}_ur_pwd'] += x
                obc_to_obc_open[branch]['pwd'] = 0
                count1 += x


            if(obc_to_obc_open[branch]['freedom_fighter'] > 0 and remaining_seats[f'{branch}_obc_open'] > 0):
                x = min(obc_to_obc_open[branch]['freedom_fighter'], remaining_seats[f'{branch}_obc_open'])
                remaining_seats[f'{branch}_ur_freedom_fighter'] += x
                obc_to_obc_open[branch]['freedom_fighter'] = 0
                count1 += x


            if(obc_to_obc_open[branch]['ex_serviceman'] > 0 and remaining_seats[f'{branch}_obc_open'] > 0):
                x = min(obc_to_obc_open[branch]['ex_serviceman'], remaining_seats[f'{branch}_obc_open'])
                remaining_seats[f'{branch}_ur_ex_serviceman'] += x
                obc_to_obc_open[branch]['ex_serviceman'] = 0
                count1 += x

            remaining_seats[f'{branch}_obc_open']= -1*count1


        for branch in seats:
            count2=0
            if(st_to_st_open[branch]['female'] > 0 and remaining_seats[f'{branch}_st_open']>0 ):
                x=min(st_to_st_open[branch]['female'],remaining_seats[f'{branch}_st_open'])
                remaining_seats[f'{branch}_sc_female'] += x
                st_to_st_open[branch]['female'] = 0
                count2+=x


            if(st_to_st_open[branch]['pwd'] > 0 and remaining_seats[f'{branch}_st_open'] > 0):
                x = min(st_to_st_open[branch]['pwd'], remaining_seats[f'{branch}_st_open'])
                remaining_seats[f'{branch}_sc_pwd'] += x
                st_to_st_open[branch]['pwd'] = 0
                count2 += x


            if(st_to_st_open[branch]['freedom_fighter'] > 0 and remaining_seats[f'{branch}_st_open'] > 0):
                x = min(st_to_st_open[branch]['freedom_fighter'], remaining_seats[f'{branch}_st_open'])
                remaining_seats[f'{branch}_sc_freedom_fighter'] += x
                st_to_st_open[branch]['freedom_fighter'] = 0
                count2 += x


            if(st_to_st_open[branch]['ex_serviceman'] > 0 and remaining_seats[f'{branch}_st_open'] > 0):
                x = min(st_to_st_open[branch]['ex_serviceman'], remaining_seats[f'{branch}_st_open'])
                remaining_seats[f'{branch}_sc_ex_serviceman'] += x
                st_to_st_open[branch]['ex_serviceman'] = 0
                count2 += x
            remaining_seats[f'{branch}_st_open']= -1*count2
        return remaining_seats
    def display_remaining_seats(remaining_seats):
        for table_name, remaining in remaining_seats.items():
            print(f"Remaining seats in {table_name}: {remaining}")






    def update_seats_with_remaining(remaining_seats):
        # Update the original seats dictionary with the remaining seats calculated
        for table_name, remaining in remaining_seats.items():
            branch, category, spec = table_name.split('_', 2)
            spec = spec.replace(' ', '_')  # Match with seats key format

            # Ensure the branch and category exist in the seats dictionary before updating
            if branch in seats and category in seats[branch]:
                if spec in seats[branch][category]:
                    # Add the remaining seats to the existing seats
                    seats[branch][category][spec] += remaining
                    # Ensure no negative seat values
                    if seats[branch][category][spec] < 0:
                        seats[branch][category][spec] = 0
    columns = [
        'Name', 'Gender', 'Category', 'Choice1', 'Choice2', 'Choice3', 'Rank',
        'Physical Disabled', 'Wards of ex-serviceman', 'Freedom fighter',
        'XII_Aggregate Percentage', 'Allocated_Branch', 'Allocated_Table'
    ]


    # Call the function to update seats with the remaining seats
    def clear_all_tables(allocation_tables, columns):
        for table_name in allocation_tables:
            allocation_tables[table_name] = pd.DataFrame(columns=columns)

    # Main allocation loop
    def main_allocation():
        for _, student in df.iterrows():
            allocated = False
            for choice in ['Choice1', 'Choice2', 'Choice3']:
                branch = student[choice]
                allocated_table = allocate_student(student, branch, allocation_tables, seats)

                if allocated_table:  # Ensure allocation happened
                    # Add 'Allocated_Branch' and 'Allocated_Table' columns
                    if allocated_table in allocation_tables:  # Ensure the key exists
                        #print(f"Allocating {student['Name']} to {allocated_table}")  # Debug info

                        table_df = allocation_tables[allocated_table].copy()

                        # Create a copy of the student data with branch and table info
                        student_with_branch = student.copy()
                        student_with_branch['Allocated_Branch'] = branch
                        student_with_branch['Allocated_Table'] = allocated_table

                        # Append the student to the allocated table
                        

                        # Assuming student_with_branch is a dictionary or list representing the student's data
                        warnings.simplefilter(action='ignore', category=FutureWarning)

                        # Assuming student_with_branch is a dictionary or list representing the student's data
                        student_df = pd.DataFrame([student_with_branch])

                        # Check if the DataFrame is not empty or all NaN before concatenating
                        if not student_df.isna().all(axis=None):  # Check if the entry is not all-NA
                            table_df = pd.concat([table_df, student_df], ignore_index=True)
                            allocation_tables[allocated_table] = table_df
                            allocated = True
                            break  # Stop once the student is allocated to a branch
                        else:
                            print("Warning: Attempted to add an empty or all-NA entry.")


    main_allocation()

    remaining_seats = calculate_remaining_seats()

    update_seats_with_remaining(remaining_seats)
    clear_all_tables(allocation_tables, columns)
    main_allocation()
   


    tables_df = pd.concat(allocation_tables.values(), keys=allocation_tables.keys(), names=['Table'])
    #print(f"Total number of entries in final table: {len(tables_df)}")  # Check final table size
    tables_df= tables_df.sort_values(by='Rank')
    
    # Write the processed DataFrame to an output CSV
    tables_df.to_csv(output_csv_path, index=False)

    return output_csv_path


if __name__ == "__main__":
    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]

    output_file = process_csv(input_csv_path, output_csv_path)
    print(json.dumps({"output_file": output_file}))
