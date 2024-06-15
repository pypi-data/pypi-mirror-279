import xlwings as xw
#################################################### Range lib #################################
def Rg_PickTilEnd(rng, direction) -> xw.main.Range:
        # direction => 'left','right','up','down' as text is shorter
    ws = rng.sheet
    end_address = rng.end(direction).address
    outRng = ws.range(rng.address, end_address)
    return outRng

def Rg_FindAllRange(str_list,ws,wb=None,as_list=True,search_rng=None,caseSensitive=False) -> xw.main.Range :
    # still slow
    ws01 = Ws_WS_at_WB(ws,wb)
    out_list = []
    outRng = None

    if search_rng:
        search_area = search_rng
    else:
        search_area = ws01.used_range

    for rng in search_area:
        curr_val = rng.value
        if isinstance(str_list,list):
            for text in str(str_list):
                if curr_val:
                    if caseSensitive:
                        if text in str(curr_val):
                            out_list.append(rng)
                            # outRng = xw.Range.union(outRng,rng)
                            # outRng = rng
                    else:
                        if text.lower() in str(curr_val).lower():
                            #Don't care about case
                            out_list.append(rng)
                            # outRng = xw.Range.union(outRng,rng)
                            # outRng = rng
        else:
            # in case str_list is only string
            if curr_val:
                if caseSensitive:
                    if str_list in str(curr_val):
                        out_list.append(rng)
                        # outRng = xw.Range.union(outRng,rng)
                        # outRng = rng
                else:
                    if str_list.lower() in str(curr_val).lower():
                        out_list.append(rng)

    # only cover 1 cell case bc I don't know how to union in xlwings
    # if 1 cell it will return as cell object regardless of T/F from as_list
    if len(out_list)==1:
        return out_list[0]

    if as_list:
        return out_list
    else:
        
        return outRng


def Rg_NextTextCell(rng, direction = "down",cut_off = 100):
    return_text = "No Next Text Cell"
    func = lambda x: not x is None
    ans = Rg_NextCell(rng,direction,func,True,return_text,cut_off)
    return ans

def Rg_NextNoTextCell(rng, direction = "down",cut_off = 100):
    return_text = "No Next Empty Cell"
    func = lambda x: x is None
    ans = Rg_NextCell(rng,direction,func,True,return_text,cut_off)
    return ans

def Rg_NextContainNum(rng, direction = "down",cut_off = 100):
    return_text = "No Next Cell that contains number"
    func = St_ContainsNum
    ans = Rg_NextCell(rng,direction,func,True,return_text,cut_off)
    return ans

def Rg_NextNumeric(rng, direction = "down",cut_off = 100):
    return_text = "No Next Cell that is Number"
    func = lambda x: isinstance(x,(int,float))
    ans = Rg_NextCell(rng,direction,func,True,return_text,cut_off)
    return ans


def Rg_NextCell(rng, direction,func_bool,on_value=True,return_text="No Next Cell Found",cut_off = 100):
    # direction => 'left','right','up','down' as text is shorter
    # func_bool should return only True or False
    # on_value = True func_bool will work on rng.value, otherwise it will work directly on rng
    nextCell = rng
    row_offset, col_offset = D_OffsetVal(direction)
    nextCell = nextCell.offset(row_offset,col_offset)
    try:
        # if search through cut_off # of rows and still find nothing then return: return_text
        i = 0
        while i < cut_off:
            if on_value:
                condition = func_bool(nextCell.value)
            else:
                condition = func_bool(nextCell)

            if condition:
                break
            nextCell = nextCell.offset(row_offset, col_offset)
            # if "H" in nextCell.address:
            #     # For debug
            #     pass
            i += 1
        if i == cut_off:
            #Don't have
            return return_text

        return nextCell
    except:
        return return_text

#################################################### Other lib #################################
def Ws_WS_at_WB(ws, wb=None, outputOption=True):
    # If outputOption = True => output WS
    # If outputOption = False => ws_name as string
    # wb could be workbook or string or missing
    # ws could be worksheet or string or missing
    
    try:
        if wb is None:
            wb = ws.book
        elif isinstance(wb, xw.Range):
            wb = xw.Book(wb.value)
        elif wb == "":
            wb = xw.Book.caller()
        else:
            # wb is string
            wb = xw.Book(wb)
    except:
        pass
    
    try:
        wb_name = wb.name
        if ws is None:
            ws02 = xw.Sheet.caller()
        elif isinstance(ws, xw.Range):
            ws02 = wb.sheets[ws.value]
        elif not isinstance(ws, str):
            ws02 = ws
        elif ws == "":
            ws02 = xw.Sheet.caller()
        else:
            # ws is string
            ws02 = wb.sheets[ws]
    except:
        pass
    
    outputWS = wb.sheets[ws02.name]
    if outputOption:
        return outputWS
    else:
        return outputWS.name

def Wb_ReturnAsWB(wb):
    if isinstance(wb,str):
        # This is path
        out_wb = xw.Book(wb)

    elif isinstance(wb,xw.main.Book):
        out_wb = wb
    else:
        return "Not Valid input"
    return out_wb
#################################################### Start Emblem function #################################
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

def emblem_column_report(data,beta):
    data_df = return_as_dataFrame(data)
    beta_df = return_as_dataFrame(beta)
    beta_col_dict = create_emblem_column(data_df)
    data_col_dict = input_data_column(beta_df)

def emblem_level_report(data,beta):
    beta_wb = Wb_ReturnAsWB(beta)
    data_df = return_as_dataFrame(data)


    beta_col_dict = create_emblem_column(beta_wb)
    data_col_dict = input_data_column(data_df)

    beta_column_list =list(beta_col_dict.keys())
    level_report_rows = []

    for column, levels in data_col_dict.items():
        for level in levels[column]:
            if column in beta_col_dict.keys():
                beta_level = list(beta_col_dict[column]['level'])
                if level not in beta_level:
                    level_report_rows.append({'column': column, 'level': level})

    level_report = pd.DataFrame(level_report_rows)
    #line 110 not work
    closest_list = St_SimilarString(list(level_report['level']), beta_column_list, 0.8)
    level_report['closest_level'] 
        
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

#################################################### Main function #################################

def main():
    TP_death_Freq_path = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\Emblem Coef\TP Death Freq.xlsx"
    TP_csv_path = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\final_TP_60_000_rows.csv"
    OD_csv_path = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\final_OD_3000_rows.csv"

    emblem_column = create_emblem_column(TP_death_Freq_path)
    data_column = input_data_column(TP_csv_path)

    level_report = emblem_level_report(TP_csv_path,TP_death_Freq_path)

if __name__ == "__main__":
    main()
