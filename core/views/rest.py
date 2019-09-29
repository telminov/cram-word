from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

import core.ya_dictionary
from core import serializers


class YaDictFromRus(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = serializers.YaDictFromRus(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = core.ya_dictionary.from_rus(
            rus_word=serializer.validated_data['rus_word'],
            lang_code=serializer.validated_data['lang'].code,
        )

        return Response(result)


class YaDictToRus(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = serializers.YaDictToRus(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = core.ya_dictionary.to_rus(
            word=serializer.validated_data['word'],
            lang_code=serializer.validated_data['lang'].code,
        )

        return Response(result)

