def user_wants_to_continue():
    while True:
        inp=input('continue [y/n]').lower()
        if inp=='y':
            return True
        elif inp=='n':
            return False
        else:
            print('try again')

import os
import re
def get_video_files(year='2009'):
    ret={}
    for file in  os.listdir():
        match=re.search(f'{year}-(\d).*',file)
        if match:
            period_num=int(match.group(1))
            if period_num in ret:
                print(f'more then 1 file with {period_num} period in folder')
                if not user_wants_to_continue():
                    exit()
            ret[period_num]=file
    return ret

