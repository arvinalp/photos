import streamlit as st
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from PIL import Image
import requests
import io

# Configure Cloudinary
cloudinary.config(
    cloud_name="dx6luakep",
    api_key="661933616146216",
    api_secret="bu-WDRjHvteqWeowPkVOwYwpGLs",
    secure=True
)

# Streamlit app for replacing items using Cloudinary's Gen Fill
st.title("Image Replace with Cloudinary's Gen Fill")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded image
    st.image("temp_image.jpg", caption="Uploaded Image", use_column_width=True)

    # Input fields for replacing items
    item_to_replace = st.text_input("Item to Replace", "sweater")
    replace_with = st.text_input("Replace With", "leather jacket with pockets")

    # Generate button for replacement
    if st.button("Replace Item"):
        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload("temp_image.jpg", public_id="replace-image")

        # Generate the replacement image URL
        replacement_effect = f"gen_replace:from_{item_to_replace};to_{replace_with}"
        replaced_image_url, _ = cloudinary_url(
            "replace-image",
            effect=replacement_effect
        )

        # Load images
        original_image = Image.open("temp_image.jpg")

        # Fetch the transformed image from the generated URL
        response = requests.get(replaced_image_url)
        transformed_image = Image.open(io.BytesIO(response.content))

        # Display slider
        st.subheader("Compare Images")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(original_image, caption="Original Image", use_column_width=True)

        with col2:
            st.image(transformed_image, caption="Transformed Image", use_column_width=True)


