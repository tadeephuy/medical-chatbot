from underthesea import word_tokenize
import json

def load_json_lines(path):
    list_data = []
    for line in open(path, 'r'):
        list_data.append(json.loads(line))
    return list_data

def tokenize(sentence):
    """
    word tokenizer
    """
    tokens = word_tokenize(sentence)
    return tokens


def create_seq(list_tokens, seq_len = 5):
    """
    window sliding with window_size = seq_len
    """
    sequences = []
    # if the number of tokens in 'text' is greater than 5
    if len(list_tokens) > seq_len:
        for i in range(seq_len, len(list_tokens)):
            # select sequence of tokens
            seq = list_tokens[i-seq_len:i+1]
            # add to the list
#             sequences.append(" ".join(seq))
            sequences.append(seq)
        
    return sequences
#     else:
#         print('list_tokens',list_tokens)
#         return [list_tokens]
    
def get_integer_seq(token2int,list_token):
    return [token2int[w] for w in list_token]


def get_batches(arr_x, arr_y, batch_size):
         
    # iterate through the arrays
    prv = 0
    for n in range(batch_size, arr_x.shape[0], batch_size):
        x = arr_x[prv:n,:]
        y = arr_y[prv:n,:]
        prv = n
        yield x, y