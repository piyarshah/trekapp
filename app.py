import streamlit as st
import pandas as pd

# Initialize session state for page view
if "page" not in st.session_state:
    st.session_state.page = "home"
if "participant_data" not in st.session_state:
    st.session_state.participant_data = {}

# Page setup
st.set_page_config(page_title="Trek Participant Tracker", layout="centered")

# Inject custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 500;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="title">Yanam Offbeat</div>', unsafe_allow_html=True)

pickup_info = {
    "Twin Valley Trek": {
        "Borivali National Park Bus Stop": "https://maps.app.goo.gl/qzqduuLKv4hCz1jH9",
        "JVLR": "https://goo.gl/maps/JMtCx4jS5voKcnKV6",
        "IIT Bombay": "https://goo.gl/maps/QCHpG3Y8zjJttX2w8",
        "Gandhinagar Junction Flyover": "https://goo.gl/maps/NLtzCNDeMFCerPEp7",
        "Bhandup Pumping Station": "https://goo.gl/maps/8EkZb1jHN9sHJ6vk6",
        "Rabale FOB": "https://maps.app.goo.gl/8HpgvAG5pFvfDujJ9",
        "Ghansoli Station": "https://maps.app.goo.gl/f8Qdxh7V4DbBqaJe7",
        "Lodha Xperia Mall Dombivili": "https://maps.app.goo.gl/2RvJJcPFanL5iFwm7",
        "Mahanagar Gas AMBERNATH": "https://maps.app.goo.gl/xjSkq6MmPHdahqVQ7",
        "Meeting the team directly at the base": ""
    },

    "Nanemachi Waterfall": {
        "Borivali National Park Gate": "https://maps.app.goo.gl/qzqduuLKv4hCz1jH9",
        "Gundavali Metro Station": "https://maps.app.goo.gl/5STm9EdBt2gGpCGN8",
        "Ghatkopar Bus Depot": "https://maps.app.goo.gl/mhaRWfZVT8jxuAuh7",
        "Ghatkopar Traffic Police Chowky": "https://maps.app.goo.gl/vHzm6eRPXWgxZwv48",
        "Chheda Nagar Junction Highway Chembur": "https://maps.app.goo.gl/7QmKtbjhK2SXXrRx6",
        "Vashi Plaza": "https://maps.app.goo.gl/mgz5zgyvLBywZ6LW8",
        "Below Turbhe Foot Over Bridge": "https://maps.app.goo.gl/V4FUS4qg9mQUmtwE6",
        "DY Patil Nerul FOB": "https://maps.app.goo.gl/C1GbhEFLg3M9DrY68",
        "Meeting the team directly at the base": ""
    },

    "Steps of Paradise": {
        "Mumbai": {
            "JVLR Chowk": "https://maps.app.goo.gl/5TxsbUUpg4ZcMcHJ6",
            "IIT Bombay": "https://maps.app.goo.gl/jaQLjkoRCaCfvAJG6",
            "Gandhinagar Junction": "https://maps.app.goo.gl/HFZjctLNFntNHxBVA",
            "Bhandup Pumping Station (Airoli side)": "https://maps.app.goo.gl/tRLyzMKHp8tAoqDA8",
            "Rabale Station FOB": "https://maps.app.goo.gl/WEA4UxxuQ4a5GjYx7",
            "Ghansoli Station (towards Shilphata road)": "https://maps.app.goo.gl/fM4k2Rx95eWtxckq5",
            "Xperia Mall (Dombivili)": "https://maps.app.goo.gl/cKmWTv6r6oKHXnVe7",
            "Meeting the team directly at the base": ""
        },
        "Pune": {
            "Safire Park Galleria": "https://maps.app.goo.gl/qJ3U8BHp1DpgPaai6",
            "Wakdewadi New Bus Stand": "https://maps.app.goo.gl/LhDZWqEHYNgPGHY56",
            "Bopodi Jakat Naka": "https://maps.app.goo.gl/mH9qvqPSzmD9y3Mf6",
            "Nashik Bus Stop - Nashik Phata": "https://maps.app.goo.gl/Z6sJUV5G8syRhqUo6",
            "Tata Motors Cars Showroom (Bhosari)": "https://maps.app.goo.gl/5GbUoywBPJXyZ86C8",
            "Lakshmi Energy & Fuel": "https://maps.app.goo.gl/TYB2dCVnAdboUK1t9",
            "Meeting the team directly at the base": ""
        }
    }
}

# --- Home Page ---
if st.session_state.page == "home":
    st.markdown('<div class="section-title" style="margin-bottom: 0px;">Select City</div>', unsafe_allow_html=True)
    selected_city = st.selectbox("", ["Select", "Mumbai", "Pune"])

    if selected_city == "Mumbai":
        trek_names = ["Nanemachi Waterfall", "Twin Valley Trek", "Steps of Paradise"]
    elif selected_city == "Pune":
        trek_names = ["Steps of Paradise"]
    else:
        trek_names = []

    if trek_names:
        st.markdown('<div class="section-title" style="margin-bottom: 0px;">Select Trek</div>', unsafe_allow_html=True)
        selected_trek = st.selectbox("", ["Select"] + trek_names)

        if selected_trek != "Select":
            st.markdown('<div class="section-title" style="margin-top: 24px; margin-bottom: 20px;">Upload the Google Sheet</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload the Google Sheet", type=["csv", "xlsx"], help="Upload the sheet you downloaded from Google Forms", label_visibility="collapsed")

            if uploaded_file:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
                name_col = next((col for col in df.columns if "name" in col.lower()), None)
                phone_col = next((col for col in df.columns if "whatsapp" in col.lower()), None)
                pickup_col = next((col for col in df.columns if "pickup" in col.lower()), None)

                if not all([name_col, phone_col, pickup_col]):
                    st.error("Could not identify required columns in the sheet.")
                else:
                    if selected_trek == "Steps of Paradise":
                        pickup_order = list(pickup_info[selected_trek][selected_city].keys())
                    else:
                        pickup_order = list(pickup_info[selected_trek].keys())

                    participants = {}
                    for _, row in df.iterrows():
                        pickup_raw = str(row[pickup_col])
                        matched_stop = next((stop for stop in pickup_order if stop.lower() in pickup_raw.lower()), "Other")
                        entry = f"{row[name_col]} – {row[phone_col]}"
                        participants.setdefault(matched_stop, []).append(entry)

                    st.session_state.participant_data = {
                        "trek": selected_trek,
                        "participants": participants,
                        "city": selected_city
                    }
                    st.session_state.page = "summary"
                    st.rerun()

# --- Summary Page ---
if st.session_state.page == "summary":
    trek = st.session_state.participant_data["trek"]
    participants = st.session_state.participant_data["participants"]
    city = st.session_state.participant_data["city"]

    # Choose correct pickup map
    if trek == "Steps of Paradise":
        location_links = pickup_info[trek][city]
    else:
        location_links = pickup_info[trek]

    total_participants = sum(len(v) for v in participants.values())
    st.markdown(f"<h3 style='font-size:28px;'>Total Participants: {total_participants}</h3>", unsafe_allow_html=True)

    # Sort locations according to order in pickup_info
    if trek == "Steps of Paradise":
        pickup_order = list(pickup_info[trek][city].keys())
    else:
        pickup_order = list(pickup_info[trek].keys())

    full_text = f"Total Participants: {total_participants}\n\n"

    for location in pickup_order:
        if location in participants:
            people = participants[location]
            loc_url = location_links.get(location, "")
            if loc_url:
                st.markdown(f"- [{location}]({loc_url}) ({len(people)})")
                full_text += f"{location} ({len(people)}):\n"
            else:
                st.markdown(f"- {location} ({len(people)})")
                full_text += f"{location} ({len(people)}):\n"
            for person in people:
                st.checkbox(person, value=False, key=f"{location}_{person}")
                full_text += f"  - {person}\n"
            full_text += "\n"
