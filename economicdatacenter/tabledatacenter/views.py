from django.shortcuts import render
from django.db.models import Max
from tabledatacenter.models import DataCountryByEconomic
from django.http import JsonResponse
from django.db.models import F

def home(request):
    # Get the latest date for each 'name' and 'country'
    latest_entries = (DataCountryByEconomic.objects
                      .values('name', 'country')  # Get unique name-country pairs
                      .annotate(latest_date=Max('date')))  # Annotate with the latest date for each pair

    # Prepare the filtered data based on the latest entries
    data_to_insert = []
    for entry in latest_entries:
        # Get the row with the latest date for this name and country combination
        latest_row = (DataCountryByEconomic.objects
                      .filter(name=entry['name'], country=entry['country'], date=entry['latest_date'])
                      .first())  # Get the first result (since we expect only one)

        if latest_row:
            # Append the filtered row to the data_to_insert list
            data_to_insert.append(latest_row)

    context = {
        'data': data_to_insert
    }

    return render(request, 'home.html', context)

def fetch_data(request):
    name = request.GET.get('name')
    country = request.GET.get('country')

    # Query to get all data for the selected name and country, ordered by date
    data_entries = (DataCountryByEconomic.objects
                    .filter(name=name, country=country)
                    .order_by('date')
                    .values('date', 'data', 'unit'))

    # Extract dates, data points (rounded to 2 decimal places), and unit
    dates = [entry['date'].strftime('%d-%b-%Y') for entry in data_entries]
    data_points = [round(entry['data'], 2) for entry in data_entries]
    unit = data_entries[0]['unit'] if data_entries else ''

    # Return JSON response with dates, data points, and unit
    return JsonResponse({'dates': dates, 'data': data_points, 'unit': unit})
