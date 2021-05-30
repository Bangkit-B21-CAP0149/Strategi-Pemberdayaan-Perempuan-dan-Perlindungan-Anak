import re
from urllib.parse import urlparse
from urllib.request import urlopen
import queue
import threading


class Extractor:

    @staticmethod
    def create_url_list(data, list_url_column):
        url_list = []
        try:
            for x in data:
                if x[list_url_column] != []:
                    for url in x[list_url_column]:
                        url_list.append(url['expanded_url'])
            return url_list
        except Exception as e:
            return str(e)

    @staticmethod
    def extract_url(url, queue):
        try:
            expanded_url = urlopen(url).url
            data = urlparse(expanded_url).netloc
            queue.put(data)
        except Exception as e:
            pass

    @staticmethod
    def parallel_url_extractor(list_url):
        result = queue.Queue()
        try:
            threads = [threading.Thread(target=Extractor.extract_url, args=(url, result)) for url in list_url]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            return list(result.queue)
        except Exception as e:
            print(e)


