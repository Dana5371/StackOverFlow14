from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . serializers import ProblemSerializer
from main.models import *
from main.serializers import *
from .permissions import IsAuthorPermission
from rest_framework.decorators import action
from django.db.models import Q


# class ProblemListView(ListAPIView):
#     queryset = Problem.objects.all()
#     serializer_class = ProblemListSerializer
#
#
# class ProblemCreateView(CreateAPIView):
#     queryset = Problem.objects.all()
#     serializer_class = ProblemCreateSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}

class PermssionMixin:
    def get_permissions(self):

        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        elif self.action == 'create':
            permissions = [IsAuthenticated,]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProblemViewSet(PermssionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(title__icontains=query) | Q(description__icontains=query))
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ReplyViewSet(PermssionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class CommentViewSet(PermssionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


