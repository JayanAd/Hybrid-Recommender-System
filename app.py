import streamlit as st
from content_based_filtering import content_recommendation
from scipy.sparse import load_npz
import pandas as pd
from collaborative_filtering import collaborative_recommendation
from numpy import load

cleaned_data_path = "data/cleaned_data.csv"
songs_data = pd.read_csv(cleaned_data_path)

transformed_data_path = "data/transformed_data.npz"
transformed_data = load_npz(transformed_data_path)


track_ids_path = "data/track_ids.npy"
track_ids = load(track_ids_path, allow_pickle=True)

filtered_data_path = "data/collab_filtered_data.csv"
filtered_data = pd.read_csv(filtered_data_path)

interaction_matrix_path = "data/interaction_matrix.npz"
interaction_matrix = load_npz(interaction_matrix_path)


st.title("Welcome to the Song Recommender")
st.write("### Enter the name of the song and recommender will suggest similar songs.")

song_name = st.text_input("Enter a song name: ")
st.write("You entered: ", song_name)

artist_name = st.text_input("Enter artist name: ")
st.write("You entered: ", artist_name)

song_name = song_name.lower()
artist_name = artist_name.lower()

k = st.selectbox("How many recommendations do you want?", [5, 10, 15, 20], index=1)

filtering_type = st.selectbox(
    "Select the type of filtering:", ["Content Based", "Collaborative"]
)

if filtering_type == "Content Based":
    if st.button("Get Recommendations"):
        if (
            (songs_data["name"] == song_name) & (songs_data["artist"] == artist_name)
        ).any():
            st.write("Recommendations for", f"**{song_name}**")
            recommendations = content_recommendation(
                song_name, artist_name, songs_data, transformed_data, k
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

elif filtering_type == "Collaborative":
    if st.button("Get Recommendations"):
        if (
            (filtered_data["name"] == song_name)
            & (filtered_data["artist"] == artist_name)
        ).any():
            st.write("Recommendations for", f"**{song_name}** by **{artist_name}**")

            recommendations = collaborative_recommendation(
                song_name=song_name,
                artist_name=artist_name,
                songs_data=filtered_data,
                track_ids=track_ids,
                interaction_matrix=interaction_matrix,
                k=k,
            )
            # Display Recommendations
            for ind, recommendation in recommendations.iterrows():
                song_name = recommendation["name"].title()
                artist_name = recommendation["artist"].title()

                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
                elif ind == 1:
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
                else:
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
