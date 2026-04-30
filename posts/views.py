# Create your views here.
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import Post
from .serializers import PostSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def api_post_list(request):
    """
    Return all posts.
    """
    posts = Post.objects.select_related('author').all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_post(request):
    """
    Create a new post.
    """
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_post_detail(request, pk):
    """
    Retrieve, update, or delete a post.
    """
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == 'PUT':
        if post.author != request.user:
            return Response(
                {'error': 'You do not have permission to edit this post.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if post.author != request.user:
        return Response(
            {'error': 'You do not have permission to delete this post.'},
            status=status.HTTP_403_FORBIDDEN
        )

    post.delete()
    return Response(
        {'message': 'Post deleted successfully.'},
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    Authenticate user and return token.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(
        username=username,
        password=password
    )

    if not user:
        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'username': user.username,
    })