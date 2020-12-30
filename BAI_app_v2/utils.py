from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


account_activation_token=AccountActivationTokenGenerator()

# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
#
# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None