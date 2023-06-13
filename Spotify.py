import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Replace with newly obtained access token
access_token = "BQBDsNJpTpsmQ_LhiJI64tlgzDRWHXCNSOKUC26tID8O3uXjvhPyAPailifanG_mxiSSJSREoPDrraeLnAA-aGfpPYcn62P3O2vMHaS0-ZMp3f4DobAu"
headers = {
    'Authorization': f'Bearer {access_token}'
}

# My Spotify User ID
user_id = '1215280657'

# Get "Liked Songs" playlist ID
url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
params = {'limit': 50}
liked_songs_playlist_id = None
while url:
    response = requests.get(url, headers=headers, params=params)
    playlists_data = response.json()
    for playlist in playlists_data['items']:
        if playlist['name'] == 'Liked Songs':
            liked_songs_playlist_id = playlist['id']
            break
    if liked_songs_playlist_id:
        break
    url = playlists_data['next']

if not liked_songs_playlist_id:
    raise Exception("Liked Songs playlist not found")

# Get tracks from the "Liked Songs" playlist
url = f'https://api.spotify.com/v1/playlists/{liked_songs_playlist_id}/tracks'
params = {'limit': 100}
tracks = []
while url:
    response = requests.get(url, headers=headers, params=params)
    playlist_tracks_data = response.json()
    for item in playlist_tracks_data['items']:
        track = item['track']
        artist = track['artists'][0]
        tracks.append({
            'name': track['name'],
            'artist_id': artist['id'],
            'artist_name': artist['name'],
            'album_name': track['album']['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'explicit': track['explicit'],
            'track_id': track['id']
        })
    url = playlist_tracks_data['next']

# Get artist names
def get_artist_names(artist_ids, headers):
    url = 'https://api.spotify.com/v1/artists'
    artist_id_to_name = {}
    for i in range(0, len(artist_ids), 50):
        ids_batch = artist_ids[i:i+50]
        params = {
            'ids': ','.join(ids_batch)
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            raise Exception('API request failed')
        artists_data = response.json()['artists']
        for artist in artists_data:
            artist_id_to_name[artist['id']] = artist['name']
    return artist_id_to_name

artist_ids = [track['artist_id'] for track in tracks]
artist_id_to_name = get_artist_names(artist_ids, headers)

# Add artist names to the tracks
for track in tracks:
    track['artist_name'] = artist_id_to_name[track['artist_id']]

# Get the audio features
track_ids = [track['track_id'] for track in tracks]
url = 'https://api.spotify.com/v1/audio-features'
params = {
    'ids': ','.join(track_ids)
}
response = requests.get(url, headers=headers, params=params)

# Create a DataFrame of audio features for each song
audio_features = []
for track in tracks:
    response = requests.get(f'https://api.spotify.com/v1/audio-features/{track["track_id"]}', headers=headers)
    audio_features_data = response.json()
    audio_features.append({
        'name': track['name'],
        'artist_name': track['artist_name'],
        'danceability': audio_features_data['danceability'],
        'energy': audio_features_data['energy'],
        'key': audio_features_data['key'],
        'loudness': audio_features_data['loudness'],
        'mode': audio_features_data['mode'],
        'speechiness': audio_features_data['speechiness'],
        'acousticness': audio_features_data['acousticness'],
        'instrumentalness': audio_features_data['instrumentalness'],
        'liveness': audio_features_data['liveness'],
        'valence': audio_features_data['valence'],
        'tempo': audio_features_data['tempo'],
        'duration_ms': audio_features_data['duration_ms'],
        'duration_minutes': audio_features_data['duration_ms'] / 60000
    })

# Pandas dataframe
df = pd.DataFrame(audio_features)

# Print dataframe
print(df.head())

# Create a DataFrame of artist danceability
artist_danceability = pd.DataFrame(audio_features).groupby('artist_name')['danceability'].mean().reset_index()

# Sort the DataFrame by danceability in descending order
artist_danceability_sorted = artist_danceability.sort_values(by='danceability', ascending=False)

# Create a horizontal bar plot of danceability by artist
plt.figure(figsize=(12, 6))
sns.barplot(x='danceability', y='artist_name', data=artist_danceability_sorted, palette='RdBu')
plt.xlabel('Danceability')
plt.ylabel('Artist Name')
plt.title('Danceability by Artist')
plt.show()

'''This displays that the Top Artist for Danceability is Marshmellow and the least Danceable is Glass Animals'''

# Create a DataFrame of song acousticness
song_acousticness = pd.DataFrame(audio_features)

# Sort the DataFrame by acousticness in descending order with the top 10 songs
top_songs_acousticness = song_acousticness.sort_values(by='acousticness', ascending=False).head(10)

# Add a new column with the song name and artist name combined so that we can also see acousticness
top_songs_acousticness['name_artist'] = top_songs_acousticness['name'] + ' (' + top_songs_acousticness['artist_name'] + ')'

# Create a horizontal bar plot of the top 10 songs with the highest acousticness
plt.figure(figsize=(12, 6))
sns.barplot(x='acousticness', y='name_artist', data=top_songs_acousticness, palette='RdBu')
plt.xlabel('Acousticness')
plt.ylabel('Song Name (Artist Name)')
plt.title('Top 10 Songs with the Highest Acousticness')
plt.show()

'''For this I only picked the top 10 so that it would be easier to diplay in a chart. 
I already expected Glass Animals to have a high Acoustic value especially considering it showed up as the least danceable.
However, I was expecting Red Hot Chili Peppers to be a little higher on the chart. 
I was also expecting Marshbellow to be a little lower on the chart considering he had the highest danceability.'''

# Add genre to function
def get_artist_names_and_genres(artist_ids, headers):
    url = 'https://api.spotify.com/v1/artists'
    artist_id_to_info = {}
    for i in range(0, len(artist_ids), 50):
        ids_batch = artist_ids[i:i+50]
        params = {
            'ids': ','.join(ids_batch)
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            raise Exception('API request failed')
        artists_data = response.json()['artists']
        for artist in artists_data:
            artist_id_to_info[artist['id']] = {
                'name': artist['name'],
                'genres': artist['genres']
            }
    return artist_id_to_info

# Get artist names and genres
artist_id_to_info = get_artist_names_and_genres(artist_ids, headers)

# Add artist names and genres to the tracks
for track in tracks:
    track['artist_name'] = artist_id_to_info[track['artist_id']]['name']
    track['artist_genres'] = artist_id_to_info[track['artist_id']]['genres']

# Count genre occurrences
genre_counts = {}
for track in tracks:
    for genre in track['artist_genres']:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

# Create a DataFrame of genre occurrences
genre_counts_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])

# Sort the DataFrame by count in descending order
genre_counts_df = genre_counts_df.sort_values(by='Count', ascending=False)

# Create a horizontal bar plot of the genre distribution
plt.figure(figsize=(12, 6))
sns.barplot(x='Count', y='Genre', data=genre_counts_df, palette='viridis')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.title('Genre Distribution')
plt.show()

'''For this I discovered a lot of genres that I didn't know existed such as 'Permanent Wave,' 'Tropical House,' and 'Fremantle Indie.' '''

# Create scatter plot of valence vs. energy
plt.figure(figsize=(12, 6))
plt.scatter(df['valence'], df['tempo'])
plt.xlabel('Valence')
plt.ylabel('Tempo (BPM)')
plt.title('Valence vs. Tempo')
plt.show()

'''This was surprising because I would have thought that faster songs would have had a higher level of valance(musical positivity or mood)'''

# Create box plot to show length of songs
plt.boxplot(df["duration_minutes"])
plt.xlabel("Songs")
plt.ylabel("Duration (minutes)")
plt.title("Distribution of Song Length")
plt.show()

'''Results were originally in miliseconds, so I had to add to divide by 60000 (1,000 milliseconds in a second and 60 seconds in a minute) 
and add ''duration_minutes': audio_features_data['duration_ms'] / 60000' to the audio features dataframe.
You can see that songs start at a little under 3 minutes, most fall within 3.5 minutes, with some songs slightly over 4 minutes.'''