import base64
import mimetypes
import os
from io import BytesIO
from typing import Optional

import pandas as pd
import streamlit as st
from logzero import logger
from simplesingletable import DynamoDbMemory

from supersullytools.utils.media_manager import MediaManager, MediaType

st.set_page_config(layout="wide")


def setup_media_manager():
    # Placeholder function to set up the MediaManager
    # Replace with your actual implementation
    dynamodb_memory = DynamoDbMemory(logger=logger, table_name=os.environ.get("DYNAMODB_TABLE"))
    return MediaManager(
        bucket_name=os.environ.get("S3_BUCKET"),
        logger=logger,
        dynamodb_memory=dynamodb_memory,
        global_prefix="media-manager-testing",
    )


def detect_media_type(file_name: str) -> Optional[MediaType]:
    mime_type, _ = mimetypes.guess_type(file_name)
    if mime_type:
        if mime_type.startswith("image"):
            return MediaType.image
        elif mime_type.startswith("audio"):
            return MediaType.audio
        elif mime_type.startswith("video"):
            return MediaType.video  # Assuming "video" is a valid media type in your MediaManager
        elif mime_type == "application/pdf":
            return MediaType.pdf
        elif mime_type.startswith("text"):
            return MediaType.text
    return None


def display_content(contents, media_type: MediaType):
    if media_type == "image":
        st.image(contents, caption="Image")
    elif media_type == "audio":
        st.audio(contents)
    elif media_type == "video":
        st.video(contents)
    else:
        st.write("Unable to display contents")


# Initialize the media manager
media_manager = setup_media_manager()

st.title("Media Manager Streamlit App")

# File upload section
st.header("Upload Media")
uploaded_file = st.file_uploader(
    "Choose a file",
)

default_media_type = None
if uploaded_file:
    media_types = list(MediaType)
    st.write(mimetypes.guess_type(uploaded_file.name)[0])
    try:
        default_media_type = media_types.index(detect_media_type(uploaded_file.name))
    except ValueError:
        pass

media_type: MediaType = st.selectbox(
    "Select media type", options=list(MediaType), index=default_media_type, format_func=lambda x: x.value
)

if uploaded_file is not None and media_type:
    st.write("Filename:", uploaded_file.name)
    bytes_data = uploaded_file.read()
    file_obj = BytesIO(bytes_data)

    try:
        preview = media_manager.generate_preview(uploaded_file, media_type)
        st.image(preview, media_type)
    except Exception as e:
        st.error(f"Failed to generate preview for file: {str(e)}")
    if st.button("Upload"):
        try:
            metadata = media_manager.upload_new_media(uploaded_file.name, media_type, file_obj)
            st.success(f"File uploaded successfully! Media ID: {metadata.resource_id}")
        except Exception as e:
            st.error(f"Failed to upload file: {str(e)}")


st.header("Recent Uploads")

data = []
previews = []


@st.cache_data
def get_preview_image_base64(media_id: str) -> str:
    preview_content = media_manager.retrieve_media_preview(media_id)
    return base64.b64encode(preview_content).decode("utf-8")


for media in media_manager.list_available_media(num=25, oldest_first=False):
    media_dict = media.model_dump(
        mode="json", exclude={"created_at", "updated_at", "file_size_bytes", "preview_size_bytes"}
    )
    data.append(media_dict)
    previews.append(get_preview_image_base64(media.resource_id))

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Add a column for the preview images
df["Preview"] = [f"data:image/jpeg;base64,{preview}" for preview in previews]

# Display the DataFrame with custom column configuration
st.dataframe(
    df,
    column_config={
        "Preview": st.column_config.ImageColumn(
            label="Preview Image",
            help="Preview of the uploaded media",
            width="small",
        ),
    },
    use_container_width=True,
)


# Retrieve metadata section
st.header("Retrieve Metadata")
media_id = st.text_input("Enter media ID to retrieve metadata")
if st.button("Retrieve Metadata"):
    try:
        metadata = media_manager.retrieve_metadata(media_id)
        st.json(metadata.dict())
    except Exception as e:
        st.error(f"Failed to retrieve metadata: {str(e)}")

# Retrieve content section
st.header("Retrieve Content")
media_id_content = st.text_input("Enter media ID to retrieve content")
if st.button("Retrieve Content"):
    try:
        contents_metadata, contents = media_manager.retrieve_media_metadata_and_contents(media_id_content)
        st.write(contents_metadata.src_filename)
        display_content(contents, contents_metadata.media_type)
        st.download_button("Download Content", data=contents, file_name=contents_metadata.src_filename)
    except Exception as e:
        st.error(f"Failed to retrieve content: {str(e)}")

# Retrieve preview section
st.header("Retrieve Preview")
media_id_preview = st.text_input("Enter media ID to retrieve preview")
if st.button("Retrieve Preview"):
    try:
        preview_metadata = media_manager.retrieve_metadata(media_id_preview)
        preview_contents = media_manager.retrieve_media_preview(media_id_preview)
        st.image(preview_contents, preview_metadata.media_type)
    except Exception as e:
        st.error(f"Failed to retrieve preview: {str(e)}")


# Retrieve preview section
st.header("Delete Media")
delete_media_id = st.text_input("Enter media ID to delete; this cannot be undone!")
if st.button("Delete Media", type="primary"):
    try:
        preview_metadata = media_manager.delete_media(delete_media_id)
        st.info("Deleted")
    except Exception as e:
        st.error(f"Failed to delete media: {str(e)}")
