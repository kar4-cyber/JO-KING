import json
import urllib.request
import streamlit as st

st.set_page_config(page_title="JO-KING", page_icon="👑", layout="centered")

st.title("👑 JO-KING 👑")

categories = [
    "Dad Jokes",
    "General Puns",
    "Programming",
    "Animals",
    "Food",
    "Science",
    "History",
    "Sports",
    "Music",
    "Movies",
    "School",
    "Work",
    "Spooky",
    "Christmas",
    "Any"
]

category = st.selectbox("Choose Joke Category:", categories)

def fetch_live_joke(cat):
    try:
        if cat == "Dad Jokes":
            url = "https://icanhazdadjoke.com/"
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "JO-KING App"})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode())
                return data["joke"]
        else:
            api_cat = "Pun" if cat == "General Puns" else ("Any" if cat in ["History", "Sports", "Music", "Movies", "School", "Work", "Animals", "Food", "Science"] else cat)
            
            if cat in ["History", "Sports", "Music", "Movies", "School", "Work", "Animals", "Food", "Science"]:
                url = f"https://v2.jokeapi.dev/joke/Any?contains={cat.lower()}&safe-mode"
            else:
                url = f"https://v2.jokeapi.dev/joke/{api_cat}?safe-mode"

            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode())
                
                if data.get("error"):
                    url_fallback = "https://icanhazdadjoke.com/"
                    req_fb = urllib.request.Request(url_fallback, headers={"Accept": "application/json", "User-Agent": "JO-KING App"})
                    with urllib.request.urlopen(req_fb, timeout=4) as resp_fb:
                        return json.loads(resp_fb.read().decode())["joke"]
                        
                if data["type"] == "single":
                    return data["joke"]
                else:
                    return f"{data['setup']} - {data['delivery']}"
    except Exception:
        url_fallback = "https://icanhazdadjoke.com/"
        req_fb = urllib.request.Request(url_fallback, headers={"Accept": "application/json", "User-Agent": "JO-KING App"})
        with urllib.request.urlopen(req_fb, timeout=4) as resp_fb:
            return json.loads(resp_fb.read().decode())["joke"]

if "current_joke" not in st.session_state:
    st.session_state.current_joke = fetch_live_joke(category)

if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.info(st.session_state.current_joke)

col1, col2 = st.columns(2)

with col1:
    if st.button("Regenerate"):
        st.session_state.current_joke = fetch_live_joke(category)
        st.rerun()

with col2:
    if st.button("Save Favorite"):
        if st.session_state.current_joke not in st.session_state.favorites:
            st.session_state.favorites.append(st.session_state.current_joke)
            st.success("Saved!")

st.write("---")
st.subheader("📌 Your Saved Favorites")

for idx, fav in enumerate(st.session_state.favorites, 1):
    st.write(str(idx) + ". " + fav)