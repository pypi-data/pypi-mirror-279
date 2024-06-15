import os
import sys
import time
import logging
import argparse
from PIL import Image
from threading import Thread


logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG, format="%(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)


def reduce_image_size(imgpath: str):
    """
    Given an image filepath it will try to reduce it's size to 500kb.
    Returns image filepath
    """

    image = Image.open(imgpath)
    target_size = 500 * 1024  # 500 KB

    initial_image_size = os.path.getsize(imgpath)
    if initial_image_size <= target_size:
        return imgpath

    quality_range = range(90, 10, -10)
    for quality in quality_range:
        image.save(imgpath, optimize=True, quality=quality)

        current_image_size = os.path.getsize(imgpath)

        if current_image_size <= target_size:
            break

        if current_image_size == initial_image_size:
            break

        initial_image_size = current_image_size

    return imgpath


def optimize_image(filepath: str):
    try:
        original_size = os.path.getsize(filepath)
        reduce_image_size(filepath)
        reduced_size = os.path.getsize(filepath)
        reduction_percentage = (
            (original_size - reduced_size) / original_size
        ) * 100
        if reduction_percentage < 0:
            reduction_percentage = 0
        log.info(
            f"File {filepath} reduced from {original_size} to {reduced_size} which is a {reduction_percentage:.2f}% reduction"
        )
    except Exception as err:
        log.error(f"Can't optimize {filepath} because:\n{err}")


def process_images(directory: str):
    """
    Traverse given `directory` path and try to shrink/optimize all images found.
    Returns a list of images.
    """
    extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")

    threads = []
    optimized_images_filepaths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("HQ_"):
                continue
            if file.lower().endswith(extensions):
                filepath = os.path.join(root, file)
                thread = Thread(name=filepath, target=optimize_image, args=(filepath,))
                threads.append(thread)
                thread.start()
                optimized_images_filepaths.append(filepath)

    for thread in threads:
        thread.join()

    return optimized_images_filepaths


def cli():
    parser = argparse.ArgumentParser(
        description="Aggresively optimize images to be under 500kb"
    )
    parser.add_argument(
        "--path",
        type=str,
        default="./",
        help="Path to the directory to optimize images.",
    )
    args = parser.parse_args()
    start = time.perf_counter()
    process_images(args.path)
    end = time.perf_counter()
    log.info(f"Done in {(end - start):.2f} seconds!")



if __name__ == "__main__":
    cli()
