import json

from django.db.models import Count
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from user.models import User, UserSerializer, UserPostSerializer


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super(UserListView, self).get(request, *args, **kwargs)
        user_serializer = UserSerializer(self.object_list.select_related('location'), many=True)
        return JsonResponse(user_serializer.data, safe=False, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            super(UserDetailView, self).get(request, *args, **kwargs)
        except Http404 as error:
            return JsonResponse({'error': error.args}, status=404)
        User.objects.annotate(published=Count('is_published'))
        ads_serializer = UserSerializer(self.object)
        return JsonResponse(ads_serializer.data, safe=False, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super(UserCreateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        serializer = UserPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=422)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ('username',)

    def patch(self, request, *args, **kwargs):
        super(UserUpdateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        serializer = UserPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.update(self.object, serializer.validated_data)
            model = UserSerializer(self.object)
            return JsonResponse(model.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=422)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super(UserDeleteView, self).delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, safe=False, status=204)
