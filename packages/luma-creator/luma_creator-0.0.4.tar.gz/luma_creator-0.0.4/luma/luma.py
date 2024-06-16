import argparse
import os
import time
from http.cookies import SimpleCookie
from datetime import datetime
from urllib.parse import urlparse, unquote

from fake_useragent import UserAgent
import requests
from requests.utils import cookiejar_from_dict

browser_version = "edge101"
ua = UserAgent(browsers=["edge"])

class VideoGen:
    def __init__(self, cookie, image_file="") -> None:
        self.session: requests.Session = requests.Session()
        self.cookie = cookie
        self.session.cookies = self.parse_cookie_string(self.cookie)
        self.image_file = image_file
        print(self.image_file)

    @staticmethod
    def parse_cookie_string(cookie_string):
        cookie = SimpleCookie()
        cookie.load(cookie_string)
        cookies_dict = {}
        cookiejar = None
        for key, morsel in cookie.items():
            cookies_dict[key] = morsel.value
            cookiejar = cookiejar_from_dict(
                cookies_dict, cookiejar=None, overwrite=True
            )
        return cookiejar

    def get_limit_left(self) -> int:
        self.session.headers["user-agent"] = ua.random
        url = "https://internal-api.virginia.labs.lumalabs.ai/api/photon/v1/subscription/usage"
        r = self.session.get(url)
        if not r.ok:
            raise Exception("Can not get limit left.")
        data = r.json()
        return int(data["available"])

    def get_signed_upload(self):
        url = "https://internal-api.virginia.labs.lumalabs.ai/api/photon/v1/generations/file_upload"
        params = {
            'file_type': 'image',
            'filename': 'file.jpg'
        }
        response = self.session.post(url, params=params,)
        response.raise_for_status()
        return response.json()

    def upload_file(self):
        try:
            signed_upload = self.get_signed_upload()
            presigned_url = signed_upload['presigned_url']
            public_url = signed_upload['public_url']

            with open(self.image_file, 'rb') as file:
                response = self.session.put(presigned_url, data=file,
                                        headers={'Content-Type': "image/png", "Referer": "https://lumalabs.ai/",
                                                "origin": "https://lumalabs.ai"})

            if response.status_code == 200:
                print("Upload successful:", public_url)
                return public_url
            else:
                print("Upload failed.")
        except Exception as e:
            print("Upload failed.")
            print("Error uploading image:", e)

    def refresh_dream_machine(self):
        url = "https://internal-api.virginia.labs.lumalabs.ai/api/photon/v1/user/generations/"
        querystring = {"offset": "0", "limit": "10"}

        response = self.session.get(url, params=querystring)
        return response.json()

    @staticmethod
    def generate_slug(url):
        path = urlparse(url).path
        filename = os.path.basename(unquote(path))
        slug, _ = os.path.splitext(filename)
        return slug

    def save_video(
        self,
        prompt: str,
        output_dir: str,
    ) -> None:
        url = "https://internal-api.virginia.labs.lumalabs.ai/api/photon/v1/generations/"

        if self.image_file:
            print("uploading image")
            img_url = self.upload_file()
            payload = {
                "aspect_ratio": "16:9",
                "expand_prompt": True,
                "image_url": img_url,
                "user_prompt": prompt
            }
        else:
            payload = {
                "user_prompt": prompt,
                "aspect_ratio": "16:9",
                "expand_prompt": True
            }

        headers = {
            "Origin": "https://lumalabs.ai",
            "Referer": "https://lumalabs.ai",
            "content-type": "application/json"
        }
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        try:
            r = self.session.post(url, json=payload, headers=headers).json()
            task_id = r[0]["id"]
        except Exception as e:
            print(e)
            print("Another try")
            r = self.session.post(url, json=payload, headers=headers).json()
            task_id = r[0]["id"]
        start = time.time()
        video_url = ""
        while True:
            if int(time.time() - start) > 1200:
                raise Exception("Error 20 minutes passed.")
            response_json = self.refresh_dream_machine()
            for it in response_json:
                if it["id"] == task_id:
                    print(f"proceeding state {it['state']}")
                    if it["state"] == "pending":
                        print("pending in queue will wait more time")
                        time.sleep(30)
                    if it["state"] == "failed":
                        print("generate failed")
                        raise
                    if it['video']:
                        print(f"New video link: {it['video']['url']}")
                        video_url = it['video']['url']
                    break
            if video_url:
                break
            time.sleep(3)
            print("sleep 3")
        content = self.session.get(video_url)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        slug = self.generate_slug(video_url)
        video_path = f"{output_dir}/output_{slug}.mp4"

        with open(video_path, "wb") as f:
            f.write(content.content)
        print(f"Video saved to {video_path}")
        return video_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", help="Auth cookie from browser", type=str, default="")
    parser.add_argument("-I", help="image file path if you want use image", type=str, default="")
    parser.add_argument(
        "--prompt",
        help="Prompt to generate images for",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        help="Output directory",
        type=str,
        default="./output",
    )

    args = parser.parse_args()

    # Create video generator
    # follow old style
    video_generator = VideoGen(
        os.environ.get("LUMA_COOKIE") or args.U,
        image_file=args.I,
    )
    print(f"Left {video_generator.get_limit_left()} times.")
    video_generator.save_video(
        prompt=args.prompt,
        output_dir=args.output_dir,
    )

if __name__ == "__main__":
    main()
