import streamlit as st
from content_based_filtering import content_recommendation
from scipy.sparse import load_npz
import pandas as pd

# load the data
cleaned_data_path = "data/cleaned_data.csv"
songs_data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data_path = "data/transformed_data.npz"
transformed_data = load_npz(transformed_data_path)

st.title("Welcome to the Song Recommender")
st.write("### Enter the name of the song and recommender will suggest similar songs.")

song_name = st.text_input("Enter a song name: ")
st.write("You entered: ", song_name)
song_name = song_name.lower()


k = st.selectbox("How many recommendations do you want?", [5, 10, 15, 20], index=1)


if st.button("Get Recommendations"):
    if (songs_data["name"] == song_name).any():
        st.write("Recommendations for", f"**{song_name}**")
        recommendations = content_recommendation(
            song_name, songs_data, transformed_data, k
        )

        for ind, recommendation in recommendations.iterrows():
            song_name = recommendation["name"].title()
            artist_name = recommendation["artist"].title()

            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(f"### **{song_name}** by **{artist_name}**")
                st.audio(recommendation["spotify_preview_url"])
                st.write("---")
            elif ind == 1:
                st.markdown("### Next UP")
                st.markdown(f"### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation["spotify_preview_url"])
                st.write("---")
            else:
                st.markdown(f"### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation["spotify_preview_url"])
                st.write("---")
    else:
        st.write(
            f"Sorry, we couldn't find {song_name} in our database. Please try another song."
        )
