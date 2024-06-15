import xlwings as xw
import pandas as pd
from thefuzz import fuzz
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
############################## String Lib ###########################
def St_ContainsNum(string):
    if isinstance(string,bool) or string is None:
        return False
    if isinstance(string,(int,float)):
        return True
    return any(char.isnumeric() for char in string)
def St_SimilarScore(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
    # Assume that word_in is only string
    outlist = []
    for text in compare_list:
        similar_score = fuzz.WRatio(word_in,text)
        string_similar = (text,similar_score)
        outlist.append(string_similar)
    outlist.sort(key = lambda x:x[1],reverse=True)
    return outlist
# --------------------------- String Lib ------------------------------------
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
def D_OffsetVal(direction):
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

