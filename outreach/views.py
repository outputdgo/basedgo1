from django.http import HttpResponse, Http404
from django.shortcuts import render ,get_object_or_404
from .models import OutreachPost
from django.core.paginator import Paginator
# Create your views here.
# def index(request):
    # all_outreach_posts = OutreachPost.objects.all()
    # output = ', '.join([outreach.title for outreach in all_outreach_posts])
    # return HttpResponse("Outreach Posts: %s" % output)

def index(request):
    all_outreach_posts = OutreachPost.objects.all()
    paginator = Paginator(all_outreach_posts, 5)  # Show 5 outreach posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'templates/outreach/index.html', {'page_obj': page_obj})


def detail(request, outreachpost_id):
    outreach = get_object_or_404(OutreachPost, pk=outreachpost_id)
    images = outreach.outreachimage_set.all()
    return render(request, "templates/outreach/post.html", {"outreach": outreach})

