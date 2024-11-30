from django.core import paginator
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.views.decorators.csrf import csrf_exempt

from api.models import *
from api.serializers import ProductSerializer

# get all product with querry
@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword', '')  # Default to an empty string if keyword is None
    products = Product.objects.filter(name__icontains=query).order_by('-_id')

    # Handle pagination
    page = request.query_params.get('page', '1')  # Default to page 1 if not provided
    paginator = Paginator(products, 8)
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Convert page to an integer safely
    try:
        page = int(page) if page.isdigit() else 1
    except ValueError:
        page = 1

    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

# Top Products
@api_view(['GET'])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# get isnglee product
@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def createProductReview(request, pk):
    print(request.headers)  # Logs to check headers
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data
    # Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # No rating or 0 rating
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)
        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total / len(reviews)
        product.save()
        return Response('Review Added')


