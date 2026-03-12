import streamlit as st
import pandas as pd

# Connect to Sheet
SHEET_ID = "YOUR_ID_HERE"
url = f"https://docs.google.com/spreadsheets/d/1lj92K_9shLGq5qY7pEzyHFLFn6rk3eEDb3NQjWbVVds/gviz/tq?tqx=out:csv"

df = pd.read_csv(url)

# --- DEBUG LINE: This will show you exactly what the columns are named ---
st.write("Current Columns found in Sheet:", df.columns.tolist())

# Adjust the name below based on what you see in the list above!
player_name = st.selectbox("Pick a player:", df.iloc[:, 0]) # This picks the 1st column regardless of name

# 2. Setup the App UI
st.title("⚾ 2026 WBC International Scout")
st.markdown("Find the MLB twin for international stars.")

# Load Data
df = pd.read_csv(url)

# 3. User Interaction
player_name = st.selectbox("Pick a player to scout:", df["Player's Name"])
player_info = df[df["Player's Name"] == player_name].iloc[0]

if st.button("Get Scouting Report"):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    prompt = f"""
    Act as a professional MLB scout. 
    Player: {player_info["Player's name"]}
    Position: {player_info["Position"]}
    Current Team: {player_info["Current professional team"]}
    League: {player_info["League"]}
    
    Task: Give a 2-sentence scouting report and name one current MLB player who is their closest 'twin' in terms of playstyle.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    st.subheader(f"Scout's Take on {player_name}")
    st.info(response.choices[0].message.content)
