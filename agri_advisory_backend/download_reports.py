import os
import requests

# Define our destination directory
DOWNLOAD_DIR = "./data_sources"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Map of verified direct PDF URLs from the ICAR portals
ICAR_REPORTS = {
    "ICAR_Annual_Report_2024-25.pdf": "https://icar.org.in/sites/default/files/2025-10/ICAR%20Eng%20Annual%20Report_2024-25.pdf",
    "ICAR_Annual_Report_2023-24_English.pdf": "https://icar.org.in/sites/default/files/2025-04/ICAR%20Annual%20Report%202023-24-english.pdf",
    "ICAR_Annual_Report_2022-23_English.pdf": "https://icar.org.in/sites/default/files/2025-04/ICAR-Annual-Report-2022-23-English.pdf",
    "ICAR_Annual_Report_2021-22_English.pdf": "https://icar.org.in/sites/default/files/2022-09/AR-2021-22.pdf",
    "ICAR_Annual_Report_2020-21_English.pdf": "https://icar.org.in/sites/default/files/2022-09/ICAR-AR-2020.pdf",
    "DARE_ICAR_Annual_Report_2019-20.pdf": "https://icar.org.in/sites/default/files/2022-09/AR-2019-20.pdf",
    "DARE_ICAR_Annual_Report_2018-19.pdf": "https://icar.org.in/sites/default/files/2020-10/DARE-ICAR-Annual-Report-2018-19.pdf",
    "DARE_ICAR_Annual_Report_2017-18.pdf": "https://icar.org.in/sites/default/files/2019-10/DARE-ICAR-Annual-Report-2017-18.pdf",
    "DARE_ICAR_Annual_Report_2016-17.pdf": "https://icar.org.in/sites/default/files/2018-10/DARE-ICAR-Annual-Report-2016-17.pdf"
}

def download_file(filename: str, url: str):
    target_path = os.path.join(DOWNLOAD_DIR, filename)
    print(f"\n📥 Starting download: {filename}")
    print(f"🔗 Source: {url}")
    
    try:
        # Stream the download so it doesn't overload system memory for large files
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Get total file size from headers (if available)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(target_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r progress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB)", end="")
            print(f"\n✅ Successfully saved to: {target_path}")
            
    except Exception as e:
        print(f"\n❌ Error downloading {filename}: {e}")

if __name__ == "__main__":
    print("🌾 Starting ICAR Agricultural Manual Downloader 🌾")
    for filename, url in ICAR_REPORTS.items():
        download_file(filename, url)
    print("\n🏁 All downloads completed!")