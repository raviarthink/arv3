import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes
import numpy as np
import av

st.title("OpenCV Filters on Video Stream")

filter = "none"

def transform(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")

    if filter == "blur":
        img = cv2.GaussianBlur(img, (21, 21), 0)
    elif filter == "canny":
        img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
    elif filter == "grayscale":
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    elif filter == "sepia":
        kernel = np.array(
            [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
        )
        img = cv2.transform(img, kernel)
    elif filter == "invert":
        img = cv2.bitwise_not(img)
    elif filter == "none":
        pass

    return av.VideoFrame.from_ndarray(img, format="bgr24")

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

with col1:
    if st.button("None"):
        filter = "none"
with col2:
    if st.button("Blur"):
        filter = "blur"
with col3:
    if st.button("Grayscale"):
        filter = "grayscale"
with col4:
    if st.button("Sepia"):
        filter = "sepia"
with col5:
    if st.button("Canny"):
        filter = "canny"
with col6:
    if st.button("Invert"):
        filter = "invert"

# Get IP camera URL from user input
ip_camera_url = st.text_input("Enter IP Camera URL:")

# Validate if the URL is provided
if ip_camera_url:
    webrtc_streamer(
        key="streamer",
        video_stream_url=ip_camera_url,
        video_frame_callback=transform,
        sendback_audio=False
    )
else:
    st.write("Please enter the IP camera URL.")

