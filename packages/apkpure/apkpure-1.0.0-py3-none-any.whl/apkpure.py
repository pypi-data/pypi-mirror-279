import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class ApkPure:
    def helper(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup

    def search_top(self, name: str) -> str:
        url = f"https://apkpure.com/search?q={name}"
        soup = self.helper(url)
        result = soup.find("div", class_="first")
        package_url = result.find("a", class_="first-info brand-info").attrs["href"]
        title = result.find("p", class_="p1").text.strip()
        developer = result.find("p", class_="p2").text.strip()
        icon = result.find("img").attrs["src"]
        dl_btn = result.attrs
        package_name = dl_btn["data-dt-app"]
        package_size = dl_btn["data-dt-filesize"]
        package_version = dl_btn["data-dt-version"]
        package_versioncode = dl_btn["data-dt-versioncode"]
        download_link = result.find("a", class_="is-download").attrs["href"]

        new = {
            "title": title,
            "developer": developer,
            "package_name": package_name,
            "package_url": package_url,
            "icon": icon,
            "version": package_version,
            "version_code": package_versioncode,
            "size": package_size,
            "download_link": download_link,
        }
        return json.dumps(new)

    def search_all(self, name: str) -> str:
        full = []

        url = f"https://apkpure.com/search?q={name}"

        first = self.search_top(name)
        full.append(json.loads(first))
        soup = self.helper(url)
        results = soup.find("div", class_="list sa-apps-div app-list")
        ul = results.find_all("li")
        for li in ul:
            package_url = li.find("a", class_="dd", href=True).attrs["href"]
            title = li.find("p", class_="p1").text.strip()
            developer = li.find("p", class_="p2").text.strip()
            icon = li.find("img").attrs["src"]
            dl_btn = li.find("a", class_="is-download").attrs
            package_name = dl_btn["data-dt-app"]
            package_size = dl_btn["data-dt-filesize"]
            package_version = dl_btn["data-dt-version"]
            package_versioncode = dl_btn["data-dt-versioncode"]
            download_link = dl_btn["href"]

            new = {
                "title": title,
                "developer": developer,
                "package_name": package_name,
                "package_url": package_url,
                "icon": icon,
                "version": package_version,
                "version_code": package_versioncode,
                "size": package_size,
                "download_link": download_link,
            }
            full.append(new)
        return json.dumps(full)

    def get_versions(self, name) -> str:
        s = json.loads(self.search_top(name))
        url = f"{s["package_url"]}/versions"
        soup = self.helper(url)

        full = [{"app": s["package_name"]}]
        ul = soup.find("ul", class_="ver-wrap")
        lists = ul.find_all("li")
        lists.pop()
        for li in lists:
            dl_btn = li.find("a", class_="ver_download_link").attrs
            package_version = dl_btn["data-dt-version"]
            download_link = dl_btn["href"]

            package_versioncode = dl_btn["data-dt-versioncode"]

            new = {
                "version": package_version,
                "download_link": download_link,
                "version_code": package_versioncode,
            }
            full.append(new)
        return json.dumps(full)

    def get_info(self, name: str) -> str:
        url = json.loads(self.search_top(name))["package_url"]
        soup = self.helper(url)

        divs = soup.find("div", class_="detail_banner")
        title = divs.find("div", class_="title_link").get_text(strip=True)
        rating = divs.find("span", class_="rating").get_text(strip=True)
        date = divs.find("p", class_="date").text.strip()
        sdk_info = divs.find("p", class_="details_sdk")
        latest_version = sdk_info.contents[1].get_text(strip=True)
        developer = sdk_info.contents[3].get_text(strip=True)
        dl_btn = divs.find("a", class_="download_apk_news").attrs
        package_name = dl_btn["data-dt-package_name"]
        package_versioncode = dl_btn["data-dt-version_code"]
        download_link = dl_btn["href"]

        # Find the Description
        description = soup.find("div", class_="translate-content").get_text()

        # Older Versions
        versions = json.loads(self.get_versions(name))
        new = {
            "title": title,
            "rating": rating,
            "date": date,
            "latest_version": latest_version,
            "description": description,
            "developer": developer,
            "package_name": package_name,
            "package_versioncode": package_versioncode,
            "package_url": download_link,
            "older_versions": versions,
        }
        return json.dumps(new)

    def download(self, name: str, version=None):
        versions = json.loads(self.get_versions(name))
        url = ""
        if version == None:
            url = f"https://d.apkpure.com/b/APK/{versions[0]["app"]}?versionCode={versions[1]["version_code"]}"
            print(url)
            print("Downloading Latest")
            self.downloader(url, f"{name}-Latest.apk")
            return
        for v in versions[1:]:
            if version == v["version"]:
                url = f"https://d.apkpure.com/b/APK/{versions[0]["app"]}?versionCode={v["version_code"]}"
                break
        if url == "":
            print(f"Invalid Version: {version}")
            return
        print(f"Downloading v{version}")
        self.downloader(url, f"{name}-{version}.apk")

    def downloader(self, url: str, name: str):
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, stream=True, allow_redirects=True, headers=headers)

        with tqdm.wrapattr(
            open(name, "wb"),
            "write",
            miniters=1,
            total=int(r.headers.get("content-length", 0)),
        ) as file:
            for chunk in r.iter_content(chunk_size=4 * 1024):
                if chunk:
                    file.write(chunk)
        print("Download Complete")
