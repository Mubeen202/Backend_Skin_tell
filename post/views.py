from .serializers import PostSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from PIL import Image
import tensorflow as tf
import seaborn as sns
import random
import os,keras
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
import cv2
import pandas as pd
from tensorflow.keras.applications import  VGG19,EfficientNetB0,VGG16,InceptionV3,ResNet50,EfficientNetB3
# Get the absolute path to the model file
# model_path = os.path.join(os.getcwd(), 'AI_Model', 'FNAI_cosmetic_model.h5')
# model_path2 = os.path.join(os.getcwd(), 'AI_Model', 'FNAI_type_model.h5')

# Load the Keras model
# model1 = keras.models.load_model(model_path)
# model2 = keras.models.load_model(model_path2)
# vgg_model1 = EfficientNetB0(weights = 'imagenet',  include_top = False, input_shape = (180,180, 3)) 
# Function to classify image and print results
# def classify_image(img): 
#     new_size = (180, 180)
#     resized_img = img.resize(new_size)

#     image=resized_img
#     #image.append(resized_img)
    
#     img_array = np.asarray(image)
#     img_array = img_array[np.newaxis, ...]
#     features_test=vgg_model1.predict(img_array)
#     num_test2=img_array.shape[0]
#     x_t=features_test.reshape(num_test2,-1)
#     probs = model1.predict(x_t)  # Make predictions using the model
#     total = np.sum(probs)  # Total probability sum for normalization
#     percentages = (probs / total) * 100
#     for i, percentage in enumerate(percentages[0]):
#         if i == 0:
#             dark_spot=(f"Dark Spots : {percentage:.2f}%")
            

#         elif i == 1:
#             puffy_eyes=(f"Puffy Eyes : {percentage:.2f}%")
           

#         elif i == 2:
#             wrinkles=(f"Wrinkles : {percentage:.2f}%")
#      # Return the values after the loop
#     return dark_spot, puffy_eyes, wrinkles
          

# vgg_model = ResNet50(weights = 'imagenet',  include_top = False, input_shape = (180,180, 3)) 
# # Function to classify image and print results
# def classify_type(img):
#     new_size = (180, 180)
#     resized_img = img.resize(new_size)
#     image=resized_img
#     img_array = np.asarray(image)
#     img_array = img_array[np.newaxis, ...]
#     features_test=vgg_model.predict(img_array)
#     num_test2=img_array.shape[0]
#     x_t=features_test.reshape(num_test2,-1)
#     probs = model2.predict(x_t)  # Make predictions using the model
#     predctionClass = np.argmax(probs, axis = 1)

#     total = np.sum(probs)  # Total probability sum for normalization
#     percentages = (probs / total) * 100
#     for i, percentage in enumerate(percentages[0]):
        
#         # print(f"Class {i + 1}: {percentage:.2f}%")
#         if (percentages[0][0] > 15 and percentages[0][0] < 80 and percentages[0][1] > 15 and percentages[0][1] < 80):
#             return(" MIXED SKIN")
#         elif(percentages[0][3] > 15 and percentages[0][3] < 80 and percentages[0][1] > 15 and percentages[0][1] < 80):
#             return(" MIXED SKIN")
#         elif(predctionClass == 0):
#             return(" DRY SKIN")
#         elif(predctionClass == 1):
#             return(" OILY SKIN")
#         elif(predctionClass == 2):
#             return(" SENSITIVE SKIN")
#         elif(predctionClass == 3):
#             return(" NORMAL SKIN")    
        
    


class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            #  array = np.array([1, 2, 3], dtype=np.int32)
            imagee = request.FILES['image']
            file_name = str(imagee)
            print(f'[INFO] File Name: {file_name}')
            with open("media/post_images/"+file_name, 'wb+') as f:
                for chunk in imagee.chunks():
                    f.write(chunk)
            img = Image.open(imagee)

            # class_type=classify_type(img)
            print('*****************************************break************************')
            # class_image=classify_image(img)
            return Response({'data':posts_serializer.data, "classify_type": class_type, "classify_image": class_image }, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)