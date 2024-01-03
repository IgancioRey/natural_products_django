import csv
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, ProductFormEdit
from .models import Product
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize



def import_product_csv():
    default_products = []
    file_path = 'products\products.csv'
    # Product.objects.all().delete()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Ignora la primera fila si contiene encabezados
        next(csv_reader, None)

        for row in csv_reader:
            default_products.append(
                {
                    "name": row[1],
                    "count": 0,
                    "price": row[3],
                    "sellingPrice": row[4]
                }
            )
        
        for product_data in default_products:
            try:
                product_form = ProductForm(product_data)        
                if product_form.is_valid():
                    product_form.save()
                else:
                    print(f"Error al crear el producto {product_data['name']}")
            except Exception as e:
                print(f"Error al crear el producto {product_data['name']}")
        

def products_list(request):    
    
    productList = Product.objects.order_by('name')

    if not productList:
        print("No hay productos. Creando productos por defecto.")
        import_product_csv()
        productList = Product.objects.order_by('name')

    success_message_count = len(messages.get_messages(request))

    return render(
        request,
        'products/product_list.html',
        {'products': productList}
    )
    
def product_list_json(request):
    productList = Product.objects.order_by('name')
    data = [product.get_data() for product in productList]
    response = {'data': data}
    
    return JsonResponse(response)
    


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
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return render(request, 'products/product_detail.html', {'product': product})
        else:
                messages.error(request, 'No se pudo actualizar el producto.', extra_tags='danger')
    else:
        form = ProductFormEdit(instance=product)

    return render(request, 'products/product_edit.html', {'form': form})

@csrf_exempt
def product_edit_modal(request):
    if request.method == 'POST':
        id = int(request.POST['idProduct'])
        product = get_object_or_404(Product, pk=id)

        product.name = request.POST['name']
        product.count = int(request.POST['count'])
        product.price = float(request.POST['price'])
        product.sellingPrice = float(request.POST['sellingPrice'])

        form = ProductFormEdit(request.POST, instance=product)

        if form.is_valid():
            updated_product = form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return JsonResponse({'success': True})
        else:
            errors = dict(form.errors.items())
            messages.error(request, 'No se pudo actualizar el producto.', extra_tags='danger')
            return JsonResponse({'success': False, 'errors': errors})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    product.delete()

    return redirect('products_list')
