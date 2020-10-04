from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
import datetime
from django.views import View
from .models import Purchase


class BarChart(View):
    def get(self, request, *args, **kwargs):
        context_data = {
            'frequency': [0] * 12
        }
        return render(request, "charts/base.html", context_data)

    def post(self, request, *args, **kwargs):
        date_string = request.POST.get('start_date', None)
        start_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        end_date = start_date + datetime.timedelta(days=365)
        dispatched_purchases = Purchase.objects.filter(
            purchasestatus__status='dispatched', purchasestatus__created_at__gte=start_date,
            purchasestatus__created_at__lt=end_date)
        if dispatched_purchases:
            dispatched_purchases = dispatched_purchases.annotate(
                month=ExtractMonth('purchasestatus__created_at')).values('month').annotate(count=Count('id')).values(
                'month', 'count').order_by('month')
        delivered_and_non_dispatched = Purchase.objects.filter(
            purchasestatus__status='delivered', purchasestatus__created_at__gte=start_date,
            purchasestatus__created_at__lt=end_date).exclude(purchasestatus__status='dispatched')
        if delivered_and_non_dispatched:
            delivered_and_non_dispatched = delivered_and_non_dispatched.annotate(
                month=ExtractMonth('purchasestatus__created_at')).values('month').annotate(count=Count('id')).values(
                'month', 'count').order_by('month')

        frequency_in_month = [0] * 12
        for freq_dict in dispatched_purchases:
            frequency_in_month[freq_dict['month'] - 1] += freq_dict['count']
        for freq_dict in delivered_and_non_dispatched:
            frequency_in_month[freq_dict['month'] - 1] += freq_dict['count']
        context = {
            'frequency': frequency_in_month
        }
        return render(request, "charts/base.html", context=context)
