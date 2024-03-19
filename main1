from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, ClientSettings
import av
import cv2
import numpy as np
import streamlit as st

class OpenCVFilter(VideoTransformerBase):
    def __init__(self):
        self.filter = "none"

    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        if self.filter == "blur":
            img = cv2.GaussianBlur(img, (21, 21), 0)
        elif self.filter == "canny":
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
        elif self.filter == "grayscale":
            img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        elif self.filter == "sepia":
            sepia_matrix = np.array([[0.393, 0.769, 0.189],
                                     [0.349, 0.686, 0.168],
                                     [0.272, 0.534, 0.131]])
            img = cv2.transform(img, sepia_matrix)
        elif self.filter == "invert":
            img = cv2.bitwise_not(img)
        elif self.filter == "none":
            pass

        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def filter_changed(self, new_filter):
        self.filter = new_filter

def main():
    st.title("OpenCV Filters on Video Stream")

    filters = ["none", "blur", "canny", "grayscale", "sepia", "invert"]
    selected_filter = st.selectbox("Select Filter", filters)

    open_cv_filter = OpenCVFilter()
    open_cv_filter.filter_changed(selected_filter)

    # Get IP camera URL from user input
    ip_camera_url = st.text_input("Enter IP Camera URL:")

    if ip_camera_url:
        webrtc_ctx = webrtc_streamer(
            key="opencv-filter",
            video_transformer_factory=OpenCVFilter,
            async_transform=True,
            client_settings=ClientSettings(
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
                media_stream_constraints={"video": {"mandatory": {"minWidth": "640", "minHeight": "480"}}},
            ),
            source_video=ip_camera_url,
        )
    else:
        st.write("Please enter the IP camera URL.")

if __name__ == "__main__":
    main()
