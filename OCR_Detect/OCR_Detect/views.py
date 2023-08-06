"""
to render html web pages
"""
#from django.http import HttpResponse
import os
from django.conf import settings
from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from django.core.files.storage import default_storage
import easyocr
import numpy as np
from PIL import Image
from io import BytesIO
import pytesseract
print(pytesseract.__version__)

model_checkpoint = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForTokenClassification.from_pretrained(model_checkpoint)

nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)



def home_view(request):
    lst = []
    if request.method == "POST":
        #
        file = request.FILES["imageFile"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.url(file_name).lstrip("/media/")
        media_root = settings.MEDIA_ROOT
        full_file_path = os.path.abspath(os.path.join(media_root, file_url))
        print("Full file path:", full_file_path)

        if default_storage.exists(file_name):
            print("File exists!")

        else:
            print("File does not exist!")
    

        #text = reader.readtext(file_url)
        with open(full_file_path, "rb") as image_file:
            pil_image = Image.open(image_file)

            # Now you can pass the PIL image to the easyocr reader
            extracted_text = pytesseract.image_to_string(pil_image)
            segments = extracted_text.split('\n')
            for segment in segments:
                ner_text_results = nlp(extracted_text)
                for val in ner_text_results:
                    if 'entity_group' in val and 'word' in val and 'score' in val:
                        lst.append([val['entity_group'], val['word'], val['score']])
            arr = np.array(lst)
            
        '''
        extracted_text = [val[1] for val in text]
        ner_text_results = nlp(extracted_text)
        
        for val in ner_text_results:
            if len(val) > 0:
                lst.append([val[0]['entity_group'], val[0]['word'], val[0]['score']])
        arr = np.array(lst)
        '''
        return render(request, 'index.html', {'predictions': arr})
    else:
        return render(request, 'index.html')



def User(request):
    username = request.GET['username']
    return render(request, 'user.html', {'username': username})