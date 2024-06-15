import pathlib

from PIL import Image

from .image_comparator import ImageComparator


# Get list of image file extensions from PIL
IMAGE_EXTENTIONS = {ex.lower() for ex, f in Image.registered_extensions().items() if f in Image.OPEN}
IMAGE_EXTENTIONS |= {'.bmp', '.png', '.jpg', '.ps', '.eps', '.cps', '.tif', '.tiff'}


def is_image(file_path):
    return file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENTIONS


def list_files(left_topdir, right_topdir, subdir=pathlib.Path('.')):
    if left_topdir.is_dir():
        leftdir = left_topdir / subdir
        if right_topdir.is_dir():
            rightdir = right_topdir / subdir

            dirs = set()
            files = set()

            if leftdir.is_dir():
                leftdir_paths = list(leftdir.glob('[!.]*'))
                dirs |= set(
                    map(
                        lambda p: p.relative_to(left_topdir),
                        filter(pathlib.Path.is_dir, leftdir_paths),
                    )
                )
                files |= set(map(lambda p: p.name, filter(pathlib.Path.is_file, leftdir_paths)))

            if rightdir.is_dir():
                rightdir_paths = list(rightdir.glob('[!.]*'))
                dirs |= set(
                    map(
                        lambda p: p.relative_to(right_topdir),
                        filter(pathlib.Path.is_dir, rightdir_paths),
                    )
                )
                files |= set(map(lambda p: p.name, filter(pathlib.Path.is_file, rightdir_paths)))

            for file in sorted(files):
                yield str(subdir / file), leftdir / file, rightdir / file

            for d in sorted(dirs):
                for item in list_files(left_topdir, right_topdir, d):
                    yield item


def list_image_files(left_topdir, right_topdir, subdir=pathlib.Path('.')):
    for subpath, left, right in list_files(left_topdir, right_topdir, subdir):
        if is_image(left) or is_image(right):
            yield subpath, ImageComparator(left, right)
