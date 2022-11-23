import json

from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView

from location.models import Location, LocationSerializer, LocationPostSerializer


class LocationListView(ListView):
    model = Location

    def get(self, request, *args, **kwargs):
        super(LocationListView, self).get(request, *args, **kwargs)
        ads_serializer = LocationSerializer(self.object_list, many=True)
        return JsonResponse(ads_serializer.data, safe=False, status=200)


class LocationDetailView(DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        try:
            super(LocationDetailView, self).get(request, *args, **kwargs)
        except Http404 as error:
            return JsonResponse({'error': error.args}, status=404)
        ads_serializer = LocationSerializer(self.object)
        return JsonResponse(ads_serializer.data, safe=False, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class LocationCreateView(CreateView):
    model = Location
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super(LocationCreateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        serializer = LocationPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=422)
