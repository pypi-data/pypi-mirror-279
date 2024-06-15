import xlwings as xw
from excel_toolkit.worksheet import ws_at_WB
from excel_toolkit.M01_String import St_ContainsNum


def find_all_range(str_list, ws, wb=None, as_list=True, search_rng=None, caseSensitive=False) -> list:
    #  supposed to run much faster than Rg_FindAllRange as it use .api
    
    #  medium tested through get_interaction_grouping
    # Rg_FindAllRange2... seems like this function can run as fast as my VBA Rg_FindAllRange now
    
    
    #  about 2 hrs to write 
    ws01 = ws_at_WB(ws, wb)
    out_list:List[xw.main.Range] = []

    # Set the search area
    if search_rng:
        if isinstance(search_rng, str):
            search_area = ws01.range(search_rng)
        elif isinstance(search_rng, xw.main.Range):
            search_area = search_rng
    else:
        search_area = ws01.used_range

    # Prepare search parameters for case sensitivity
    lookAt = xw.constants.LookAt.xlPart

    if caseSensitive:
        matchCase = True
    else:
        matchCase = False

    # Convert str_list to list if it's a single string
    if isinstance(str_list, str):
        str_list = [str_list]

    # Loop through each string in str_list to find all occurrences
    for text in str_list:
        # found = search_area.api.Find(What=text, LookAt=lookAt, MatchCase=matchCase)
        # if use * only it wouldn't find this actual symbol
        # You need to add tilda to specify that we want this symbol
        if text in ['*','~','?']:
            text_in = "~" + text
        else:
            text_in = text

        found = search_area.api.Find(What=text_in, LookAt=lookAt, MatchCase=matchCase)
        found_adr = found.GetAddress(0,0)
        found_range = ws01.range(found_adr)
        out_list.append(found_range)

        while found_adr:

            # Avoid infinite loop by searching from the next cell
            try:
                found = search_area.api.FindNext(After=found)
            except:
                break

            found_adr = found.GetAddress(0,0)
            # Convert COM object to xlwings Range object
            found_range = ws01.range(found_adr)
            # found_range = xw.Range(found)
            out_list.append(found_range)

            # Break if we loop back to the first found cell
            if found_range.address == out_list[0].address:
                break
            
    if len(out_list)==1:
        return out_list[0]
    # weird bug where you get the same range
    elif len(out_list)==2:
        # if 2 range is the same just return 1 of them
        if out_list[0].address == out_list[1].address:
            return out_list[0]
    if as_list:
        return out_list
    else:
        # If needed, implement logic to return a unified range (not directly supported by xlwings)
        return None  # Placeholder: xlwings does not directly support Range union like Excel VBA


def pick_til_end(rng, direction) -> xw.main.Range:
        # direction => 'left','right','up','down' as text is shorter
    ws = rng.sheet
    end_address = rng.end(direction).address
    outRng = ws.range(rng.address, end_address)
    return outRng

def find_all_range_slow(str_list,ws,wb=None,as_list=True,search_rng=None,caseSensitive=False) -> xw.main.Range :
    # still slow
    ws01 = ws_at_WB(ws,wb)
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


def next_text_cell(rng, direction = "down",cut_off = 100):
    return_text = "No Next Text Cell"
    func = lambda x: not x is None
    ans = next_cell(rng,direction,func,True,return_text,cut_off)
    return ans

def next_no_text_cell(rng, direction = "down",cut_off = 100):
    return_text = "No Next Empty Cell"
    func = lambda x: x is None
    ans = next_cell(rng,direction,func,True,return_text,cut_off)
    return ans

def next_contain_num(rng, direction = "down",cut_off = 100):
    return_text = "No Next Cell that contains number"
    import py_string_tool as pst
    func = pst.contain_num
    ans = next_cell(rng,direction,func,True,return_text,cut_off)
    return ans

def next_numeric(rng, direction = "down",cut_off = 100):
    return_text = "No Next Cell that is Number"
    func = lambda x: isinstance(x,(int,float))
    ans = next_cell(rng,direction,func,True,return_text,cut_off)
    return ans


def next_cell(rng, direction,func_bool,on_value=True,return_text="No Next Cell Found",cut_off = 100):
    # direction => 'left','right','up','down' as text is shorter
    # func_bool should return only True or False
    # on_value = True func_bool will work on rng.value, otherwise it will work directly on rng
    nextCell = rng
    row_offset, col_offset = _offset_val(direction)
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

def _offset_val(direction):
    if direction in ['up']:
        row_offset = -1
        col_offset = 0
    if direction in ['down']:
        row_offset = 1
        col_offset = 0
    if direction in ['left']:
        row_offset = 0
        col_offset = -1
    if direction in ['right']:
        row_offset = 0
        col_offset = 1
    return [row_offset,col_offset]


