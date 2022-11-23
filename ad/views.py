import json

from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from ad.models import Ad, AdListSerializer, AdPostSerializer, AdPatchSerializer
from avito import settings


def index(request):
    if request.method == 'GET':
        return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super(AdListView, self).get(request, *args, **kwargs)
        paginator = Paginator(self.object_list.select_related('author').prefetch_related('category').order_by('-price'),
                              settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        ads_serializer = AdListSerializer(page_object, many=True)
        response = {
            'items': ads_serializer.data,
            'total': paginator.count,
            'num_pages': paginator.num_pages,
        }
        return JsonResponse(response, safe=False, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super(AdCreateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        serializer = AdPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=422)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            super(AdDetailView, self).get(request, *args, **kwargs)
        except Http404 as error:
            return JsonResponse({'error': error.args}, status=404)
        ads_serializer = AdListSerializer(self.object)
        return JsonResponse(ads_serializer.data, safe=False, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ('name',)

    def patch(self, request, *args, **kwargs):
        super(AdUpdateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        serializer = AdPatchSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.update(self.object, serializer.validated_data)
            model = AdListSerializer(self.object)
            return JsonResponse(model.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=422)


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super(AdDeleteView, self).delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, safe=False, status=204)


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ('name', 'image')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()
        return JsonResponse(
            {
                'id': self.object.id,
                'name': self.object.name,
                'image': self.object.image.url
            }
        )
