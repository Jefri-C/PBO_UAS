from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from products.serializers import ProductSerializer
from pbo_uas.models import Product
from pbo_uas.response import ok_with_msg, ok_with_data, error_with_msg


@api_view(['GET'])
def getProduct(request):
    name = request.query_params.get('name', None)
    category_id = request.query_params.get('category_id', None)

    # get all the data from db
    products = Product.objects.all()

    # filter
    if name:
        products = products.filter(name__icontains=name)
    if category_id:
        products = products.filter(category_id=category_id)


    # serialize and return it
    serializer = ProductSerializer(products, many=True)
    return ok_with_data(data=serializer.data, msg='ok')


@api_view(['POST'])
def addProduct(request):
    # get the data
    serializer = ProductSerializer(data=request.data)

    # check is the requested data valid
    if serializer.is_valid():
        serializer.save()
        return ok_with_msg(msg='product created successfully!')
    else:
        return error_with_msg(msg=serializer.errors)


@api_view(['POST'])
def updateProduct(request):
    # get id
    product_id = request.data.get('id')
    if not product_id:
        return error_with_msg(msg='id is required!')

    # check the data is exist
    product = get_object_or_404(Product, pk=product_id)

    # get the data
    serializer = ProductSerializer(product, data=request.data, partial=True if request.method == 'PATCH' else False)

    # check is the requested data valid
    if serializer.is_valid():
        serializer.save()
        return ok_with_msg(msg='product updated successfully!')
    else:
        return error_with_msg(msg=serializer.errors)


@api_view(['DELETE'])
def deleteProduct(request):
    # get id
    product_id = request.data.get('id')
    if not product_id:
        return error_with_msg(msg='id is required!')

    # check if the product exists
    product = get_object_or_404(Product, pk=product_id)

    # delete the product
    product.delete()

    return ok_with_msg(msg='product deleted successfully!')
