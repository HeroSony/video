from config import theme
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from video.models import Video
from config import site_title

from django.views.generic import DetailView, TemplateView
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
import os
from django.views.generic import ListView
import requests
from datetime import date, timedelta

class PostMixinDetailView(object):
    model = Video
    template_name = theme + '/pages/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)

        items = Video.objects.order_by('-created_at').filter(active='A')
        paginator = Paginator(items, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)

        # Test FFMPEG
        from commons.utils import ffmpeg
        ffmpeg(self.request)

        context['videos'] = videos
        # context['videos'] = Video.objects.order_by('-created_at').filter(active='A')[:12]
        # context['post_views'] = ["ajax", "detail", "detail-with-count"]

        return context

class IndexView(PostMixinDetailView, TemplateView):
    template_name = theme + '/pages/index.html'

class PostDetailView(PostMixinDetailView, HitCountDetailView):
    template_name = theme + '/pages/video.html'
    # model = Video
    count_hit = True

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context['aaa'] = 'Hello'
    #     return context


# def index(request):
#     videos = Video.objects.order_by('-created_at').filter(active='A')[:12]

#     context = {
#         'videos': videos,
#     }
#     return render(request, theme + '/pages/index.html', context)

# def video(request, video_id):
#     video = get_object_or_404(Video, pk=video_id)

#     context = {
#         'video': video
#     }
#     return render(request, theme + '/pages/video.html', context)


def dmca(request):
    return render(request, theme + '/pages/dmca.html')

def statement(request):
    return render(request, theme + '/pages/2257.html')
    
def contact(request):
    return render(request, theme + '/pages/contact.html')

def flash(request):

    try:
        user = "herosony"
        album = "vSHWsoKl"
        response = requests.get('https://api.gfycat.com/v1/users/'+user+'/albums/'+album)
    except requests.exceptions.ConnectionError as e:
        return render(request, theme + '/errors/something_went_wrong.html')

    data = response.json()

    context = {
        'data': data['publishedGfys']
    }
    
    # print(data['publishedGfys'])
    return render(request, theme + '/pages/flash.html', context)

def search(request):
    queryset_list = Video.objects.order_by('-created_at').filter(active='A')
    keywords_key = ''
    mostview_key = ''

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(title__icontains=keywords)
            
            keywords_key = keywords.strip()

    # Most View
    if 'mostview' in request.GET:
        mostview = request.GET['mostview']
        if mostview:
            if mostview == "a": # all
                queryset_list = queryset_list.order_by("-hit_count_generic__hits")
            if mostview == "w": # week
                d = date.today() - timedelta(days=7)
                queryset_list = queryset_list.order_by("-hit_count_generic__hits").filter(created_at__gte=d)
            if mostview == "m": # month
                d = date.today() - timedelta(days=30)
                queryset_list = queryset_list.order_by("-hit_count_generic__hits").filter(created_at__gte=d)
            
            mostview_key = request.GET['mostview'].strip()

    # Tags
    if 'tags' in request.GET:
        tags = request.GET['tags']
        if tags:
            tags = tags.split(',')
            # print(tags)
            queryset_list = queryset_list.filter(tags__slug__in=tags).distinct()

    context = {
        'videos': queryset_list,
        'keywords': keywords_key,
        'mostview': mostview_key,
    }

    return render(request, theme + '/pages/search.html', context)




# preview size
# 260x140
# Crawlers Video Concepts
# Get video durations in seconds :A
# Creating a compilation clip(9x) based on cuts in a video using ffmpeg
# :A / 9 = :B
"""
.\ffmpeg.exe -y -hide_banner -i .\Smoul.mp4 -filter_complex "
[0:v]trim=start=10:duration=1,setpts=PTS-STARTPTS[av];
[0:v]trim=start=22:duration=1,setpts=PTS-STARTPTS[av1];
[0:v]trim=start=44:duration=1,setpts=PTS-STARTPTS[av2];
[0:v]trim=start=66:duration=1,setpts=PTS-STARTPTS[av3];
[0:v]trim=start=88:duration=1,setpts=PTS-STARTPTS[av4];
[0:v]trim=start=110:duration=1,setpts=PTS-STARTPTS[av5];
[0:v]trim=start=132:duration=1,setpts=PTS-STARTPTS[av6];
[0:v]trim=start=154:duration=1,setpts=PTS-STARTPTS[av7];
[0:v]trim=start=176:duration=1,setpts=PTS-STARTPTS[av8];
[av][av1][av2][av3][av4][av5][av6][av7][av8]concat=n=9:v=1[outv];[outv]scale=260:-1[outv1];[outv1]crop=iw:iw*0.55[outv2]" -map [outv2] -c:v libvpx -crf 10 -b:v 1M -c:a libvorbis out.webm


.\ffmpeg.exe -y -hide_banner -i .\Smoul.mp4 -filter_complex "
[0:v]trim=start=10:duration=2.5,setpts=PTS-STARTPTS[av];
[0:a]atrim=start=10:duration=2.5,asetpts=PTS-STARTPTS[aa];
[0:v]trim=start=40:duration=2.5,setpts=PTS-STARTPTS[av1];
[0:a]atrim=start=40:duration=2.5,asetpts=PTS-STARTPTS[aa1];
[0:v]trim=start=80:duration=2.5,setpts=PTS-STARTPTS[av2];
[0:a]atrim=start=80:duration=2.5,asetpts=PTS-STARTPTS[aa2];
[0:v]trim=start=120:duration=2.5,setpts=PTS-STARTPTS[av3];
[0:a]atrim=start=120:duration=2.5,asetpts=PTS-STARTPTS[aa3];
[0:v]trim=start=160:duration=2.5,setpts=PTS-STARTPTS[av4];
[0:a]atrim=start=160:duration=2.5,asetpts=PTS-STARTPTS[aa4];
[av][aa][av1][aa1][av2][aa2][av3][aa3][av4][aa4]concat=n=5:v=1:a=1[outv][outa]" -map [outv] -map [outa] -c:v libvpx -crf 10 -b:v 1M -c:a libvorbis out.webm



"""

