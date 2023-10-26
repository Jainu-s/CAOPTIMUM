
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

'''
This code takes HTML code, a sentence, a double-quoted word, and a driver as input. It parses the
 HTML code to find input and textarea tags, filters out hidden inputs, and searches for specific 
 attributes that match the given sentence using fuzzy string matching. If a match is found, 
 it returns the attribute key and value. It also considers currency-related synonyms. 
 If no match is found, it returns None for both key and value.
'''

def find_input_textarea(html_code,sentence,double_quoted_word,driver):

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_code, 'html.parser')

    ''' This is important'''
    input_tags = soup.find_all(['input', 'textarea'])



    def remove_hidden_inputs(input_tags):
        filtered_tags = []
        for tag in input_tags:
            if 'style="display: none"' not in str(tag):
                filtered_tags.append(tag)
        return filtered_tags

    filtered_inputs = remove_hidden_inputs(input_tags)
    print('Filtered Inputs:',filtered_inputs)


    # This for those input tags which doesn't have meaningful values so we try with keys and current requirement for money
    money_synonyms = ['currency','cash', 'currencyvalue', 'dollars', 'funds', 'amount', 'rupee']

    # Match each value in the tag attributes with the search sentence using fuzzy token set ratio
    all_attr_list = []
    for each_tag in filtered_inputs:
        print('Each Tag:',each_tag)
        for key, value in each_tag.attrs.items():
            for i in money_synonyms:
                if (i in str(key)) or  (i in str(value)):
                    print('Curreny Triggered')
                    return key,value
            for word in sentence.split():
                #if value is not None:
                if key != 'type':
                    if value != double_quoted_word.replace('"', ''):
                        att_score = fuzz.token_set_ratio(str(value),sentence)
                        sent_score = fuzz.token_set_ratio(word,value)
                        if att_score > sent_score and att_score > 70:
                            all_attr_list.append([key,value,att_score])
                        elif sent_score > att_score and  sent_score > 70:
                            all_attr_list.append([key,value, sent_score])
                        elif word in value:

                            found_sublists = [sublist for sublist in all_attr_list if [key,value] == sublist[:2]]
                            print('found_sublist:',found_sublists)
                            if not found_sublists:

                                all_attr_list.append([key,value])
                                return key,value

                            else:
                                return key,value

                    elif value == double_quoted_word.replace('"', ''):
                        value = ''
                        return key,value






    print('all_attr_list:',all_attr_list)

    if all_attr_list:
        max_sublist = max(all_attr_list, key=lambda x: x[2])
        max_key, max_value, max_number = max_sublist
        if max_value == 'password' or 'Password':
            return max_key, max_value
    else:
        return None,None





