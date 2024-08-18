import streamlit as st
import requests

# Replace with your Strava app's client ID and secret
CLIENT_ID = '132513'
CLIENT_SECRET = '98b0aa1146fde236a9c30822f23fe4b63acf0531'
REDIRECT_URI = 'http://localhost:8501/'  # Update this to your deployed URL
AUTHORIZATION_URL = 'https://www.strava.com/oauth/authorize'
TOKEN_URL = 'https://www.strava.com/oauth/token'
ACTIVITIES_URL = 'https://www.strava.com/api/v3/athlete/activities'

def get_authorization_url():
    return f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=read_all"

def get_access_token(code):
    response = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    })
    return response.json().get('access_token')

def fetch_activities(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(ACTIVITIES_URL, headers=headers)
    return response.json()

st.title('Strava Workout Data Viewer')

if 'access_token' not in st.session_state:
    st.write("Please authenticate with Strava to access your data.")
    st.markdown(f"[Authenticate with Strava]({get_authorization_url()})")
else:
    st.write("You are authenticated. Fetching your workout data...")
    activities = fetch_activities(st.session_state.access_token)
    st.write(activities)

# Handle OAuth2 callback
params = st.experimental_get_query_params()
if 'code' in params:
    code = params['code'][0]
    access_token = get_access_token(code)
    st.session_state.access_token = access_token
    st.write("Authentication successful. You can now view your workout data.")