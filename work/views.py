from .models import Project
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    all_projects = Project.objects.all()
    paginator = Paginator(all_projects, 6)  # Show 5 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'templates/work/index.html' , {'page_obj': page_obj})


def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project_images = project.projectimage_set.all()
    return render(request, "templates/work/project.html", {"project": project})
