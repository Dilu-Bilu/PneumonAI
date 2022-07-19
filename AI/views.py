from cgi import test
from re import template
from django.shortcuts import render
from django.views import View
from .forms import PneumoniaForm
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from keras.utils import np_utils
from PIL import Image
from django.core.files.storage import default_storage
from io import BytesIO
from django.contrib import messages

# Create your views here.
class AIClassificationView(View):
    template_name = "pages/home.html"

    def get(self, request, *args, **kwargs):
        form = PneumoniaForm()
        context = {
            "form": form 
        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = PneumoniaForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['image']
            file_name = "pic.jpg"
            file_name_2 = default_storage.save(file_name, img)
            file_url = default_storage.url(file_name_2)
            classifier = load_model('AI/pneumonia_model.h5')

            #loading new image from directory
            # test_image = img.thumbnail(64,64)
            test_image = image.load_img("fyrewatchai/" + file_url, target_size = (64, 64))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis = 0)

            #making detection
            result = classifier.predict(test_image)
            if result[0][0] == 1:
                status = 'Pneumonia Detected'
                messages.warning(self.request, "This Patient Has Pneumonia | Treatment is advised")
            else:
                status = 'No Pneumonia Detected'
                messages.success(self.request, "Everything is alright!")
            #Save data to django model
            context = {
                "form": form,
                "status": status
            }
                        
        else:
            status = "Your Form failed"
            context = {
                "form": form,
                "status": status,
            }
        return render(request, self.template_name, context)
