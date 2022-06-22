import json
import zipfile
# from convlab2.util.multiwoz.multiwoz_slot_trans import REF_SYS_DA
from collections import defaultdict

def read_zipped_json(filepath, filename):
    archive = zipfile.ZipFile(filepath, 'r')
    return json.load(archive.open(filename))

def extract_intent_dict(data):
    intent_dict = defaultdict(list)
    for dialogs in list(data.values()):
        for turn, meta in enumerate(dialogs['log']):
            if turn % 2 == 1:
                # skip system turn
                continue
            text = meta['text']
            text = text.strip().split()
            spans = meta["span_info"]
            if len(spans) > 0:
                # skip when no slots needed
                for idx, span in enumerate(spans):
                    if idx == 0:
                        intent = span[0]
                    if len(text) <= span[4] or len(text) <= span[3]:
                        # skip invalid span
                        continue
                    # print("TEXT:",text)
                    # print("SPAN:",span)
                    # print("_____________________________________")
                    slot = span[1]
                    text[span[3]] = "[" + text[span[3]]
                    text[span[4]] = text[span[4]] + "]" + r'{' + slot + r'}'
                intent_dict[intent].append(" ".join(text))
    return intent_dict

def write_to_yaml(intent, yaml_name):
    with open(yaml_name, 'w') as f:
        f.writelines(r'version: "1.0" # training dataset format version' + '\n')
        f.writelines(r'domain: "cross" # domain name' + '\n')
        f.writelines('\n')
        f.writelines('nlu:'+ '\n')
        for key, vals in intent.items():
            f.writelines(r'- intent: ' + key + '\n')
            f.writelines(r'  queries:' + '\n')
            for val in vals:
                f.writelines(r'   - ' + val + '\n')
            f.writelines('\n')

       



if __name__=="__main__":
    for s in ['train', 'val', 'test']:
        data = read_zipped_json(s + '.json.zip', s + '.json')
        intent_dict = extract_intent_dict(data)
        print(s + " has ", len(intent_dict), " intents.")
        write_to_yaml(intent_dict, s + '.yaml')


                

