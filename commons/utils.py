import os
import uuid
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def comma_splitter(tag_string):
    return [t.strip().lower() for t in tag_string.split(',') if t.strip()]

def comma_joiner(tags):
    return ', '.join(t.name for t in tags)

def ffmpeg(request):
    base_path = os.path.join(BASE_DIR, 'media')
    input_file = "Smoul.mp4"
    input_path = os.path.join(base_path, input_file)

    output_file = "{}.webm".format(uuid.uuid4())
    output_path = os.path.join(base_path, os.path.join('previews', output_file))
    
    print("base_path", input_path)
    os.system("""
        ffmpeg -y -hide_banner -i {} -filter_complex "\
        [0:v]trim=start=10:duration=1,setpts=PTS-STARTPTS[av];\
        [0:v]trim=start=22:duration=1,setpts=PTS-STARTPTS[av1];\
        [0:v]trim=start=44:duration=1,setpts=PTS-STARTPTS[av2];\
        [0:v]trim=start=66:duration=1,setpts=PTS-STARTPTS[av3];\
        [0:v]trim=start=88:duration=1,setpts=PTS-STARTPTS[av4];\
        [0:v]trim=start=110:duration=1,setpts=PTS-STARTPTS[av5];\
        [0:v]trim=start=132:duration=1,setpts=PTS-STARTPTS[av6];\
        [0:v]trim=start=154:duration=1,setpts=PTS-STARTPTS[av7];\
        [0:v]trim=start=176:duration=1,setpts=PTS-STARTPTS[av8];\
        [av][av1][av2][av3][av4][av5][av6][av7][av8]concat=n=9:v=1[outv];[outv]scale=260:-1[outv1];[outv1]crop=iw:iw*0.55[outv2]" -map [outv2] -c:v libvpx -crf 10 -b:v 1M -c:a libvorbis {}

    """.format(input_path, output_path ))