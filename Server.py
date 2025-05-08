import os
from flask import Flask, request, redirect, url_for, render_template
from moviepy import VideoFileClip, AudioFileClip
import pytubefix
from pytubefix import YouTube
import re

Server = Flask(__name__)

def clean_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)

def create_flac_output_folder(): 
    user_home = os.path.expanduser('~') 
    output_path = os.path.join(user_home, 'Converted Flac Files') 
    if not os.path.exists(output_path): 
        os.makedirs(output_path) 
    print(output_path)
    return output_path

def create_yt_output_folder():
    user_home = os.path.expanduser('~')
    output_path = os.path.join(user_home, 'Downloaded Youtube Videos')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


#youtube_url = "https://www.youtube.com/watch?v=7TpscN7uMBQ"
UPLOAD_FOLDER = create_yt_output_folder()
Server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url, use_po_token=True)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if stream:
            stream.download(output_path)
        else:
            raise Exception("No MP4 stream available")
    except pytubefix.exceptions.VideoUnavailable:
        raise Exception("Video unavailable")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def convert_video_to_flac(video_path, flac_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(flac_path, codec='flac')
    except KeyError:
        audio = AudioFileClip(video_path)
        audio.write_audiofile(flac_path, codec='flac')
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

@Server.route('/')
def home():
    return render_template('index.html')

@Server.route('/convert', methods=['POST'])
def convert():
    mp4_path = None

    # Handle YouTube URL
    youtube_url = request.form.get('youtube_url')
   # print(youtube_url)
    if youtube_url:
        yt = YouTube(youtube_url,use_po_token=True)
        video_title =yt.title
        video_title = clean_filename(video_title)
        mp4_path = os.path.join(UPLOAD_FOLDER, f'{video_title}.mp4')
        try:
            download_youtube_video(youtube_url, UPLOAD_FOLDER)
            message = f"Conversion Complete! Youtube Video saved at {mp4_path}"
            return redirect(url_for('result', message=message))
        except Exception as e:
            return f"Failed to download video: {str(e)}"

    # Handle MP4 file upload
    if 'mp4_file' in request.files and request.files['mp4_file'].filename != '':
        file = request.files['mp4_file']
        mp4_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(mp4_path)

    if not mp4_path:
        return "No video provided"

    output_folder = create_flac_output_folder()
    title = extract_title_from_path(mp4_path)
    flac_path = os.path.join(output_folder, f"{title}.flac")

    try:
        convert_video_to_flac(mp4_path, flac_path)
        message = f"Conversion Complete! FLAC file saved at {flac_path}"
    except Exception as e:
        message = f"Conversion failed: {str(e)}"

    return redirect(url_for('result', message=message))

def extract_title_from_path(path):
    base_name = os.path.basename(path)
    title, _ = os.path.splitext(base_name)
    return title

@Server.route('/result')
def result():
    message = request.args.get('message', '')
    return render_template('Result.html', message=message)

if __name__ == '__main__':
    #download_youtube_video(youtube_url, UPLOAD_FOLDER)
    Server.run(debug=True)
    # port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000 locally
    # Server.run(debug=True, host='0.0.0.0', port=port)  # Bind to 0.0.0.0 for external access

