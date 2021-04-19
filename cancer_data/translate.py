import json
from googletrans import Translator
from tqdm import tqdm

if __name__ == '__main__':
    from google_trans_new import google_translator

    translator = google_translator()
    # translate_text = translator.translate('rectal cancer',lang_tgt='vi')

    # translator = Translator()
    # data = json.loads(open('database.json',))
    data = json.load(open('database.json', encoding='utf-8'))

    trans_data = []
    for i, sample in tqdm(enumerate(data)):
        new_sample = {
            "source": translator.translate(sample['source'], lang_tgt='vi'),
            'relation': sample['relation'],
            'target':  translator.translate(sample['target'], lang_tgt='vi'),
            'original_text':  translator.translate(sample['original_text'], lang_tgt='vi'),
        }
        trans_data.append(new_sample)
        if i % 100 == 0:
            print(new_sample)
        # translations = translator.translate([], dest='vi').text
    file_out = open('database_vi.json', 'w')
    for item in trans_data:
        item_str = str(item).replace(r"'", r'"')
        file_out.write(item_str) 
        file_out.write('\n')
    