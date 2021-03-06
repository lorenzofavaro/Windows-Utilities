from getpass import getuser
import os
from shutil import copy
from PIL import Image
from screeninfo import get_monitors
from imagehash import average_hash
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning)

monitor = get_monitors()[0]
screen_size = monitor.width, monitor.height

user = getuser()
src = f"/Users/{user}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets"
dest = f"/Users/{user}/Pictures/Wallpapers"

if not os.path.isdir(dest):
    os.mkdir(dest)


def get_starting_index():
    starting_index = 1

    for file_name in os.listdir(dest):
        index = os.path.splitext(file_name)[0]
        if index.isdigit():
            starting_index = max(int(index) + 1, starting_index)
    return starting_index


def get_wallpapers(index):
    first_index = index
    present_hashes = [str(average_hash(Image.open(os.path.join(dest, dest_file)))) for dest_file in os.listdir(dest)]
    
    for file_name in os.listdir(src):
        src_name = os.path.join(src, file_name)
        dest_name = os.path.join(dest, f"{index}.jpg")
        
        with Image.open(src_name) as im:
            im_hash = str(average_hash(im))

            if im.size == screen_size and im_hash not in present_hashes:
                copy(src_name, dest_name)
                index += 1

    return index - first_index


if __name__ == "__main__":
    starting_index = get_starting_index()
    images_count = get_wallpapers(starting_index)
    
    if images_count > 0:
        print(f"Put {images_count} images in '{dest}'")
    else:
        print("No new images found")
    
    input("\nClick any button to exit...")
