import yt_dlp
import os
import traceback

class Download:
    def __init__(self, url, format, resolution, Playlist=False, dir="Downloads"):
        self.url = url
        self.format = format
        self.resolution = resolution
        self.Playlist = Playlist
        self.dir = dir
        if not os.path.exists(dir):
            os.makedirs(dir)

    def download_video(self):
        try:
            ydl_opts = {
                'format': f'bestvideo[height<={self.resolution}]+bestaudio/best[height<={self.resolution}]',
                'outtmpl': os.path.join(self.dir, '%(title)s.%(ext)s'),
                'noplaylist': not self.Playlist,
                'merge_output_format': 'mp4'  # assure une sortie .mp4
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            print(f"Erreur lors du téléchargement vidéo : {e}")
            traceback.print_exc()

    def download_audio(self):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.dir, '%(title)s.%(ext)s'),
                'noplaylist': not self.Playlist,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            print(f"Erreur lors du téléchargement audio : {e}")
            traceback.print_exc()

    def download_audio_and_video(self):
        """
        Télécharge la vidéo en MP4 + un MP3 séparé
        """
        self.download_video()
        self.download_audio()

    def download(self):
        print(f"Requête de téléchargement : {self.url}")
        try:
            if self.format == "video":
                self.download_video()
            elif self.format == "audio":
                self.download_audio()
            elif self.format == "video+audio":
                self.download_audio_and_video()
            else:
                print("Format non reconnu (utilise 'video', 'audio' ou 'video+audio').")
        except Exception as e:
            print(f"Erreur lors du téléchargement : {e}")
            traceback.print_exc()
        print("Téléchargement terminé.")