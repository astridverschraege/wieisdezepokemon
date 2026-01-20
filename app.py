import streamlit as st
import random
import requests
from io import BytesIO
from PIL import Image, ImageEnhance

st.set_page_config(page_title="Wie is deze Pokémon?", page_icon="🎮")

st.title("🎮 Wie is deze Pokémon?")
st.write("De afbeelding is verduisterd. Kan jij raden welke Pokémon dit is?")

# -----------------------------
# Pokémon ophalen
# -----------------------------
def load_pokemon():
    random_id = random.randint(1, 151)  # Gen 1
    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
    data = requests.get(url).json()
    name = data["name"]
    sprite_url = data["sprites"]["front_default"]

    img_data = requests.get(sprite_url).content
    img = Image.open(BytesIO(img_data)).convert("RGB")
    return name, img

# -----------------------------
# Silhouet (brightness 0)
# -----------------------------
def make_dark(img):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(0.0)  # exact zoals CSS brightness(0)

# -----------------------------
# State initialiseren
# -----------------------------
if "pokemon_name" not in st.session_state:
    st.session_state.pokemon_name, st.session_state.pokemon_img = load_pokemon()

# -----------------------------
# UI
# -----------------------------
dark_img = make_dark(st.session_state.pokemon_img)
st.image(dark_img, width=200)

guess = st.text_input("Jouw gok:")

if st.button("Raad!"):
    if guess.strip().lower() == st.session_state.pokemon_name.lower():
        st.success(f"🎉 Juist! Het is {st.session_state.pokemon_name.capitalize()}!")
        st.image(st.session_state.pokemon_img, width=200)
    else:
        st.error("❌ Nope, probeer opnieuw!")

# -----------------------------
# Nieuwe Pokémon knop
# -----------------------------
if st.button("Nieuwe Pokémon"):
    st.session_state.pokemon_name, st.session_state.pokemon_img = load_pokemon()
    st.rerun()