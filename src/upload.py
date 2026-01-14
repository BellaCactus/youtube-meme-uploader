import os
import random
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# --- YouTube API Setup ---
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secrets.json" # Your credentials file

# --- Meme Vocabulary List ---
meme_vocabulary = [
    "skibidi", "gyatt", "rizz", "only in ohio", "duke dennis", "did you pray today", "livvy dunne",
    "rizzing up", "baby gronk", "sussy imposter", "pibby glitch", "in real life", "sigma male",
    "alpha male", "omega male", "grindset", "andrew tate", "goon cave", "freddy fazbear", "colleen ballinger",
    "smurf cat", "strawberry elephant", "blud", "dawg", "shmlawg", "ishowspeed", "a whole bunch of turbulence",
    "ambatukam", "bro really thinks he's carti", "literally hitting the griddy", "the ocky way",
    "kai cenat", "fanum tax", "garten of banban", "no edging in class", "not the mosquito again", "bussing",
    "axel in harlem", "whopper whopper", "1 2 buckle my shoe", "goofy ahh", "aiden ross", "sin city",
    "monday left me broken", "quirked up white boy", "busting it down sexual style", "goated with the sauce",
    "john pork", "grimace shake", "kiki do you love me", "huggy wuggy", "nathaniel b", "lightskin stare",
    "biggest bird", "omar the referee", "amogus", "uncanny", "wholesome", "reddit chungus", "keanu reeves",
    "pizza tower", "zesty", "poggers", "kumalala savesta", "quandale dingle", "glizzy", "rose toy",
    "ankha zone", "thug shaker", "morbin time", "dj khaled", "sisyphus", "oceangate", "shadow wizard money gang",
    "ayo the pizza here", "PLUH", "nair butthole waxing", "t-pose", "ugandan knuckles",
    "family guy funny moments compilation", "subway surfers gameplay", "nickeh30", "ratio", "uwu", "delulu",
    "opium bird", "cg5", "mewing", "fortnite battle pass", "all my fellas", "gta 6", "backrooms",
    "gigachad", "based", "cringe", "kino", "redpilled", "no nut november", "pokénut november", "foot fetish",
    "F in the chat", "i love lean", "looksmaxxing", "gassy", "social credit", "bing chilling", "xbox live",
    "mrbeast", "kid named finger", "better caul saul", "i am a surgeon", "hit or miss", "i like ya cut g",
    "ice spice", "gooning", "fr", "we go gym", "kevin james", "josh hutcherson", "coffin of andy and leyley",
    "metal pipe falling", "brainrot"
]

# --- Function Definitions ---
def get_authenticated_service():
    """Logs the user in and returns an authorized YouTube API service object."""
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, file, title, description, category, tags):
    """Uploads a video to YouTube."""
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category
        },
        'status': {
            'privacyStatus': 'private'
        }
    }
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if 'id' in response:
            print(f"✅ Video '{title}' was successfully uploaded with ID: {response['id']}")
        elif status:
            print(f"Uploaded {int(status.progress() * 100)}%.")

# --- Main Execution Block ---
# This is the code that runs when you start the script.
if __name__ == '__main__':
    print("--- SCRIPT HAS STARTED, TRYING TO LOGIN NOW ---")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube_service = get_authenticated_service()

    # Configuration
    video_file_path = "my_test_video.mp4"
    upload_count = 100

    # Loop, Generate, and Upload
    for i in range(upload_count):
        print("-" * 50)
        print(f"▶️ Starting upload {i + 1} of {upload_count}...")

        title_parts = random.sample(meme_vocabulary, k=random.randint(3, 5))
        video_title = ' '.join(title_parts).title()

        desc_parts = random.sample(meme_vocabulary, k=random.randint(8, 15))
        video_description = ' '.join(desc_parts) + "."

        video_tags = random.sample(meme_vocabulary, k=5)
        video_category_id = "24" # Entertainment

        print(f"   Title: {video_title}")
        print(f"   Description: {video_description}")

        try:
            upload_video(youtube_service, video_file_path, video_title, video_description, video_category_id, video_tags)
        except googleapiclient.errors.HttpError as e:
            print(f"❌ An HTTP error {e.resp.status} occurred:\n{e.content}")
            if 'quotaExceeded' in str(e.content):
                print("🛑 Daily quota exceeded. Stopping the script.")
                break