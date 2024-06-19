import logging
import subprocess
from pathlib import Path

from pytube import YouTube

logging.getLogger("pytube").setLevel(level=logging.INFO)
logger = logging.getLogger(__name__)


def _download_and_merge(
    video_url: str, path_dir_video: Path, path_dir_audio: Path, path_dir_combined: Path
) -> None:
    video = YouTube(video_url)

    # Select the highest resolution video stream with progressive=False
    video_stream = (
        video.streams.filter(progressive=False, file_extension="mp4", type="video")
        .order_by("resolution")
        .desc()
        .first()
    )
    logger.info(
        "The following video stream is automatically selected "
        f"as the highest quality stream:\n{video_stream}"
    )

    # Select the highest quality audio stream
    audio_stream = (
        video.streams.filter(progressive=False, file_extension="mp4", type="audio")
        .order_by("abr")
        .desc()
        .first()
    )
    logger.info(
        "The following audio stream is automatically selected "
        f"as the highest quality stream:\n{audio_stream}"
    )

    # Download video and audio streams
    video_filename = video_stream.default_filename
    audio_filename = video_stream.default_filename.replace(".mp4", ".mp3")

    video_file = path_dir_video / video_filename
    audio_file = path_dir_audio / audio_filename

    video_stream.download(output_path=path_dir_video, filename=video_filename)
    audio_stream.download(output_path=path_dir_audio, filename=audio_filename)

    logger.info(f"Downloaded video: {video_file}")
    logger.info(f"Downloaded audio: {audio_file}")

    # Define the output file path
    output_file = path_dir_combined / video_filename

    # Create parent directories if not exist already
    logger.info(f'The following directory would be created if not already exist:\n{output_file.parent}')
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Merge video and audio using ffmpeg
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        str(video_file),
        "-i",
        str(audio_file),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-strict",
        "experimental",
        str(output_file),
    ]
    subprocess.run(ffmpeg_command)

    logger.info(f"Final video saved to: {output_file}")
