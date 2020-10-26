from templates import requester
import json

class Sub_Enum:

    def __init__(self,domain,path):

        self.domain =f"%25.{domain}"
        self.path = path
        self.subdomains = []
        self.wildcardsubdomains = []

    def crtsh_subdomain_enum(self):

        try:
            url = f"https://crt.sh/?q={self.domain}&output=json"

            r = requester.requester(url,time=20)

            jsondata = json.loads(r.content.decode())

            with open (self.path,'a') as f :

                for i in range(len(jsondata)):

                            name_value = jsondata[i]['name_value']

                            if name_value.find('\n'):

                                subname_value = name_value.split('\n')

                                for subname_value in subname_value:

                                    if "*" not in subname_value:

                                        if subname_value not in self.subdomains:
                                            f.write(subname_value+'\n')
                                            self.subdomains.append(subname_value)
                                    else:

                                        if subname_value not in self.wildcardsubdomains:
                                            self.wildcardsubdomains.append(subname_value)
        except:

            pass
  
    def iterate_through_wildcards(self):

        try:

            for wildcardsubdomain in self.wildcardsubdomains:
                
                self.domain = wildcardsubdomain.replace('*.','%25.')
                self.crtsh_subdomain_enum()

            print(f"SUBDOMAIN ENUMERATION COMPLETED---> {self.path}")

        except:

            pass

    
  

