from django.conf import settings

class referralCatcher:
    def process_request(self, request):
        if 'HTTP_REFERER' in request.META:
            referral_site = request.META['HTTP_REFERER']
            base_site = 'http://cbio-test.cs.brown.edu'
            if referral_site.startswith(base_site):
                request.referral_site = base_site
            else:
                request.referral_site = None
        else:
            request.referral_site = None
        return 

    def process_template_response(self, request, response):
        response.context_data['referral_site'] = request.referral_site
        return response

