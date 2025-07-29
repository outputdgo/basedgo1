from django.shortcuts import render , get_object_or_404
from outreach.models import OutreachPost
from work.models import Project


# Create your views here.
def index(request):
    outreach_updates = OutreachPost.objects.order_by('-date')[:3]
    featured_project = Project.objects.filter(featured=True).order_by('-date').first()
    return render(request, 'templates/base/base.html', {
        'outreach_updates': outreach_updates,
        'featured_project': featured_project,
        })


def about(request):
    return render(request, 'templates/home/about.html')

