import pandas as pd
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from .models import Venta
from django.db.models import Sum




def get_all_sales_report():
    return [
        {
            "total": Venta.objects.filter(
                                fecha_creacion__gte=date_range['after'],
                                fecha_creacion__lte=date_range['before']
                            ).aggregate(total_ventas=Sum('total'))['total_ventas'] or 0,
            "desde": f"{date_range['after'].day}/{date_range['after'].month}/{date_range['after'].year}",
            "hasta": f"{date_range['before'].day}/{date_range['before'].month}/{date_range['before'].year}",
        } for date_range in get_last_12_months()
    ]

def get_client_all_sales_report(cliente):
    return [
        {
            "total": Venta.objects.filter(
                                fecha_creacion__gte=date_range['after'],
                                fecha_creacion__lte=date_range['before'],
                                cliente=cliente,
                            ).aggregate(total_ventas=Sum('total'))['total_ventas'] or 0,
            "desde": f"{date_range['after'].day}/{date_range['after'].month}/{date_range['after'].year}",
            "hasta": f"{date_range['before'].day}/{date_range['before'].month}/{date_range['before'].year}",
        } for date_range in get_client_all_months(cliente)
    ]

def get_client_last_year_sales_report(cliente):
    return [
        {
            "total": Venta.objects.filter(
                                fecha_creacion__gte=date_range['after'],
                                fecha_creacion__lte=date_range['before'],
                                cliente=cliente,
                            ).aggregate(total_ventas=Sum('total'))['total_ventas'] or 0,
            "desde": f"{date_range['after'].day}/{date_range['after'].month}/{date_range['after'].year}",
            "hasta": f"{date_range['before'].day}/{date_range['before'].month}/{date_range['before'].year}",
        } for date_range in get_last_12_months()
    ]

def get_client_last_month_sales_report(cliente):
    return [
        {
            "total": Venta.objects.filter(
                                fecha_creacion__year=str(past_date.year),
                                fecha_creacion__month=str(past_date.month),
                                fecha_creacion__day=str(past_date.day),
                                cliente=cliente,
                            ).aggregate(total_ventas=Sum('total'))['total_ventas'] or 0,
            "fecha": f"{past_date.day}/{past_date.month}/{past_date.year}",
        } for past_date in get_last_30_days()
    ]


def get_past_date_range(past_days):
    TODAY = datetime.datetime.utcnow()
    delta = datetime.timedelta(days=past_days)
    return {
        "after": TODAY - delta,
        "before": TODAY
    }

def get_last_12_months():
    TODAY = datetime.datetime.utcnow()
    MONTHS_AGO_YEAR = 12
    for i in range(MONTHS_AGO_YEAR):
        yield (get_month_range(TODAY.year, TODAY.month))
        TODAY += relativedelta(months = -1)

def get_client_all_months(cliente):
    TODAY = datetime.datetime.utcnow()
    MONTHS_AGO = diff_month(cliente.fecha_creacion, TODAY)
    for i in range(MONTHS_AGO):
        yield (get_month_range(TODAY.year, TODAY.month))
        TODAY += relativedelta(months = -1)

def get_last_30_days():
    return pd.date_range(end = datetime.datetime.today(), periods = 30).to_pydatetime().tolist()

def get_month_range(year, month):
    first_day = datetime.datetime(year, month, 1)
    last_day = first_day + datetime.timedelta(days=calendar.monthrange(year, month)[1] - 1)
    return {
        "after": first_day,
        "before": last_day,
    }

def diff_month(d1, d2):
    diff = (d1.year - d2.year) * 12 + d1.month - d2.month
    if (diff > 2):
        return diff
    return 2