import csv
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from customers.forms import CustomerForm
from customers.models import Customer


# Create your views here.
def import_customers_csv():
    default_customers = []
    file_path = 'customers\customers.csv'
    # Customer.objects.all().delete()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Ignora la primera fila si contiene encabezados
        next(csv_reader, None)

        for row in csv_reader:
            default_customers.append(
                {
                    "firstName": row[1],
                    "lastName": row[2],
                    "mobileNumber": row[3],
                    "observation": row[4]
                }
            )

        for customer_data in default_customers:
            try:
                customer_form = CustomerForm(customer_data)
                if customer_form.is_valid():
                    customer_form.save()
                else:
                    print(f"Error al crear el cliente {customer_data['firstName']} : {customer_form.errors}")
            except Exception as e:
                print(f"Error al crear el cliente {customer_data['firstName']}")


def customers_list(request):
    customerList = Customer.objects.all().order_by('firstName', 'lastName')

    if not customerList:
        print("No hay clientes. Creando clientes por defecto.")
        import_customers_csv()
        customerList = Customer.objects.all().order_by('firstName', 'lastName')

    return render(
        request,
        'customers/customer_list.html',
        {'customers': customerList}
    )


def customer_list_json(request):
    customerList = Customer.objects.all().order_by('firstName', 'lastName')
    data = [customer.get_data() for customer in customerList]
    response = {'data': data}

    return JsonResponse(response)


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    customer.delete()

    return redirect('customer_list')


@csrf_exempt
def customer_new(request):
    try:
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('customer_detail', pk=form.instance.pk)
        else:
            form = CustomerForm()

        return render(request, 'customers/customer_create.html', {'form': form})

    except Exception as e:
        print("Error:", str(e))
        return HttpResponseServerError("Ocurrió un error al intentar crear el cliente.")


@csrf_exempt
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            form.save()
            return render(request, 'customers/customer_detail.html', {'customer': customer})
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_edit.html', {'form': form})
