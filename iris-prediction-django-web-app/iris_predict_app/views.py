from django.shortcuts import render
from django.http import JsonResponse
from .models import PredResults
import os
from reimaginedparakeet.model.train import load_pickle, train

def predict(request):
    """Show the form to predict."""
    return render(request, "predict.html")

def train_model(request):
    """Make a prediction using the input features from the user."""
    if request.POST.get('action') == 'post':
        # Receive data from client
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))

        current_path = os.path.dirname(__file__)
        pickle_file_name = os.path.join(current_path, '../', 'ml_models', 'new_model.pickle')
        retcode = train(start_year, end_year, pickle_file_name)

        return JsonResponse({'result': retcode}, safe=False)

def train_page(request):
    return render(request, "train.html")

def predict_chances(request):
    """Make a prediction using the input features from the user."""
    if request.POST.get('action') == 'post':

        # Receive data from client
        previous_day_pool_price = float(request.POST.get('previous_day_pool_price'))
        mean_temp = float(request.POST.get('mean_temp'))
        rolling_30day_avg = float(request.POST.get('rolling_30day_avg'))
        alberta_internal_load = float(request.POST.get('alberta_internal_load'))
        ng_price = float(request.POST.get('ng_price'))
        spd_of_max_gust = float(request.POST.get('spd_of_max_gust'))
        day_of_year = float(request.POST.get('day_of_year'))
        total_precip = float(request.POST.get('total_precip'))
        is_public_holiday = float(request.POST.get('is_public_holiday'))

        # get the file path
        current_path = os.path.dirname(__file__)
        pickle_file_name = os.path.join(current_path, '../', 'ml_models', 'new_model.pickle')

        # Unpickle model
        model = load_pickle(pickle_file_name)
        # Make prediction
        result = model.get_model_predictions([[day_of_year, mean_temp, spd_of_max_gust, total_precip,
                                               alberta_internal_load, rolling_30day_avg, previous_day_pool_price,
                                               is_public_holiday, ng_price]])

        pool_price = result[0]

        PredResults.objects.create(previous_day_pool_price=previous_day_pool_price, mean_temp=mean_temp,
                                   rolling_30day_avg=rolling_30day_avg, alberta_internal_load=alberta_internal_load,
                                   ng_price=ng_price, spd_of_max_gust=spd_of_max_gust, day_of_year=day_of_year,
                                   total_precip=total_precip, is_public_holiday=is_public_holiday,
                                   pool_price=pool_price)

        return JsonResponse({'result': pool_price, 'day_of_year': day_of_year, 'mean_temp': mean_temp,
                             'spd_of_max_gust': spd_of_max_gust, 'total_precip': total_precip,
                             'alberta_internal_load': alberta_internal_load, 'rolling_30day_avg': rolling_30day_avg,
                             'previous_day_pool_price': previous_day_pool_price, 'is_public_holiday': is_public_holiday,
                             'ng_price': ng_price}, safe=False)


def view_results(request):
    """Submit prediction and show all results."""
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)
