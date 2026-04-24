"""
YouTube Comments Scraper - Mengumpulkan komentar dari video YouTube
I Putu Sutha Satyawan
"""

import pandas as pd
import time
import sys
import subprocess
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def check_and_install_requirements():
    """Memeriksa dan menginstall requirements jika diperlukan"""
    try:
        import pkg_resources
        with open('requirements.txt', 'r') as f:
            requirements = f.read().splitlines()
        
        print("Memeriksa dependencies...")
        for req in requirements:
            req = req.split('>=')[0].split('==')[0].strip()
            if req:
                try:
                    pkg_resources.get_distribution(req)
                    print(f"✓ {req} sudah terinstall")
                except pkg_resources.DistributionNotFound:
                    print(f"✗ {req} belum terinstall, menginstall...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        print("✅ Semua dependencies siap!\n")
    except FileNotFoundError:
        print("File requirements.txt tidak ditemukan, menginstall dependencies default...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-api-python-client", "pandas"])

class YouTubeCommentsScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def scrape_all_comments(self, video_id):
        """Scrape semua komentar dari video"""
        comments = []
        next_page_token = None
        page_count = 0
        
        print(f"\nMemulai scraping komentar untuk video ID: {video_id}")
        print("Mengumpulkan semua komentar yang tersedia...\n")
        
        while True:
            try:
                request = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token,
                    textFormat='plainText'
                )
                
                response = request.execute()
                
                for item in response['items']:
                    # Komentar utama
                    top_comment = item['snippet']['topLevelComment']['snippet']
                    comment_data = {
                        'comment_id': item['snippet']['topLevelComment']['id'],
                        'author_name': top_comment.get('authorDisplayName', 'Unknown'),
                        'author_channel_id': top_comment.get('authorChannelId', {}).get('value', ''),
                        'comment_text': top_comment.get('textDisplay', ''),
                        'like_count': top_comment.get('likeCount', 0),
                        'published_at': top_comment.get('publishedAt', ''),
                        'updated_at': top_comment.get('updatedAt', ''),
                        'is_reply': False,
                        'parent_id': None,
                        'total_reply_count': item['snippet'].get('totalReplyCount', 0)
                    }
                    comments.append(comment_data)
                    
                    # Proses replies jika ada
                    if 'replies' in item:
                        replies = item['replies']['comments']
                        for reply in replies:
                            reply_snippet = reply['snippet']
                            reply_data = {
                                'comment_id': reply['id'],
                                'author_name': reply_snippet.get('authorDisplayName', 'Unknown'),
                                'author_channel_id': reply_snippet.get('authorChannelId', {}).get('value', ''),
                                'comment_text': reply_snippet.get('textDisplay', ''),
                                'like_count': reply_snippet.get('likeCount', 0),
                                'published_at': reply_snippet.get('publishedAt', ''),
                                'updated_at': reply_snippet.get('updatedAt', ''),
                                'is_reply': True,
                                'parent_id': comment_data['comment_id'],
                                'total_reply_count': 0
                            }
                            comments.append(reply_data)
                    
                    if len(comments) % 200 == 0:
                        print(f"Progress: {len(comments):,} komentar terkumpul...")
                
                next_page_token = response.get('nextPageToken')
                page_count += 1
                
                if not next_page_token:
                    print("\nSudah mencapai halaman terakhir komentar.")
                    break
                
                time.sleep(0.5)
                
            except HttpError as e:
                print(f"HTTP Error: {e}")
                if e.resp.status == 403:
                    print("Quota API habis. Silakan coba lagi nanti.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
        
        print(f"\nSelesai! Total komentar terkumpul: {len(comments):,}")
        return comments
    
    def save_to_csv(self, comments, video_title, video_id):
        """Menyimpan komentar ke CSV (tanpa file summary)"""
        if not comments:
            print("Tidak ada komentar untuk disimpan.")
            return None
        
        df = pd.DataFrame(comments)
        df['video_title'] = video_title
        df['video_id'] = video_id
        
        # Bersihkan teks komentar
        df['comment_text'] = df['comment_text'].str.replace('\n', ' ', regex=False)
        df['comment_text'] = df['comment_text'].str.replace('\r', ' ', regex=False)
        df['comment_text'] = df['comment_text'].str.strip()
        
        # Buat nama file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"youtube_comments_{timestamp}.csv"
        
        # Simpan ke CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ Data berhasil disimpan ke: {filename}")
        print(f"📊 Total komentar: {len(comments):,}")
        print(f"   - Komentar utama: {sum(1 for c in comments if not c['is_reply']):,}")
        print(f"   - Balasan: {sum(1 for c in comments if c['is_reply']):,}")
        
        return filename

def main():
    print("=" * 70)
    print("YOUTUBE COMMENTS SCRAPER")
    print("=" * 70)
    
    # Cek dan install requirements
    check_and_install_requirements()
    
    # Video target
    VIDEO_ID = "dSq0Z5XpoLc"
    VIDEO_TITLE = "Pertemuan Bersejarah dr. Tirta dan dr. Gia"
    
    print(f"\nVideo Target:")
    print(f"Judul: {VIDEO_TITLE}")
    print(f"Link: https://youtu.be/{VIDEO_ID}")
    
    # Input API Key
    print("\n" + "-" * 70)
    api_key = input("Masukkan YouTube API Key: ").strip()
    
    if not api_key:
        print("\n❌ ERROR: API Key tidak boleh kosong!")
        print("\n📝 Cara mendapatkan API Key:")
        print("1. Buka https://console.cloud.google.com/")
        print("2. Buat project baru")
        print("3. Enable 'YouTube Data API v3'")
        print("4. Buat credentials > API Key")
        sys.exit(1)
    
    # Inisialisasi scraper
    scraper = YouTubeCommentsScraper(api_key)
    
    try:
        # Scrape komentar
        comments = scraper.scrape_all_comments(VIDEO_ID)
        
        if comments:
            # Simpan ke CSV
            scraper.save_to_csv(comments, VIDEO_TITLE, VIDEO_ID)
            
            # Preview komentar teratas
            print("\n" + "=" * 70)
            print("🏆 TOP 5 KOMENTAR (Like Terbanyak):")
            print("=" * 70)
            
            sorted_comments = sorted(comments, key=lambda x: x['like_count'], reverse=True)
            for i, comment in enumerate(sorted_comments[:5], 1):
                print(f"\n[{i}] {comment['author_name']} ({comment['like_count']} likes):")
                text = comment['comment_text']
                if len(text) > 200:
                    text = text[:200] + "..."
                print(f"    {text}")
        else:
            print("❌ Tidak ada komentar yang berhasil diambil.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Scraping dihentikan oleh user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()