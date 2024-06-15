
from LibPortableV01 import *
def is_Emblem_sheet(ws):
    search_area = ws["A1:G10"]
    base_rng = Rg_FindAllRange("base",ws,search_rng=search_area)
    if isinstance(base_rng,list) or isinstance(base_rng,xw.main.Range)  :
        return True
    else:
        return False
    
def create_emblem_column(emblem_excle):
    wb = Wb_ReturnAsWB(emblem_excle)
    #Still Only support 1 sheet 
    for curr_ws in wb.sheets:
        is_Emblem = is_Emblem_sheet(curr_ws)
        if is_Emblem:
            out_df = create_emblem_columnH01(curr_ws)

    return out_df


def create_emblem_columnH01(ws):
    curr_ws = Ws_WS_at_WB(ws)
    search_base = ws["A1:G10"]
    rng_base = Rg_FindAllRange("Base",curr_ws,search_rng=search_base)
    first_col_var = Rg_NextTextCell(rng_base,"down")

    out_dict = dict()


    while isinstance(first_col_var,xw.main.Range):
        second_col_var = first_col_var.offset(2,0)
        level_start = second_col_var.offset(1,0)
        level_rng = Rg_PickTilEnd(level_start,"down")
        variable_name = second_col_var.value
        level_list = level_rng.value

        # find columns untils the end
        first_col_var = Rg_NextTextCell(first_col_var,"right",cut_off=10)
        out_dict[variable_name] = pd.DataFrame({'level':level_list})
    return out_dict

def return_as_dataFrame(file):
    if isinstance(file,str):
        if 'csv' in file:
            df = pd.read_csv(file)
        elif 'parquet' in file:
            df = pd.read_parquet(file)
        elif ('xlsx' in file) or ('xlsm' in file):
            df = pd.read_excel(file)
        else:
            print("This data type is not supported")
    if isinstance(file,pd.DataFrame):
        df = file
    return df

def input_data_column(file,all_column=False):
    # file can be filepath parque or csv/dataFrame
    df_dict = {}
    df = return_as_dataFrame(file)
    # Iterate over each column in the DataFrame
    
    for column in df.columns:
        curr_type = df.dtypes[column]
        # Get the unique values in the column
        if all_column or (curr_type=='object') or (curr_type=='category') :
            unique_values = df[column].unique()
            
            # Create a DataFrame with the unique values
            unique_df = pd.DataFrame({column: unique_values})
        
            # Assign the DataFrame to the dictionary with the column name as the key
            df_dict[column] = unique_df
        

    return df_dict

def emblem_column_report(data,beta,similar_cut_off=80,print_output=True):

    data_df = return_as_dataFrame(data)
    beta_df = Wb_ReturnAsWB(beta)
    beta_col_dict = create_emblem_column(beta_df)
    data_col_dict = input_data_column(data_df)
    level_report = emblem_level_report(data,beta,False)

    beta_column = list(beta_col_dict.keys())
    data_column = list(data_col_dict.keys())

    # Create an empty DataFrame
    column_report = pd.DataFrame()
    # Add the keys to the 'beta_column' column
    column_report['beta_column'] = beta_column
    total_beta_col = column_report.shape[0]

    col_with_issue = level_report['column'].tolist()
    column_report["CsvClosestColumn"] = ""

    for i in range(total_beta_col):
        row = column_report.iloc[i]
        beta_col = row['beta_column']
        column_report.loc[i,"HaveInCsv"] = (beta_col in data_column)
        column_report.loc[i,"NoLevelIssue"] = not (beta_col in col_with_issue)
        # if don't have in column in csv
        if not column_report.loc[i,"HaveInCsv"]:
            similar_score = St_SimilarScore(beta_col,data_column)
            max_score = similar_score[0][1]
            csv_closest_col = similar_score[0][0]
            if max_score >= similar_cut_off:
                column_report.loc[i,"CsvClosestColumn"] = not (beta_col in col_with_issue)
            column_report.loc[i,"NoLevelIssue"] = ""
    if print_output:
        print(column_report)
    return column_report




        

def emblem_level_report(data,beta,print_output=True):
    beta_wb = Wb_ReturnAsWB(beta)
    data_df = return_as_dataFrame(data)


    beta_col_dict = create_emblem_column(beta_wb)
    data_col_dict = input_data_column(data_df)

    beta_column_list =list(beta_col_dict.keys())
    level_report_rows = []
    # level_report_rows is the list of dictionary
    for column, levels in data_col_dict.items():
        for level in levels[column]:
            if column in beta_col_dict.keys():
                beta_level = list(beta_col_dict[column]['level'])
                if level not in beta_level:
                    level_report_rows.append({'column': column, 'level': level})

    level_report = pd.DataFrame(level_report_rows)
    # print(level_report)

    #line 110 not work
    n_row = level_report.shape[0]

    for i in range(n_row):
        row = level_report.iloc[i]
        col_name = row['column']
        wrong_level = row['level']
        correct_level_list = beta_col_dict[col_name]['level'].tolist()

        if not wrong_level or ('nan' in str(wrong_level).lower()) :
            # if the type is None, np.nan
            unknown_type = "Unknown"
            similar_score = St_SimilarScore(unknown_type,correct_level_list)
            closest_level = similar_score[0][0]
        else:
            similar_score = St_SimilarScore(wrong_level,correct_level_list)
            closest_level = similar_score[0][0]
        # Don't need the declare 'beta_closest_level'
        # You can assign it immediately
        level_report.loc[i,'beta_closest_level'] = closest_level

    if print_output:
        print(level_report)
    return level_report
    # for beta_column in beta_column_list:
    #     beta_level = beta_col_dict[beta_column]
    #     data_level = data_col_dict[beta_column]

    #     beta_level_set = set(beta_level)
    #     data_level_set = set(data_level)

    #     data_extra_level = beta_level_set - data_level_set


def transform_column(df,func,output_name,column_list):
    pass

def map_level():
    pass


def main():
    # MyPC Path
    TP_death_Freq_path = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\Emblem Coef\TP Death Freq.xlsx"
    TP_csv_path = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\final_TP_60_000_rows.csv"
    OD_csv_path = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\final_OD_3000_rows.csv"

    emblem_column = create_emblem_column(TP_death_Freq_path)
    data_column = input_data_column(TP_csv_path)
    print("*"*20 + "Column Report" + "*"*20)
    column_report = emblem_column_report(TP_csv_path,TP_death_Freq_path)
    print("*"*20 + "Level Report" + "*"*20)
    level_report = emblem_level_report(TP_csv_path,TP_death_Freq_path)
    pass

if __name__ == "__main__":
    main()