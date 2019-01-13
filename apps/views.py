from django.shortcuts import render
from django.template.loader import get_template
# Create your views here.
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse
from django.conf import settings


# def map_app():
#     if request.method == 'POST':

#     if not check_name_in_list(request.POST['s_name']):
#         NAME_ERROR = True
#         insert_file = 'Name_table.html'
#         table_data = pack_table_data()
#     else:
#         species_name = request.POST['s_name']
#         map_type = request.POST['t_select']
#         if map_type == 'marker only':
#             create_simple_map(species_name)
#             insert_file = species_name+'.html'
#         elif map_type == 'marker with popup':
#             create_popup_map(species_name)
#             insert_file = species_name+'_popup.html'
#             guide_text = "<p style='color: #1561a0'>點選標記即可看到更多資訊</p>"
#         elif map_type == 'heatmap':
#             create_heatmap(species_name)
#             insert_file = species_name+'_heatmap.html'
#             guide_text = "<p style='color: #1561a0'>Kernel estimation for dense region 點位越多顏色越深</p>"
#         elif map_type == 'animation by year':
#             create_year_animation(species_name)
#             insert_file = species_name+'_anim_year.html'
#             guide_text = "<p style='color: #1561a0'> 就先用heatmap with time吧，也是有一般的with time，但來不及研究</p>"
#         else:
#             guide_text = "<h3 style='color: #ff61a0'>建構中!!，快做完才發現資料及沒月份的，懶得做了</h3>"
#             table_data = pack_table_data()
#             insert_file = 'Name_table.html'
#             # create_month_animation(species_name)
#             # insert_file = species_name+'_anim_month.html'
#     else:
#         table_data = pack_table_data()
#         insert_file = 'Name_table.html'

#     return HttpResponse(render(request, '../templates/base.html', locals()))

# def test(request):
#     return HttpResponse(render(request, '../templates/NO.html', locals()))


'''
test django paypal
'''
'''
def pay_process(request):

    # host = request.get_host()
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10000000.00",
        'currency_code': 'NTD',
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('my_return_view')),
        "cancel_return": request.build_absolute_uri(reverse('my_cancel_view')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "apps/payment.html", context)

def my_return_view(request):
    return HttpResponse('<h1>This is my return view</h1>')

def my_cancel_view(request):
    return HttpResponse('<h1>This is my cancel view</h1>')
'''