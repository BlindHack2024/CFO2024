
import torch
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def encode_text(text):

    tokens = tokenizer.encode(text, add_special_tokens=True)

    input_ids = torch.tensor(tokens).unsqueeze(0)
 
    outputs = model(input_ids)

    return outputs[0]


text = "Привет, как дела?"
encoded_text = encode_text(text)


print(encoded_text)