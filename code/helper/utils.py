import re

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def clear_special(st):
    ### save newline
    st_nl = st.replace('-\n','NEWLINE')
    word = ' '.join(re.findall('[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđA-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÍÌỈĨỊÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ0-9\!\@\#\$\%\^\&\*\(\)\'\"\:\;\<\>\?\.\,\/]+', st_nl))
    
    return word.replace('NEWLINE','')

def check_null(list_phrase):
    list_check_phrase = []
    for item in list_phrase:
        if item:
            list_check_phrase.append(item)
    return list_check_phrase