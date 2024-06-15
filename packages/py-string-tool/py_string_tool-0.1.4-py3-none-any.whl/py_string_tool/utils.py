from difflib import get_close_matches
from difflib import SequenceMatcher
from thefuzz import fuzz

def replace_backslash(s: str):
    return s.replace('\\','/')

def detect_language(input_text):
    from langdetect import detect
    try:
        # Detect the language of the text
        language = detect(input_text)
        return language
    except Exception as e:
        return f"Language detection failed: {str(e)}"

def similar_score(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
    # Assume that word_in is only string
    outlist = []
    for text in compare_list:
        similar_score = fuzz.WRatio(word_in,text)
        string_similar = (text,similar_score)
        outlist.append(string_similar)
    outlist.sort(key = lambda x:x[1],reverse=True)
    return outlist



def similar_string(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
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

def contain_num(string):
    if isinstance(string,bool) or string is None:
        return False
    if isinstance(string,(int,float)):
        return True
    return any(char.isnumeric() for char in string)

def text_after(text, prefix_list, return_as_empty=True, include_delimiter=False):
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

def text_before(text, suffix_list, return_as_empty=True, include_delimiter=False):
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



def replace_last(s: str, oldvalue, newvalue):
    last_comma_index = s.rfind(oldvalue)
    if last_comma_index != -1:
        s = s[:last_comma_index] + newvalue + s[last_comma_index + 1:]
    return s

def replace_backslash(s):
    pass
def is_empty_string(s):
    # Returns True if the string is empty or whitespace, False otherwise
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 08_VocabList\VocatList_func01.py"
    return not s.strip()

def not_empty_string(s):
    # Returns False if the string is empty or whitespace, True otherwise
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 08_VocabList\VocatList_func01.py"
    return s.strip()


def get_num(string,exclude = "", begin_with_num = True):
    # little tested
    import re
    
    """
    This function extracts the number part of a string.

    Parameters
    ----------
    string : str
        The input string to extract the number from.

    Returns
    -------
    num : int or float or None
        The extracted number as an integer or a floating-point value, or None if no number is found.
    """
    # Import the regular expression module
    if isinstance(exclude, str):
        if exclude != "":
            exclude_ = [exclude]
        else:
            exclude_ = []
    else:
        exclude_ = exclude
    
    for pattern in exclude_:
        if pattern in string:
            return False
    
    if begin_with_num:
        try:
            num = int(string[0])
        except ValueError:
            return False
    
    
    

    # Find the first occurrence of a number in the string using a regular expression
    # The regular expression allows an optional minus sign before the digits and an optional decimal part
    match = re.search(r'-?\d+(\.\d+)?', string)
    

    # If a match is found, convert it to a float and then to an int if possible
    if match:
        num = float(match.group())
        # Check if the number has a decimal part
        if num.is_integer():
            # Convert to an int and return it
            num = int(num)
            return num
        else:
            # Return the float as it is
            return num

    # If no match is found, return None
    else:
        return False