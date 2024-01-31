### Itiner-AI Web App ###

### import libraries
import pandas as pd
import streamlit as st
from openai import OpenAI
from streamlit_extras.app_logo import add_logo
from stqdm import stqdm
from time import sleep
from pathlib import Path


st.set_page_config(page_title="Itiner-AI Travel App")
ss = st.session_state
if 'debug' not in ss: ss['debug']={}

image_path = Path(__file__).parents[1] / 'streamlit/gallery/logo_edit.png'

add_logo(image_path, height=300)

###### DEFINE FUNCTIONS #######

# API Key Definition
def ai_api():
    if 'OPENAI_API_TOKEN' in st.secrets:
        st.success('OpenAPI key has been provided!', icon='✅')
        api_key = st.secrets['OPENAI_API_TOKEN']
    else:
        api_key = st.text_input('Enter OpenAI API token:', type = 'password')
        if not api_key.startswith('sk_'):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Now you can plan your trip!', icon='🌎')
    return api_key    



# Define Sidebar

with st.sidebar:
    st.image(image_path)
    api_key = ai_api()
    st.markdown('Input the details of your trip below:')

    with st.form(key='form'):
        destination = st.text_input('Trip Destination:', 'San Francisco')
        duration = st.text_input('Duration of trip:', '3 days')
        likes = st.text_input('Enter a list of likes:', 'sports, history and multi-cultural cuisine')
        dislikes = st.text_input('Enter a list of dislikes:', 'too much walking')
        specific = st.text_input('Is there anything specific you would like to include?:', 'Alcatraz')
        submit = st.form_submit_button()


# define tabs
t1,t2 = st.tabs(['Detailed Itinerary', 'Concise Itinerary'])

# define placeholders for text output

with t1:
    placeholder1 = st.empty()
    placeholder1.markdown('## Welcome to Itiner-AI! \n Fill in the information on the left to generate a personalized itinerary for your next trip with the help of Generative AI. Use the tabs above to find the right layout for you, as well as updating the output for your perfect holiday.')
with t2:
    placeholder2 = st.empty()
    placeholder2.markdown('## Welcome to Itiner-AI! \n Fill in the information on the left to generate a personalized itinerary for your next trip with the help of Generative AI. Use the tabs above to find the right layout for you, as well as updating the output for your perfect holiday.')

# cache data from function
#@st.cache_data
def itiner_ai(duration = duration, destination = destination, likes = likes, dislikes = dislikes, specific = specific, t1 = t1, t2 = t2):
    """ Function to generate a bespoke travel itinerary based on users likes/dislikes.
    
    input Variables:
        duration 
        destination 
        likes 
        dislikes
        specific 

    """

    # activate client
    client = OpenAI(api_key=api_key)

    # populate prompt with 
    prompt = "Craft an immersive and varied itinerary for a " + duration + " trip to " + destination + " that seamlessly blends " + likes + ", and ensures " + specific + ". Tailor the itinerary to accommodate these preferences while avoiding " + dislikes + ", ensuring a captivating exploration of " + destination + "'s cultural facets. Provide specific recommendations for activities, attractions, dining experiences, estimated durations, approximate costs, transportation options between locations, and unique highlights at each stop. Aim for a well-rounded itinerary that caters to diverse interests, guaranteeing an unforgettable journey through the vibrant landscape of " + destination + "."
    
    messages = [{"role": "system", "content": "You are a helpful travel agent."}]
    user_msgs = [prompt, "Summarize this to include only the timings and headlines for each activity as a bullet point schedule."]

    for q in user_msgs:

        # Create a dictionary for the user message from q and append to messages
        user_dict = {"role": "user", "content": q}
        messages.append(user_dict)

        # Create the API request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages
        )

        # Convert the assistant's message to a dict and append to messages
        assistant_dict = {"role": "assistant", "content": response.choices[0].message.content}
        messages.append(assistant_dict)

    # export itineraries    
    full = messages[2]['content']
    basic = messages[4]['content']

    return messages, full, basic

# submit input variables for itinerary generation    
if submit:

    # run function to generate itineraries    
    messages, full, basic = itiner_ai()

    with t1:
        placeholder1.empty()
        placeholder1.markdown(f'## Detailed Itinerary for {duration} in {destination} \n' + full)
    with t2:
        placeholder2.empty()
        placeholder2.markdown(f'## Concise Itinerary for {duration} in {destination} \n' + basic)


#messages, full, basic = itiner_ai()

#st.write(f'Trip to {destination}')


# define different tabs

#st.sidebar.button('Generate Itinerary', on_click=itiner_ai())

#def itinerary_click():
    #itiner_ai()

    #with t1:
       # st.subheader(f'Detailed Itinerary for {duration} in {destination}')
       # st.markdown(full)
   # with t2:
       # st.subheader(f'Concise Itinerary for {duration} in {destination}')
       # st.markdown(basic)







#for _ in stqdm(st_container=st.sidebar):
 #   sleep(0.5)
