import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
import requests
import os
import qrcode
import pyshorteners
# short_url = pyshorteners.Shortener().tinyurl.short

def shorten_url(url_received):
    res = requests.post('https://api.short.io/links', json={
        'domain': 'link.sut.com.vn',
        'originalURL': url_received,
    }, headers = {
        'authorization': 'sk_0YQAtikBf4puA3Vf',
        'content-type': 'application/json'
    }, )

    res.raise_for_status()
    data = res.json()

    print(data['shortURL'])
    return data['shortURL']
def authorize_credentials():
    CLIENT_SECRET = './credentials.json'
    SCOPE = 'https://www.googleapis.com/auth/photoslibrary'
    STORAGE = Storage('credentials.storage')

    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

def get_access_token():
    credentials = authorize_credentials()
    if credentials.access_token_expired:
        credentials.refresh(httplib2.Http())
    return credentials.access_token

def getPhotoUrl(access_token, photo_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    url = f"https://photoslibrary.googleapis.com/v1/mediaItems/{photo_id}"
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    print(response_json)
    photo_url = response_json["baseUrl"]
    return photo_url

def uploadPhoto(image_path):
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Content-Type': 'image/jpeg',
        'X-Goog-Upload-Protocol': 'raw'
    }
    with open(image_path, 'rb') as f:
        image_data = f.read()

    response = requests.post('https://photoslibrary.googleapis.com/v1/uploads',
                             headers=headers,
                             data=image_data)
    response.raise_for_status()
    
    upload_token = response.text
    headers = {
        'Authorization': f'Bearer {access_token}',
        "Content-type": "application/json"
    }
    payload = {
        "newMediaItems": [
            {
                "simpleMediaItem": {
                    "fileName": os.path.basename(image_path),
                    "uploadToken": upload_token
                }
            }
        ]
    }
    response = requests.post("https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate", 
                             headers=headers, 
                             json=payload)
    response.raise_for_status()
    json_response = response.json()
    photo_id = json_response['newMediaItemResults'][0]['mediaItem']['id']
    photo_url = getPhotoUrl(access_token, photo_id)
    photo_url = shorten_url(photo_url)
    print(photo_url)
    return photo_url

# def upload_photo_ggdrive(image_path): 


def link_to_qrcode(link, output_file):
    """
    Converts a link to a QR code and saves it to an image file.
    
    Parameters:
    link (str): The URL to be converted into a QR code.
    output_file (str): The file path where the QR code image will be saved.
    """
    # link = uploadPhoto(link)
    # Create a QR code object with the given link
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Controls the error correction used for the QR Code
        box_size=10,  # Controls how many pixels each “box” of the QR code is
        border=4,  # Controls how many boxes thick the border should be
    )
    
    # Add the link data to the QR code
    qr.add_data(link)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image to the specified file
    img.save(output_file)
    print(f"QR code saved to {output_file}")

    return output_file