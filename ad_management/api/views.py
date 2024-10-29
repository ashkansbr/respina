from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from ad_management.api.selectors import get_all_ads, get_ad_by_id, get_comments_for_ad
from ad_management.api.services import create_ad, update_ad, delete_ad, create_comment
from ad_management.api.serializers import AdSerializer, CommentSerializer


@extend_schema_view(
    get=extend_schema(
        description="Retrieve a list of all ads, accessible to anyone.",
        responses={200: AdSerializer(many=True)}
    ),
    post=extend_schema(
        description="Create a new ad. Requires user authentication.",
        request=AdSerializer,
        responses={201: AdSerializer, 400: "Bad Request", 401: "Unauthorized"},
        auth=[{"Bearer": []}],
    )
)
class AdListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        ads = get_all_ads()
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            ad = create_ad(owner=request.user, data=serializer.validated_data)
            response_serializer = AdSerializer(ad)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        description="Retrieve an ad by its ID. Accessible to anyone.",
        responses={200: AdSerializer, 404: "Not Found"}
    ),
    put=extend_schema(
        description="Update an ad by its ID. Only the owner of the ad can perform this action.",
        request=AdSerializer,
        responses={200: AdSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
        auth=[{"Bearer": []}],
    ),
    delete=extend_schema(
        description="Delete an ad by its ID. Only the owner of the ad can perform this action.",
        responses={204: "No Content", 403: "Forbidden", 404: "Not Found"},
        auth=[{"Bearer": []}],
    ),
)
class AdRetrieveUpdateDeleteView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        ad = get_ad_by_id(pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        ad = get_ad_by_id(pk)
        if ad.owner != request.user:
            return Response(
                {"detail": "You do not have permission to edit this ad."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AdSerializer(ad, data=request.data, partial=True)
        if serializer.is_valid():
            updated_ad = update_ad(ad, serializer.validated_data, request.user)
            response_serializer = AdSerializer(updated_ad)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ad = get_ad_by_id(pk)
        if ad.owner != request.user:
            return Response(
                {"detail": "You do not have permission to delete this ad."},
                status=status.HTTP_403_FORBIDDEN
            )

        delete_ad(ad, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        description="Retrieve all comments for a specific ad. Accessible to anyone.",
        responses={200: CommentSerializer(many=True), 404: "Not Found"}
    ),
    post=extend_schema(
        description="Create a comment on a specific ad. Requires user authentication. Only one comment per user per ad is allowed.",
        request=CommentSerializer,
        responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden"},
        auth=[{"Bearer": []}],
    ),
)
class CommentListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        comments = get_comments_for_ad(pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        ad = get_ad_by_id(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                comment = create_comment(ad, request.user, serializer.validated_data['text'])
                response_serializer = CommentSerializer(comment)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except PermissionDenied as e:
                return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
