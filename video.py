from moviepy.editor import VideoFileClip,VideoClip,concatenate_videoclips

def cut_episodes(episode_iter,video_clip:VideoFileClip,log_title=None):
    for episode in episode_iter:
        start,end=episode
        if log_title:
            print(f"{log_title} -> {start}-{end}")
        yield video_clip.subclip(start,end)

def make_block(timing_dict,name:str):
    open_clips=[]
    episodes=[]
    print(f'---------{name}-----------')
    for file in timing_dict:
        timings=timing_dict[file]
        clip=VideoFileClip(file)
        open_clips.append(clip)
        episodes.extend(list(cut_episodes(timings,clip,log_title=file)))
    print(f'episodes_count={len(episodes)}')
    
    final=concatenate_videoclips(episodes)
    print(f'total_duration={final.duration}')
    final.write_videofile(f'{name}.mp4')
    
    [clip.close() for clip in open_clips]
