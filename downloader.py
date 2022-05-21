import os
import requests

class Downloader(object):
    def __init__(self, fileName, url):
        self.__fileName = fileName
        self.__fileName_download = self.__fileName + '.download'
        self.__url = url

    def Download(self):
        try:
            if os.path.exists(self.__fileName):
                os.remove(self.__fileName)

            if os.path.exists(self.__fileName_download):
                os.remove(self.__fileName_download)

            r = requests.get(self.__url)
            with open(self.__fileName_download,'wb') as f:
                f.write(r.content)

            if os.path.exists(self.__fileName):
                os.remove(self.__fileName)
            else:
                os.rename(self.__fileName_download, self.__fileName)
        except Exception as e:
            print(f'%s download failed: %s' % (os.path.basename(self.__fileName), e))
