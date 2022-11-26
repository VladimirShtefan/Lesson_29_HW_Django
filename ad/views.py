import json

from django.db.models import Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView

from ad.serializers import AdListSerializer, AdPostSerializer, AdPatchSerializer
from ad.serializers import Ad


def index(request):
    if request.method == 'GET':
        return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        category_ids = request.GET.getlist('cat', None)
        text = request.GET.get('text', None)
        location = request.GET.get('location', None)
        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        search_query = None
        for category_id in category_ids:
            if search_query is None:
                search_query = Q(category__id__exact=category_id)
            else:
                search_query |= Q(category__id__exact=category_id)
        if text:
            if search_query is None:
                search_query = Q(name__icontains=text)
            else:
                search_query |= Q(name__icontains=text)
        if location:
            if search_query is None:
                search_query = Q(author__location__name__icontains=location)
            else:
                search_query |= Q(author__location__name__icontains=location)
        if price_from:
            if search_query is None:
                search_query = Q(price__gte=price_from)
            else:
                search_query &= Q(price__gte=price_from)
        if price_to:
            if search_query is None:
                search_query = Q(price__lte=price_to)
            else:
                search_query &= Q(price__lte=price_to)
        if search_query:
            self.queryset = self.queryset.select_related('author').prefetch_related('category').filter(search_query).\
                order_by('-price')
        return super(AdListView, self).get(request, *args, **kwargs)


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
