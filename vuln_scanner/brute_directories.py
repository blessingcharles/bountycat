from templates.requester import requester
from templates.logger import Logger
import concurrent.futures


class Brute:

    def __init__(self,domain,path,dir_list,thread=10):

        self.file_name = domain.replace('.','_')
        self.file_path = f"{path}/{self.file_name}_directory_bruteforcing_results.txt"  
        self.url =  f"https://{domain}/"
        self.dir_list = dir_list
        self.thread = thread
        self.a_logger = Logger(self.file_path)
        self.log = self.a_logger.start()

    def brute(self,name):

        try:
            
            req_url = self.url+name
            r = requester(req_url,time=10)
            
            print(f"trying {req_url}                                                          ",end="\r",flush=True)
            if(r.status_code < 400):
                self.log.info(f"{req_url} -----> {r.status_code}")
        except:
            pass

    def dir_brute(self):

        with open(self.dir_list,'r') as dirs: 

            names = dirs.readlines()
            names = list(map(lambda x: x.strip(),names))

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread) as executor:

            executor.map(self.brute,names) 

        self.a_logger.close_logging()





