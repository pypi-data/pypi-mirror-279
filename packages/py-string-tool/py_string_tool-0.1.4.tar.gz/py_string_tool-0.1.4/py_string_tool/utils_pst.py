from difflib import get_close_matches
from difflib import SequenceMatcher
from thefuzz import fuzz
from typing import Union, Literal
import pandas as pd


def similar_score(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
    # Assume that word_in is only string
    from thefuzz import fuzz
    outlist = []
    for text in compare_list:
        similar_score = fuzz.WRatio(word_in,text)
        string_similar = (text,similar_score)
        outlist.append(string_similar)
    outlist.sort(key = lambda x:x[1],reverse=True)
    return outlist



def similar_text(word_in, compare_list, cut_off=0,return_word=True,return_score=False):
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

def split_sentence(text, delimiter, inplace=True):
    """
    Split elements of a list of strings using a specified delimiter and optionally modify the list in place.

    Parameters
    ----------
    text : list of str
        List of strings to be split.
        
    delimiter : str
        The delimiter to use for splitting each string in the list.
        
    inplace : bool, default True
        If True, modifies the original list `text` in place and returns None.
        If False, creates a copy of the list, modifies the copy, and returns the modified list.

    Returns
    -------
    list of str or None
        If `inplace` is False, returns a new list with the split and trimmed strings.
        If `inplace` is True, modifies the original list in place and returns None.

    Notes
    -----
    - The function trims leading and trailing spaces from each string before and after splitting.
    - Empty strings resulting from the split are not included in the final list.
    - If `inplace` is True, the function operates on the original list and does not return a new list.
    - If `inplace` is False, the function operates on a copy of the list and returns the modified copy.

    Examples
    --------
    >>> text = ["Hello, world", "Python is great"]
    >>> St_SplitSentence(text, ",", inplace=False)
    ['Hello', 'world', 'Python is great']
    
    >>> text = ["Hello, world", "Python is great"]
    >>> St_SplitSentence(text, " ", inplace=True)
    >>> text
    ['Hello,', 'world', 'Python', 'is', 'great']
    """
    if not inplace:
        text = text.copy()
        
    i = 0
    while i < len(text):
        text[i] = text[i].strip()  # Trim the spaces at both ends
        if delimiter in text[i]:
            # Split the string using the delimiter
            split_strings = text[i].split(delimiter)
            
            # Remove the original string from the list
            del text[i]
            
            # Insert the split strings back into the original list at the same position
            for split_str in reversed(split_strings):
                split_str = split_str.strip()  # Remove leading and trailing spaces
                if split_str:  # Only add non-empty strings
                    text.insert(i, split_str)
        else:
            i += 1  # Only increment if no split occurred to handle new inserted strings
            
    return text if not inplace else None

def remove_from_list(lst, char="♪"):
    # Function to remove elements that start with a specific character (in this case "♪")
    # can generalize more to 
    # remove_from_list(lst,start_with = None,end_with = None,logic = "or")
    return [element for element in lst if not str(element).startswith(char)]

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


def replace(text,to_replace,replace_by):
    # unit_tested
    for word in to_replace:
        new_text = text.replace(word, replace_by)
        
    return new_text

def num_format0(num, max_num=None, digit=None):
    # ChatGPT solo
    # tested
    if max_num is not None:
        num_str = str(num).zfill(len(str(max_num)))
    elif digit is not None:
        num_str = str(num).zfill(digit)
    else:
        num_str = str(num)
    # print(num_str)
    return num_str

def format_index_num(to_format_num, total_num):
    # imported from C:/Users/Heng2020/OneDrive/D_Code/Python/Python NLP/NLP 02/NLP_2024/NLP 11_Local_TTS
    # tested via pd_split_into_dict_df
    # adding leading 0 to the number
    # Determine the number of digits in the largest number
    total_digits = len(str(total_num))
    
    # Format the number with leading zeros
    formatted_num = f"{to_format_num:0{total_digits}d}"
    
    return formatted_num

def clean_filename(ori_name):
    # update01: deal with '\n' case
    # imported from NLP 01/NLP 03_11LabsBulk
    replace_with_empty = [".","?",":",'"' , "\\" ] 
    replace_with_space = ["\n", "/" ]
    
    new_name = ori_name
    for delimiter in replace_with_empty:
        new_name = new_name.replace(delimiter, "")
        
    for delimiter in replace_with_space:
        new_name = new_name.replace(delimiter, " ")

    return new_name

def replace_backslash(s: str):
    return s.replace('\\','/')

def detect_language(input_text: Union[str,list[str],pd.Series], 
                    return_as: Literal["full_name","2_chr_code","3_chr_code","langcodes_obj"] = "full_name"):
    import pandas as pd
    from langdetect import detect
    import langcodes
    # medium tested
    # wrote < 30 min(with testing)
    # imported from C:\Users\Heng2020\OneDrive\D_Code\Python\Python NLP\NLP 02\NLP_2024\NLP 11_Local_TTS
    if isinstance(input_text, str):
    # assume only 1d list
        try:
            # Detect the language of the text
            # language_code is 2 character code
            lang_code_2chr = detect(input_text)
            language_obj = langcodes.get(lang_code_2chr)
            language_name = language_obj.display_name()
            lang_code_3chr = language_obj.to_alpha3()

            
            if return_as in ["full_name"]:
                ans = language_name
            elif return_as in ["2_chr_code"]:
                ans = lang_code_2chr
            elif return_as in ["3_chr_code"]:
                ans = lang_code_3chr
            elif return_as in ["langcodes_obj"]:
                ans = language_obj

            return ans
        except Exception as e:
            err_str = f"Language detection failed: {str(e)}"
            return False
        
    elif isinstance(input_text, list):
        out_list = []
        for text in input_text:
            detect_lang = detect_language(text, return_as = return_as)
            out_list.append(detect_lang)
        return out_list
    elif isinstance(input_text, pd.Series):
        # not tested this part yet
        unique_text = pd.Series(input_text.unique())
        full_text = unique_text.str.cat(sep=' ')
        detect_lang = detect_language(full_text,return_as)
        return detect_lang

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