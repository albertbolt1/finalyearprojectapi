from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlantDiseaseImageSerializer
from keras.models import load_model
from keras.preprocessing import image
from django.http.response import JsonResponse
import numpy as np
def prepare(img_path):
	#img = image.load_img(img_path, target_size=(256,256))
    img = image.load_img(img_path, target_size=(384,384))
    x = image.img_to_array(img)
    x = x/255
    return np.expand_dims(x, axis=0)

class MyImageView(APIView):
		parser_classes = (MultiPartParser, FormParser)
		def post(self, request, *args, **kwargs):
				serializer = PlantDiseaseImageSerializer(data=request.data)
				if serializer.is_valid():
						serializer.save()
						name=serializer.data['plantimage'][1::]
						model=load_model('./models/plantddusingresnet50of8epochs.h5')
						model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
						result = model.predict([prepare(name)])
						classes=['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
						classresult=np.argmax(result,axis=1)
						a=classes[classresult[0]]
						return JsonResponse({"disease":a}, status=status.HTTP_201_CREATED)
				else:
						return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)