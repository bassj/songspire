import subprocess

from threading import Thread

class DownloadWorker:
    def __init__(self, download_queue, cache_path):
        self.download_queue = download_queue
        self.cache_path = cache_path
        self.worker_thread = None
        self.should_close = False

    def Start(self):
        self.worker_thread = Thread(target=self.__worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        print("Staring DownloadWorker")

    def Join(self):
        self.worker_thread.join()

    def __worker(self):
        while not self.should_close:
            
            if not self.download_queue.empty():
                video = self.download_queue.get();
           
                video_url = "https://www.youtube.com%s" % video['link'] 

                subprocess.call(['youtube-dl', '-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3', '--audio-quality', '0', video_url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=self.cache_path)
               
