import logging

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from hubspot import HubSpot
from hubspot.auth.oauth import ApiException as OauthException
from hubspot.crm.objects import ApiException

from apps.core.models import Deal, HubToken
from apps.core.utils import datatable_page

logger = logging.getLogger(__name__)


class HubTokenAPIView(View):
    model = HubToken

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            api_client = HubSpot()
            data = self.request.POST
            result = api_client.auth.oauth.default_api.create_token(
                grant_type=data.get('grant_type'),
                redirect_uri=data.get('redirect_uri'),
                client_id=data.get('client_id'),
                client_secret=data.get('client_secret'),
                code=data.get('code')
            )
            self.model.objects.create(
                access_token=result.access_token,
                refresh_token=result.refresh_token,
                expires_in=result.expires_in,
            )
            return JsonResponse(result.to_dict())

        except OauthException as e:
            raise OauthException("Exception when calling create_token method: %s\n" % e)


class DealListAPIView(View):

    def get_data_deals(self, token):
        api_client = HubSpot()
        api_client.access_token = token
        try:
            all_deals = api_client.crm.deals.get_all()
            for result in all_deals:
                deal, created = Deal.objects.get_or_create(deal_id=result.id)
                properties = result.properties
                if properties:
                    deal.deal_name = properties.get('dealname')
                    deal.deal_stage = properties.get('dealstage')
                    deal.close_date = properties.get('closedate')
                    deal.amount = properties.get('amount')
                    deal.deal_type = properties.get('pipeline')
                    deal.save()
        except ApiException as e:
            print("Exception when requesting custom objects: %s\n" % e)

    def get(self, request, *args, **kwargs):
        parameter_search = self.request.GET.get('parameter_search', '').strip()
        token = self.request.GET.get('token', '')
        deals = Deal.objects.all()
        if token:
            self.get_data_deals(token)
        if parameter_search:
            if parameter_search.isdigit():
                deals = deals.filter(deal_id__exact=parameter_search)
            else:
                deals = (
                        deals.filter(deal_name__icontains=parameter_search) |
                        deals.filter(deal_stage__icontains=parameter_search) |
                        deals.filter(deal_type__icontains=parameter_search)
                )

        deals = deals.order_by('-id')
        draw, page = datatable_page(deals, request)
        tabla = []
        for deal in page.object_list:
            close_date = ''
            if deal.close_date:
                close_date = deal.close_date.strftime('%m-%d-%Y - %I:%M %p')
            tabla.append(
                [deal.deal_id,
                 deal.deal_name or '',
                 deal.deal_stage or '',
                 close_date,
                 deal.amount or '',
                 deal.deal_type or '']
            )
        data = {
            "draw": draw,
            "recordsTotal": deals.count(),
            "recordsFiltered": deals.count(),
            "data": tabla
        }
        json = JsonResponse(data)
        return json
