import pafy
from os import path
import os
import shutil
from pytube import Playlist
import unicodedata
import re


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


playlistPath = "C:\\Users\\henwi\\Music\\Playlist\\"
tempPath = "C:\\TempMusic\\"

playlist = Playlist("https://www.youtube.com/playlist?list=PLvt_sqnmkBu77HMTV9h2JI48u5pT8DnJs")

failed = 0

specialNameCases = [["美波「ライラック」MV", '"Lilac" - 美波 (Minami) MV'], ['美波「カワキヲアメク」MV', '"Crying for Rain" - 美波 (Minami) MV'], ['美波「アメヲマツ、」MV', '"Waiting for Rain" - 美波 (Minami) MV'], ['美波「ホロネス」MV', '"Hollowness" - 美波 (Minami) MV']]


def check_to_download(index, pl):
    global failed
    try:
        video = pafy.new(pl[index])
    except:
        print("Failed to get next video object, trying again...")
        try:
            video = pafy.new(pl[index])
        except:
            print("Failed again, skipping...")
            failed = failed + 1
            return

    title = video.title

    for item in specialNameCases:
        if title == item[0]:
            title = item[1]
            break

    print("Video " + str(index+1) + " of " + str(len(playlist)) + ", " + str(round((index+1) / len(playlist) * 100)) + "%")
    print("Original: " + title + "\nSimplified: " + slugify(title))

    if path.exists(tempPath + slugify(title) + ".m4a"):
        print("File is already downloaded, moving it to end directory...")
        os.rename(tempPath + slugify(title) + ".m4a", playlistPath + slugify(title) + ".m4a")
    else:
        print("File is not already downloaded, downloading now...")
        s = video.getbestaudio()
        print("Size is %s" % s.get_filesize())
        try:
            s.download(playlistPath + slugify(title) + ".m4a")
        except:
            print("ERROR: COULD NOT DOWNLOAD")
            failed = failed + 1
    print("\n")


# Creating temp path and moving existing files to it
if not os.path.exists(tempPath):
    os.makedirs(tempPath)

file_names = os.listdir(playlistPath)

for file_name in file_names:
    shutil.move(os.path.join(playlistPath, file_name), tempPath)

# Downloading song files
for i in range(len(playlist)):
    check_to_download(i, playlist)

# Delete temp path and its contents
file_names = os.listdir(tempPath)

for file_name in file_names:
    os.remove(os.path.join(tempPath, file_name))

os.rmdir(tempPath)

print("\n\nFINISHED\nFailed: " + str(failed) + " of " + str(len(playlist)) + "\n" + str(round((len(playlist) - failed) / len(playlist) * 100)) + "% Succeeded")