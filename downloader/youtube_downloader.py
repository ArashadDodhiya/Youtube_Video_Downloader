import os
import yt_dlp

class YouTubeDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    def get_video_info(self, url: str):
        """Fetch video information without downloading"""
        ydl_opts = {"quiet": True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        return {
            "title": info.get("title", "Unknown"),
            "duration": f"{info['duration'] // 60}:{info['duration'] % 60:02d}",
            "thumbnail": info.get("thumbnail", ""),
            "uploader": info.get("uploader", "Unknown"),
            "view_count": info.get("view_count", 0)
        }

    def progress_hook(self, d, download_id, progress_dict):
        """Update download progress"""
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "0%").strip()
            speed = d.get("_speed_str", "N/A").strip()
            eta = d.get("_eta_str", "N/A").strip()
            
            progress_dict[download_id] = {
                "status": "downloading",
                "percent": percent,
                "speed": speed,
                "eta": eta
            }
        elif d["status"] == "finished":
            progress_dict[download_id] = {
                "status": "processing",
                "percent": "100%",
                "speed": "N/A",
                "eta": "Processing..."
            }

    def download_video(self, url: str, quality="best", download_id="", progress_dict=None):
        """Download video with specified quality"""
        
        if progress_dict is None:
            progress_dict = {}
        
        if quality == "audio_only":
            format_str = "bestaudio/best"
        elif quality == "best":
            format_str = "best[ext=mp4]/best"
        elif quality in ["720p", "1080p", "480p"]:
            height = quality[:-1]
            format_str = f"best[height<={height}][ext=mp4]/best[height<={height}]"
        else:
            format_str = "best[ext=mp4]/best"

        ydl_opts = {
            "format": format_str,
            "outtmpl": f"{self.download_path}/%(title)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [lambda d: self.progress_hook(d, download_id, progress_dict)],
        }
        
        if quality == "audio_only":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if quality == "audio_only":
                    filename = filename.rsplit(".", 1)[0] + ".mp3"
                
            progress_dict[download_id] = {
                "status": "completed",
                "percent": "100%",
                "filename": os.path.basename(filename),
                "filepath": filename
            }
            return filename
            
        except Exception as e:
            progress_dict[download_id] = {
                "status": "error",
                "error": str(e)
            }
            return None