
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import MyUser
from account.serializers import RegisterSerializer


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered in StackO  verFlow14!', status=201)


class ActivateView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = MyUser.objects.filter(phone_number=phone_number, activation_code=code).first()

        if not user:
            return Response('No such user!', status=400)

        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('You successfully activated your account!', status=200)
