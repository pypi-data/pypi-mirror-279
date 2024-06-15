import xlwings as xw
def ws_at_WB(ws, wb=None, outputOption=True):
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