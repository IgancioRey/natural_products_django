from datetime import timedelta
from decimal import Decimal
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views.decorators.http import require_POST

from customers.models import Customer
from orders.forms import OrderForm
from orders.models import Order, OrderDetail
from products.models import Product


# Create your views here.
@csrf_exempt
def order_new(request):
    customers = Customer.objects.all()
    try:
        if request.method == "POST":
            customer_id = request.POST.get('customer')            
            date = timezone.now().date() - timedelta(days=20)
            order = Order.objects.filter(customer = customer_id, orderDate__gte=date)            
            
            if order.count() > 0:
                return redirect('order_detail', pk=order.first().pk)
            
            form = OrderForm(request.POST)
            if form.is_valid():
                customer = get_object_or_404(Customer, pk = customer_id)
                order_instance = form.save(commit=False)
                order_instance.customer = customer
                order_instance.save()
                return redirect('order_detail', pk=order_instance.pk)
            else:
                print(form.errors)
        else:

            form = OrderForm()

        return render(request, 'orders/order_create.html', {'form': form, 'customers': customers})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponseServerError(f"Ocurrió un error al intentar crear el pedido: {str(e)}")


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_details = OrderDetail.objects.filter(order=order)

    total = sum(detail.subTotal for detail in order_details)
    
    return render(request, 'orders/order_detail.html', {'order': order, 
                                                        'orderDetail': order_details, 
                                                        'total': total})

@csrf_exempt
def order_details_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_details = OrderDetail.objects.filter(order=order)

    total = sum(Decimal(str(detail.amount)) * Decimal(detail.count) for detail in order_details)

    productList = Product.objects.order_by('name')
    quantities = range(1, 11)
    
    return render(request, 'order_details/order_details_edit.html', {'order': order, 
                                                        'orderDetail': order_details, 
                                                        'total': total,
                                                        'products': productList,
                                                        'quantities': quantities})

@csrf_exempt  # Solo para pruebas. Elimina esto en producción.
def add_order_detail(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')
            product_id = request.POST.get('product')
            quantity = int(request.POST.get('quantity'))
            print(request.POST)

            order = get_object_or_404(Order, pk = order_id)
            
            product = get_object_or_404(Product, pk = product_id)
            selling_price = Decimal(str(product.sellingPrice))
            sub_total = selling_price * Decimal(quantity)
            sub_total = sub_total.quantize(Decimal('0.00'))

            order_detail = OrderDetail.objects.create(
                order=order,
                product=product,
                count=quantity,
                amount=sub_total
            )

            response = {
                'product': product.name,
                'count': quantity,
                'price': str(product.sellingPrice),
                'amount': str(sub_total)
            }
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)