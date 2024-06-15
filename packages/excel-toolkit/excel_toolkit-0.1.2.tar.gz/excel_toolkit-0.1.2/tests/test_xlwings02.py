# TODO Next: Rg_NextNoTextCell, St_GetAfter,St_GetBefore

from excel_tool.excel_tool.range import *
from excel_tool.other import *
from M01_String import *
from excel_tool.worksheet import *

###################### declare workbook/worksheet that's used for testing #######################################
test_path01 = r"C:\Users\Heng2020\OneDrive\W_Documents\Rotation 3 NPPM\Emblem Coef\OD_Freq.xlsx"
wb_test01 = xw.Book(test_path01)
ws_test01 = Ws_WS_at_WB("Model",wb_test01)

test_path02 = r"C:\Users\Heng2020\OneDrive\VBA VSCode\VBA MyLib Dev V08.02.xlsb"
wb_test02 = xw.Book(test_path02)
wb_02_Test1 = wb_test02.sheets["Test1"]
#-------------------------- declare workbook/worksheet that's used for testing ---------------------------------------

def test_St_SimilarScore():
    str01 = "apple"
    list01 = ['apples', 'oranges', 'pineapple', 'purple']
    
    ans01 = St_SimilarScore(str01,list01)
    pass


def test_St_SimilarString():
    word_list = ["apple", "banana", "cherry"]
    compare_list = ["apples", "bananas", "cherries"]
    cut_off = 0.6

    expected_output01 = ["apple", "", "cherry"]
    ans01 = St_SimilarString(word_list, compare_list, cut_off,return_score=True) 
    print(expected_output01)
    print(ans01)

    word_list = ["apple", "banana", "cherry"]
    compare_list = ["apples", "bananas", "berries"]
    cut_off = 0.6

    expected_output02 = ["apple", "banana", ""]
    ans02 = St_SimilarString(word_list, compare_list, cut_off,return_score=True) 
    print(expected_output02)
    print(ans02)
    # assert ans02 == expected_output02

    word_list = ["apple", "banana", "cherry"]
    compare_list = ["apples", "bananas", "cherries"]
    cut_off = 0.9

    expected_output03 = ["", "", ""]
    ans03 = St_SimilarString(word_list, compare_list, cut_off,return_score=True) 
    print(expected_output03)
    print(ans03)
    # assert ans03 == expected_output03

    word04 = "apples"
    compare_list04 = ["apple", "banana", "cherry"]
    ans04_01 = St_SimilarString(word04,compare_list04)
    ans04_02 = St_SimilarString(word04,compare_list04,return_word=False,return_score=True)
    ans04_03 = St_SimilarString(word04,compare_list04,return_score=True)

    word05 = "Rest - individual"
    compare_list05 = ["individual- Rest","Individual","Yeah"]
    ans05 = St_SimilarString(word05,compare_list05,return_score=True)
    print("All test cases passed!")


def test_Rg_NextNumeric():
    rng01 = wb_02_Test1["E41"]
    rng02 = wb_02_Test1["G7"]
    ans_left = nextNumeric(rng01,"left")
    ans_right = nextNumeric(rng01,"right")
    ans_up = nextNumeric(rng01,"up")
    ans_down = nextNumeric(rng01,"down")

    test_name = D_Get_FuncName()
    func_name = St_GetAfter(test_name,"test_")
    print(f"{func_name} Pass!!!")


def test_St_GetAfter():
    # Example usage
    text = "test_example"
    result = St_GetAfter(text, "test_", return_as_empty=True, include_delimiter=False)
    print(result)  # Output: "example"

    prefixes = ["pre_", "post_"]
    text2 = "post_text"
    result2 = St_GetAfter(text2, prefixes, return_as_empty=False, include_delimiter=True)
    print(result2)  # Output: "_text"

    text3 = "no_prefix"
    result3 = St_GetAfter(text3, "test_", return_as_empty=True, include_delimiter=False)
    print(result3)  # Output: ""

    text4 = "no_prefix"
    result4 = St_GetAfter(text4,"pre")
    print(result4)


def test_Ws_WS_at_WB():
    # rng02 = Rg_FindAllRange02("Base",ws_test01,wb_test01) 
    look_at = ws_test01["A1:G20"]
    rng03 = findAllRange("Base",ws_test01,wb_test01,look_at)
    # rng01 = Rg_FindAllRange("Base",ws_test01,wb_test01)

def test_Rg_NextTextCell():
    rng01 = ws_test01["D5"]
    rng02 = ws_test01["G7"]
    ans_left = nextTextCell(rng01,"left")
    ans_right = nextTextCell(rng01,"right")
    ans_up = nextTextCell(rng02,"up")
    ans_down = nextTextCell(rng01,"down")

    test_name = D_Get_FuncName()
    func_name = St_GetAfter(test_name,"test_")
    print(f"{func_name} Pass!!!")

def test_St_ContainsNum():
    str01 = "ienfno ef"
    str02 = "206446 "
    str03 = "dfefe 6164"
    str04 = "2154545 ??/??"
    str05 = 6
    str06 = 6.58
    ans01 = St_ContainsNum(str01)
    ans02 = St_ContainsNum(str02)
    ans03 = St_ContainsNum(str03)
    ans04 = St_ContainsNum(str04)
    ans05 = St_ContainsNum(str05)
    ans06 = St_ContainsNum(str06)
    print("St_ContainsNum Pass!!!")

def test_Rg_NextContainNum():
    rng01 = wb_02_Test1["S36"]
    rng02 = wb_02_Test1["G7"]
    ans_left = nextContainNum(rng01,"left")
    ans_right = nextContainNum(rng01,"right")
    ans_up = nextContainNum(rng01,"up")
    ans_down = nextContainNum(rng01,"down")

    func_name = "Rg_NextContainNum"
    print(f"{func_name} Pass!!!")

def test_Rg_NextNoTextCell():
    rng01 = wb_02_Test1["P29"]
    rng02 = wb_02_Test1["G7"]
    ans_left = nextNoTextCell(rng01,"left")
    ans_right = nextNoTextCell(rng01,"right")
    ans_up = nextNoTextCell(rng01,"up")
    ans_down = nextNoTextCell(rng01,"down")


    func_name = "Rg_NextNoTextCell"
    print(f"{func_name} Pass!!!")




def main():
    # test_Ws_WS_at_WB()
    # test_St_SimilarScore()
    # test_St_SimilarString()
    # test_St_GetAfter()
    test_Rg_NextNoTextCell()
    test_Rg_NextNumeric()
    test_Rg_NextContainNum()
    test_Rg_NextTextCell()
    test_St_ContainsNum()
    test_Rg_NextContainNum()



if __name__ == "__main__":
    main()
