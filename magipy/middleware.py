from django.conf import settings

class referralCatcher:
    def process_request(self, request):
        # look at the referring website;
        # if a user clicks on a link from one website/domain to another,
        # this field "HTTP_REFERER" in the HTTP header will be filled out
        if 'HTTP_REFERER' in request.META:
            referral_site = request.META['HTTP_REFERER']

            # check to see if cbio-test refered us
            base_site = 'http://cbio-test.cs.brown.edu'
            if referral_site.startswith(base_site):
                request.referral_site = base_site
            else:
                request.referral_site = None
        else:
            request.referral_site = None
        return

    # todo: pass along the referral_site in requests/use a session-cookie to store referring data
    def process_template_response(self, request, response):
        # tell the view to render links with the referrer in mind        
        response.context_data['referral_site'] = request.referral_site
        return response

