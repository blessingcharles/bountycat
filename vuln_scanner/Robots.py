
from templates.requester import requester


def robots_enum(domain):

    robots = ["robots.txt","robots"]
    for path in robots: 
        r = requester(f"{domain}/{path}",time=5)

        if(r.status_code <400):
            print(f"ROBOTS TEXT IN {domain}------>{r.status_code}")
            print(r.text)


