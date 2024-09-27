import requests
import streamlit as st
import random
import time

from generator import generate_data

st.title("Health Pal")

OPEN_API_SECRET = "4c952124-e406-4715-9e01-40c2035dc5b0"
APP_SECRET ="SLKNAAS&*AS(A(SA&S^AS$AS%A*&AS&"

default_prompt = """
Make this chat a health based chat only. 

Schemas:
Symptom(date: DateTime, name: String, type: "Symptom", description: String)
Activity(date: DateTime, name: String, type: "Activity", description: String)
Medication(date: DateTime, name: String, type: "Medication", description: String)

Rules:
1. Try to collect the data of symptoms, daily activities, and medication as a json object 
as per the above schema get all the details.
2. Don’t let the chat know about the json you are making. 
3. Keep it like a chat between a friends and try to collect as much data as possible.
4. Try to be concise.
"""

default_response = """
I'm here to help with your health-related questions and discussions. 
Feel free to share your symptoms or daily activities, and we can chat about them!
"""


# Generate sample data for each schema type
if 'Symptom' not in st.session_state:
    st.session_state['Symptom'] = []
    st.session_state['Symptom'] += generate_data("Symptom", num_samples=10)
if 'Activity' not in st.session_state:
    st.session_state['Activity'] = []
    st.session_state['Activity'] += generate_data("Activity", num_samples=10)
if 'Medication' not in st.session_state:
    st.session_state['Medication'] = []
    st.session_state['Medication'] += generate_data("Medication", num_samples=10)

def reset():
    st.session_state.messages = [
        {"role": "assistant", "content": default_response}
    ]


def getJson():
    print("saving")
    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    messages.insert(0, {"role": "user", "content": default_prompt}, )
    messages.append({"role": "user", "content": """
    give json as per the schema from the conversation so far.
     give only json with now text so it can be json loaded.
     It should have following format:
     {
        "Medication": [{'date': '2022-10-01T09:00:00', 'name': 'Paracetamol', 'type': 'Medication', 'description': 'Took paracetamol'}],
        "Symptom": [ {'date': '2022-10-01T09:00:00', 'name': 'Body Aches', 'type': 'Symptom', 'description': 'Experiencing body aches'}],
        "Activity": [...]
     }
     """}, )
    headers = {
        "Content-Type": "application/json"
    }
    data = {"messages": messages}
    assistant_response = requests.post("https://uop-app-name-1.azurewebsites.net/api/openapihttp", json=data,
                                       headers=headers)
    resp = assistant_response.json()
    print(resp)
    for key in resp.keys():
        st.session_state[key] += resp[key]
    reset()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": default_response}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.sidebar.title("Actions Menu")
save_btn = st.sidebar.button("save", on_click=getJson)
reset_btn = st.sidebar.button("reset", on_click=reset)

# Accept user input
if prompt := st.chat_input("Enter your response here"):
    # Add user message to chat history
    if prompt == "kuljasimsim":
        getJson()
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # assistant_response = random.choice(
            #     [
            #         "Hello there! How can I assist you today?",
            #         "Hi, human! Is there anything I can help you with?",
            #         "Do you need help?",
            #     ]
            # )
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            messages.insert(0, {"role": "user", "content": default_prompt}, )
            headers = {
                "Content-Type": "application/json"
            }
            data = {"messages": messages}
            assistant_response = requests.post("https://uop-app-name-1.azurewebsites.net/api/openapihttp", json=data,
                                               headers=headers)
            # Simulate stream of response with milliseconds delay
            resp = assistant_response.text
            for chunk in resp.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
