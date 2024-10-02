from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.views import generic
from .models import Property
from datetime import datetime

# Create your views here.


class IndexView(generic.ListView):
    template_name = "realestate/index.html"
    context_object_name = "realestate_list"

    def get_queryset(self):
        """
        Return property data
        """
        return Property.objects.all()


def detail(request, property_id):
    try:
        property = Property.objects.get(pk=property_id)
    except Property.DoesNotExist:
        raise Http404("Property does not exist")
    return render(request, "realestate/detail.html", {"property": property})


def create(request):
    return render(request, "realestate/create.html")


def submit(request):
    address_number = request.POST["address_number"]
    address_street = request.POST["address_street"]
    last_updated = datetime.now()
    property = Property(
        address_number=address_number,
        address_street=address_street,
        last_updated=last_updated,
    )
    property.save()
    return HttpResponseRedirect("/realestate/")
