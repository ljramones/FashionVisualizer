from pathlib import Path


def make_pingpong_loop(input_path: str, output_path: str) -> str:
    """Return the planned output path without invoking ffmpeg.

    A future implementation can use MoviePy or direct ffmpeg calls to reverse and append the
    source clip for smooth ping-pong catalog loops.
    """

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return output_path
