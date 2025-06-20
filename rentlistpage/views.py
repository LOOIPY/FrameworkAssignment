<<<<<<< HEAD
from django.shortcuts import render

def rent_list(request):

    return render(request, 'rent_list.html', )
=======
# rentlistpage/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from proplistpage.models import Property  # Import from proplistpage app


def rent_list(request):
    # Filter properties where type is "rent" (lowercase, as shown in debug)
    properties = Property.objects.filter(type="rent")

    # Get filter parameters from request
    selected_location = request.GET.get('location')
    selected_price_order = request.GET.get('price_order')
    selected_search = request.GET.get('search', '')

    # Apply location filter
    if selected_location:
        properties = properties.filter(location=selected_location)

    # Apply search filter
    if selected_search:
        properties = properties.filter(
            Q(title__icontains=selected_search) |
            Q(location__icontains=selected_search) |
            Q(price__icontains=selected_search)
        )

    # Apply price ordering
    if selected_price_order == 'asc':
        properties = properties.order_by('price')
    elif selected_price_order == 'desc':
        properties = properties.order_by('-price')
    else:
        properties = properties.order_by('-id')  # Default ordering

    # Pagination
    paginator = Paginator(properties, 6)  # Show 6 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get recommended properties (random selection of rent properties)
    recommended = Property.objects.filter(type="rent").exclude(
        id__in=[p.id for p in page_obj]
    ).order_by('?')[:4]  # Get 4 random recommendations

    context = {
        'properties': page_obj,
        'page_obj': page_obj,
        'selected_location': selected_location,
        'selected_price_order': selected_price_order,
        'selected_search': selected_search,
        'recommended': recommended,
    }

    return render(request, 'rent_list.html', context)


def rent_detail(request, property_id):
    # Get specific rent property (using "rent" instead of "For Rent")
    property_obj = get_object_or_404(Property, id=property_id, type="rent")

    context = {
        'property': property_obj,
    }

    return render(request, 'rent_detail.html', context)
>>>>>>> Pei-Yi
