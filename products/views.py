from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, ProductFormEdit
from .models import Product
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def products_list(request):
    productList = Product.objects.order_by(
        'name'
    )
    success_message_count = len(messages.get_messages(request))

    return render(
        request,
        'products/product_list.html',
        {'products': productList}
    )


def product_new(request):
    try:
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto creado correctamente.')
                return redirect('product_detail', pk=form.instance.pk)
            else:
                messages.error(request, 'No se pudo crear el producto.', extra_tags='danger')
        else:
            form = ProductForm()

        return render(request, 'products/product_create.html', {'form': form})
    
    except Exception as e:
        print("Error:", str(e))
        return HttpResponseServerError("Ocurrió un error al procesar la solicitud.")


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductFormEdit(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.lastModifiedDate = timezone.now()
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('products_list')
        else:
                messages.error(request, 'No se pudo actualizar el producto.', extra_tags='danger')
    else:
        form = ProductFormEdit(instance=product)

    return render(request, 'products/product_edit.html', {'form': form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    product.delete()

    return redirect('products_list')
