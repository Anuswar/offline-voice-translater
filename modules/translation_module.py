from transformers import MarianMTModel, MarianTokenizer

# Initialize translation models and tokenizers for English to Hindi
model_name_en_hi = 'Helsinki-NLP/opus-mt-en-hi'
tokenizer_en_hi = MarianTokenizer.from_pretrained(model_name_en_hi)
model_en_hi = MarianMTModel.from_pretrained(model_name_en_hi)

def translate(text, from_lang, to_lang):
    if from_lang == 'en' and to_lang == 'hi':
        inputs = tokenizer_en_hi.encode(text, return_tensors='pt', max_length=512, truncation=True)
        outputs = model_en_hi.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
        return [tokenizer_en_hi.decode(t, skip_special_tokens=True) for t in outputs]
