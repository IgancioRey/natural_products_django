from datetime import timedelta
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from customers.models import Customer
from orders.forms import OrderForm
from orders.models import Order


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
    # customer = get_object_or_404(Customer, pk=order.customer)
    # order.customer = customer
    return render(request, 'orders/order_detail.html', {'order': order})
