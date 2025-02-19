
from micropython import const
from collections import OrderedDict
import logging
import re


START_PARAM_TAG = const("{%") 
END_PARAM_TAG = const("%}")


class TextFileCache():
    def __init__(self, maxSize:int) -> None:
        self.maxSize = maxSize
        self.__fileCache = OrderedDict()


    def exists(self, filename:str) -> bool:
        return filename in self.__fileCache

    def get(self, filename:str) -> any:
        if self.exists( filename):
            return self.__fileCache[filename]
        else:
            # Errors must be handled by caller!
            with open(filename) as f:
                content = f.read()
            if len(self.__fileCache) > self.maxSize:
                # clear oldest member from cache
                self.__fileCache.pop(list(self.__fileCache.keys())[0])    
            self.__fileCache[filename] = content
            return content
        


__fileCache = TextFileCache(maxSize=5)
__reg = re.compile(START_PARAM_TAG)   # As usual couldnt find pattern to extract keyword, like {%.%}
def replaceParams(fname:str, **kwargs):
    global __reg, __fileCache

    try:
        fullText = __fileCache.get(fname)
    except Exception as ex:
        logging.error(f"Could not open file: {fname}. {ex}", )
        yield "Internal server error"
        return

    isKeyWord=False
    for txt in __reg.split(fullText):
        if isKeyWord:
            end = txt.find(END_PARAM_TAG)
            if end > 0:  
                kw = txt[:end].strip()
                sub = kwargs[kw]
                if sub != None:
                    yield str(sub)
                else:
                    yield f"Unknown keyword: {kw}"
                    logging.error("keyword not found:",kw)
                yield txt[end+2:]
            else:
                logging.warn(f"No closing was found for opening tag around {txt[:20]}...")
                yield txt
        else:
            yield txt
        isKeyWord = True
