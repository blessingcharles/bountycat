import os

def dir_create(dirname):

    pwd = os.getcwd()

    new_dir_path = os.path.join(pwd,dirname)
    
    if not os.path.exists(new_dir_path):

        try:
            os.mkdir(new_dir_path)

            return new_dir_path

        except:

            pass

    return new_dir_path


dir_create("Bounty")
