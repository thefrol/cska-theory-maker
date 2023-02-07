order_filename='order.txt'
year='2009'


from posixpath import split
import re
from pprint import pprint

from helpers import get_video_files, user_wants_to_continue
from video import make_block

video_files=get_video_files(year=year)
print(f'found videos: {video_files}')

#reading order
with open(order_filename,'r',encoding='utf8') as f:
    order=f.read()

#spliting parts
print(order)
pprint(order.splitlines())

def normalize_string(string):
    return re.sub('[\n \s]+',' ',string)

def split_parts(order:str):
    parts=[]
    current_string=''
    for s in order.splitlines():
        debug= re.search('[а-яА-Яa-zA-Z]+',s)
        if re.search('[а-яА-Яa-zA-Z]+',s) and current_string.strip():
            parts.append(current_string)
            current_string=''
        current_string=current_string+s
    parts.append(current_string) #adding whats left
    return [normalize_string(p) for p in parts]


parts=split_parts(order)
pprint(parts)

#forming parts
def get_part_name(string):#получает имя нарезки атака или оборона или еще чего
    s=string.lower()
    s=re.sub('[\d .\-]{3,}','',s) #удаляем тайминги
    #s=re.sub('(\d{1}\s*тайм)|(тайм\s*\d{1})','',s) # удаляем тайм
    s=re.sub('(\d{1}.{0,5}тайм)|(тайм.{0,5}\d{1})','',s) # удаляем тайм
    s=re.search('\w.*\w',s).group(0)
    return s

def get_period(string):
    match=re.search('(\d{1})\s*тайм|тайм\s*(\d{1})',string)
    return int(match.group(1) or match.group(2))

def parse_episode(episode):
    if len(episode)<4:
        print(f"WARN: error parsing episode {episode}")
        return None
    start_min,start_sec,end_min,end_sec=episode
    return f'{start_min}:{start_sec}',f'{end_min}:{end_sec}'


def get_timings(string):
    for episode in  re.findall('(\d+)\D+(\d+)\D*\-\D*(\d+)\D+(\d+)',string):
        result_tuple=parse_episode(episode)
        if not result_tuple:
            if not user_wants_to_continue():
               exit()
            continue
        yield result_tuple


blocks={}
for part in parts:
    block_name=get_part_name(part)
    period_int=get_period(part)
    period_file=video_files[period_int]
    timings=list(get_timings(part))

    if block_name not in blocks:
        blocks[block_name]={}
    blocks[block_name][period_file]=timings
    # атака:
    #   2008-1.mp4:
    #       ('01.00','02.22'),...
    #
    #

#sort by period
for block in blocks:
    blocks[block]= dict(sorted(blocks[block].items()))

pprint(blocks)

for block_name in blocks:
    timing_dict=blocks[block_name]
    make_block(timing_dict,block_name)