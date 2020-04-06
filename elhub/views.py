from django.shortcuts import render

from elhub.models import Forks


def el_hub(request):
    model_forks = Forks.objects.all()
    context = {'forks': model_forks}
    return render(request, 'elhub/main.html', context)