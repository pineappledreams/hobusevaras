import requests
import re
import os
import random
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

BASE_LINK = "https://hobune.stream"


def get_input():
    url = input("Which hobune url you wanna download?\n")
    print(f"OK bro you have selected: {url}")
    return url


def download_video(wanted_link, wanted_folder=None):
    vid_response = requests.get(wanted_link)
    vid_soup = BeautifulSoup(vid_response.text, "html.parser")
    a = vid_soup.find("a", {"href": re.compile("mp4$")})
    video_link = f'{a["href"]}' if a["href"].startswith("http") else f'{BASE_LINK}{a["href"]}'

    download = requests.get(video_link, stream=True)
    total_size_in_bytes = int(download.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    file_name = video_link.split("/")[-1].replace("%20", " ")
    folder_name = f"{wanted_folder}/" if wanted_folder else ""
    destination = f"{folder_name}{file_name}"

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, folder_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    print(f"Downloading to {destination}")

    with open(destination, "wb") as file:
        for data in download.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")


def iterate_over_channel(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    user_name = soup.find("h1").text
    links = soup.find_all("a", attrs={"class": "ui fluid card"})

    print(f"Channel name: {user_name}")
    print(f"Found {len(links)} links inside the thing!")

    for idx, link in enumerate(links):
        print(f"Index: {idx+1}/{len(links)}")
        header = link.find("h3").text
        href = link["href"]
        wanted_link = f"{BASE_LINK}{href}"

        print(f"Found {header} with link {wanted_link}")
        print(f"Getting {wanted_link}")

        download_video(wanted_link, user_name)

        sleepy_time = random.randint(1, 5)
        print(f"sleeping for: {sleepy_time} seconds before going to next")
        time.sleep(sleepy_time)


def main():
    url = get_input()
    iterate_over_channel(url)
    print("DONE!!!! ENJOY")


if __name__ == "__main__":
    main()
