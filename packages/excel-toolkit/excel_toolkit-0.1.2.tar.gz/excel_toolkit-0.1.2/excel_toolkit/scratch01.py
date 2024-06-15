import inspect
import xlwings as xw
from excel_tool.worksheet import *
# from thefuzz import fuzz
from fuzzywuzzy import fuzz

def whoami(): 
    frame = inspect.currentframe()
    return inspect.getframeinfo(frame).function

def foo():
    print(whoami())

###################### declare workbook/worksheet that's used for testing #######################################
test_path01 = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\Emblem Coef\OD_Freq.xlsx"
wb_test01 = xw.Book(test_path01)
ws_test01 = Ws_WS_at_WB("Model",wb_test01)

test_path02 = r"C:\Users\Heng2pi020\OneDrive\VBA VSCode\VBA MyLib Dev V08.02.xlsb"
# wb_test02 = xw.Book(test_path02)
# wb_02_Test1 = wb_test02.sheets["Test1"]
#-------------------------- declare workbook/worksheet that's used for testing ---------------------------------------
str01 = "Rest - Individual"
str02 = "Individual - Rest"
# print(fuzz.WRatio(str01,str02))
print(fuzz.ratio(str01,str02)) #59