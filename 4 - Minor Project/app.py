import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from pickle import load

# To remove the unneccessary error
st.set_option("deprecation.showfileUploaderEncoding", False)

@st.cache_resource()
def load_model_and_classes():
    model = load_model("model.h5")
    with open("classes.pkl", "rb") as f:
        classes = load(f)
    return model, classes
model, classes = load_model_and_classes()

# Inject custom CSS to reduce padding from above
st.markdown(
    """
    <style>
    .stApp {
        margin-top: -80px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    # Plant Diseases Detection
    """
)

file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
def predictImage(image_data):
  numpydata = np.asarray(image_data)
  imageNumpy = numpydata.reshape(1, 256, 256, 3)
  predict = model.predict(imageNumpy)
  print(predict)
  return classes[np.argmax(predict)]

if file is None:
   st.write("Please upload a valid image (jpg, png, jpeg)!")
else:
   image = Image.open(file)
   resized_image = image.resize((50, 50))
   st.image(image, use_column_width=False)
   predict = predictImage(image)
   string = "Image most likely is: "+predict+" Disease"
   st.success(string)