from difflib import get_close_matches
from difflib import SequenceMatcher
from thefuzz import fuzz
def St_SimilarScore(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
    # Assume that word_in is only string
    outlist = []
    for text in compare_list:
        similar_score = fuzz.WRatio(word_in,text)
        string_similar = (text,similar_score)
        outlist.append(string_similar)
    outlist.sort(key = lambda x:x[1],reverse=True)
    return outlist



def St_SimilarString(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
    score_list = []
    similar_word = []
    if isinstance(word_in,str):
        # if word_in is only a string
        word_list = [word_in]
    else:
        # if this is a list
        word_list = [word for word in word_in]
    
    for word in word_list:
        max_score = 0
        most_similar = ""
        for compare_word in compare_list:
            score = SequenceMatcher(None, str(word), compare_word).ratio()
            if score > max_score:
                max_score = score
                most_similar = compare_word
            if max_score >= cut_off:
                score_list.append(format(max_score,".4f"))
                similar_word.append(most_similar)
            else:
                score_list.append("")
    
    if return_word:
        if return_score:
            # return both word & score

            if isinstance(word_in,str):
                out_list = list(zip(similar_word,score_list))[0]
                if len(similar_word) == 0:
                    return ""
            else:
                if len(similar_word) == 0:
                    return []
                out_list = list(zip(similar_word,score_list))
        else:
            # return only word
            out_list = similar_word
            
            if isinstance(word_in,str):
                if len(similar_word) == 0:
                    return ""
                out_list = similar_word[0]
            else:
                if len(similar_word) == 0:
                    return []
                out_list = similar_word
    else:
        if return_score:
            # return only score
            
            if isinstance(word_in,str):
                out_list = score_list[0]
            else:
                out_list = score_list

        else:
            out_list = "Invalid! return_word & return_score can't be False at the same time"

    return out_list

def St_ContainsNum(string):
    if isinstance(string,bool) or string is None:
        return False
    if isinstance(string,(int,float)):
        return True
    return any(char.isnumeric() for char in string)

def St_GetAfter(text, prefix_list, return_as_empty=True, include_delimiter=False):
    if isinstance(prefix_list, str):
        prefix_list = [prefix_list]
    
    for prefix in prefix_list:
        index = text.find(prefix)
        if index != -1:
            out_str = text[index + len(prefix):]
            if include_delimiter:
                out_str = prefix + out_str
            return out_str

    if return_as_empty:
        return ""
    else:
        return text

def St_GetBefore(text, suffix_list, return_as_empty=True, include_delimiter=False):
    if isinstance(suffix_list, str):
        suffix_list = [suffix_list]
    
    for suffix in suffix_list:
        index = text.find(suffix)
        if index != -1:
            out_str = text[:index + len(suffix)]
            if include_delimiter:
                out_str = suffix + out_str
            return out_str

    if return_as_empty:
        return ""
    else:
        return text



