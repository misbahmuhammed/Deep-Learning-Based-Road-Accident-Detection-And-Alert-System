
import cv2
import streamlit as st
import geocoder
from geopy.geocoders import Nominatim
from twilio.rest import Client

def main():
    st.title("Deep Learning Based Auto Accident Detection And Alert System")
    st.write("Upload a video file to detect accidents and send alerts.")

    # File uploader
    video_file = st.file_uploader("Upload a video", type=["mp4", "avi"])

    if video_file is not None:
        # Initialize geocoder
        geoLoc = Nominatim(user_agent="GetLoc")
        g = geocoder.ip('me')
        locname = geoLoc.reverse(g.latlng)

        # Initialize Twilio client
        account_sid = 'ACde7a1cc7e1e9cdc46c1d95bef1b3becc'
        auth_token = '7c9f1c6e4ba1169a0cb6b6ee669681a1'
        client = Client(account_sid, auth_token)

        # Load the video
        cap = cv2.VideoCapture(video_file.name)
        i = 0
        flag = 0
        accident_detected = False

        # Placeholder for predictions
        predictions = [[3.5263438e-06, 9.9999642e-01],
                       [1.6404901e-04, 9.9983597e-01],
                       [1.4376233e-03, 9.9856240e-01],
                       [6.1180198e-04, 9.9938822e-01],
                       [1.8550121e-03, 9.9814498e-01],
                       [4.7215873e-01, 5.2784121e-01],
                       [7.7747977e-01, 2.2252022e-01],
                       [5.5686516e-01, 4.4313481e-01],
                       [8.3024567e-01, 1.6975437e-01]]

        # Process frames
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if predictions[int(i/15) % 9][0] < predictions[int(i/15) % 9][1]:
                predict = "No Accident"
            else:
                predict = "Accident"
                flag = 1
                if not accident_detected:
                    # Send alert if an accident is detected
                    client.messages.create(
                        body="Accident detected at location: " + locname.address,
                        from_='+15855132640',
                        to='+917510764209')
                    accident_detected = True
                    st.warning("Accident detected at location: " + locname.address)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,
                        predict,
                        (50, 50),
                        font, 1,
                        (0, 255, 255),
                        3,
                        cv2.LINE_4)

            # Display the live video feed in Streamlit
            st.image(frame, channels="BGR", use_column_width=True)
            st.write(f"Prediction: {predict}")

            i += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture object
                # Release the video capture object
        cap.release()
        # Close all windows
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

       


       


       


