import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, views, viewsets
from rest_framework.response import Response
from vng_api_common.permissions import AuthScopesRequired, ClientIdRequired
from vng_api_common.viewsets import CheckQueryParamsMixin

from nrc.datamodel.models import Abonnement, Kanaal

from .filters import KanaalFilter
from .scopes import (
    SCOPE_NOTIFICATIES_CONSUMEREN, SCOPE_NOTIFICATIES_PUBLICEREN
)
from .serializers import (
    AbonnementSerializer, KanaalSerializer, MessageSerializer
)

logger = logging.getLogger(__name__)


class AbonnementViewSet(CheckQueryParamsMixin,
                        viewsets.ModelViewSet):

    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    lookup_field = 'uuid'
    permission_classes = (AuthScopesRequired, ClientIdRequired)
    required_scopes = {
        'list': SCOPE_NOTIFICATIES_CONSUMEREN | SCOPE_NOTIFICATIES_PUBLICEREN,
        'retrieve': SCOPE_NOTIFICATIES_CONSUMEREN | SCOPE_NOTIFICATIES_PUBLICEREN,
        'create': SCOPE_NOTIFICATIES_CONSUMEREN,
        'destroy': SCOPE_NOTIFICATIES_CONSUMEREN,
        'update': SCOPE_NOTIFICATIES_CONSUMEREN,
        'partial_update': SCOPE_NOTIFICATIES_CONSUMEREN,
    }

    def perform_create(self, serializer):
        client_id = self.request.jwt_auth.client_id
        serializer.save(client_id=client_id)


class KanaalViewSet(CheckQueryParamsMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    queryset = Kanaal.objects.all()
    serializer_class = KanaalSerializer
    filterset_class = KanaalFilter
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_NOTIFICATIES_PUBLICEREN | SCOPE_NOTIFICATIES_CONSUMEREN,
        'retrieve': SCOPE_NOTIFICATIES_PUBLICEREN | SCOPE_NOTIFICATIES_CONSUMEREN,
        'create': SCOPE_NOTIFICATIES_PUBLICEREN,
    }


class NotificatieAPIView(views.APIView):
    required_scopes = {
        'create': SCOPE_NOTIFICATIES_PUBLICEREN,
    }
    # Exposed action of the view used by the vng_api_common
    action = 'create'

    @swagger_auto_schema(request_body=MessageSerializer, responses={200: MessageSerializer})
    def create(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # post to message queue
            # send to abonnement
            serializer.save()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
