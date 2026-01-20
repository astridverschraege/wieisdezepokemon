import streamlit as st
import random
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Wie is deze Pokémon?", page_icon="🎮")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #b6fcb6 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #a4f5a4 !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #003300 !important;
    }
    input[type="text"] {
        background-color: #e8ffe8 !important;
        color: #003300 !important;
        border: 2px solid #009900 !important;
        border-radius: 6px !important;
    }
    .stButton>button {
        background-color: #009900 !important;
        color: white !important;
        border-radius: 6px !important;
        border: 2px solid #006600 !important;
    }
    .stButton>button:hover {
        background-color: #00bb00 !important;
        border-color: #008800 !important;
    }
    .stAlert {
        background-color: #d9ffd9 !important;
        color: #003300 !important;
        border-left: 6px solid #009900 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Wie is deze Pokémon?")

def get_pokemon():
    random_id = random.randint(1, 151)
    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
    data = requests.get(url).json()
    name = data["name"]
    sprite_url = data["sprites"]["front_default"]
    if not sprite_url:
        return get_pokemon()
    img_data = requests.get(sprite_url).content
    img = Image.open(BytesIO(img_data)).convert("RGBA")
    return name, img

def make_silhouette(img):
    alpha = img.split()[-1]
    black = Image.new("RGBA", img.size, (0, 0, 0, 255))
    silhouette = Image.new("RGBA", img.size, (0, 0, 0, 0))
    silhouette.paste(black, mask=alpha)
    return silhouette

if "pokemon_name" not in st.session_state:
    st.session_state.pokemon_name, st.session_state.pokemon_img = get_pokemon()
    st.session_state.revealed = False

guess = st.text_input("Jouw gok...")

if st.button("Raad!"):
    if guess.strip().lower() == st.session_state.pokemon_name.lower():
        st.session_state.revealed = True
        st.success(f"🎉 Juist! Het is {st.session_state.pokemon_name.capitalize()}!")
        st.rerun()
    else:
        st.error("❌ Nope, probeer opnieuw!")

if st.session_state.revealed:
    st.image(st.session_state.pokemon_img, width=200)
else:
    silhouette = make_silhouette(st.session_state.pokemon_img)
    st.image(silhouette, width=200)

if st.button("Nieuwe Pokémon"):
    st.session_state.pokemon_name, st.session_state.pokemon_img = get_pokemon()
    st.session_state.revealed = False
    st.rerun()