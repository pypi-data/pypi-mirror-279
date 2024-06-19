from lioness.nodes.download_and_merge import _download_and_merge

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    from lioness.nodes.project_logging import default_logging

    default_logging()

    parser = argparse.ArgumentParser(
        description="Downloads the highest quality audio-less video and "
        "audio streams before merging them into a single file"
    )
    parser.add_argument(
        "-vu",
        "--video_url",
        type=str,
        required=True,
        help="Youtube video URL for download",
    )
    parser.add_argument(
        "-pdv",
        "--path_dir_video",
        type=Path,
        required=True,
        help="Path of a directory to which the audio-less video file is saved",
    )
    parser.add_argument(
        "-pda",
        "--path_dir_audio",
        type=Path,
        required=True,
        help="Path to a directory to which the audio file is saved",
    )
    parser.add_argument(
        "-pdc",
        "--path_dir_combined",
        type=Path,
        required=True,
        help="Path of a directory to which the combined file is saved",
    )

    args = parser.parse_args()

    _download_and_merge(
        video_url=args.video_url,
        path_dir_video=args.path_dir_video,
        path_dir_audio=args.path_dir_audio,
        path_dir_combined=args.path_dir_combined,
    )
