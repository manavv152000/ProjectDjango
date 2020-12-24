from django.shortcuts import render,redirect
from BAI_app_v2.forms import ParticipantInfoForm,SignUpForm,SpeedForm,SafetynWellfareForm,OthersForm,EconomyForm,Project_infoForm,QualityForm,CategoryForm,PaymentDetailsForm

from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .utils import account_activation_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from verify_email.email_handler import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
UserModel = get_user_model()
# Create your views here.

def home(request):
    return render(request,'BAI_app_v2/index.html')

@login_required
def participant_logout(request):
    logout(request)
    return render(request,'BAI_app_v2/login.html')


def signup(request):
    
    registered = False

    if request.method == 'POST':
        signup_form = SignUpForm(data=request.POST)
        participant_form = ParticipantInfoForm(data=request.POST)

        if signup_form.is_valid() and participant_form.is_valid():
            user = signup_form.save()
            user.set_password(user.password)
            user.save()

            profile = participant_form.save(commit=False)
            profile.user = user
            profile.save()

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('BAI_app_v2/active_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': default_token_generator.make_token(user),
                                       }
                                       )
            email_subject = 'activate your account'

            to_email = user.email
            email = EmailMessage(
                email_subject,
                message,
                to=[to_email]
            )
            email.send(fail_silently=True)

            registered = True
            messages.add_message(request, 40, 'Signup Successful!\nHead on to Logging In to fill the Application Form')
            return render(request, 'BAI_app_v2/signup.html', {'registered': registered})
        
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(signup_form.errors.values())])
            return render(request, 'BAI_app_v2/signup.html',
                          {'signup_form': signup_form,
                           'participant_form': participant_form,
                           'registered': registered,
                           'error': error_string})

    else:
        return render(request, 'BAI_app_v2/signup.html', {'registered': registered})



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user123 = authenticate(request,username=username,password=password)

        if user123 is not None:
            if user123.is_active:
                login(request,user123)
                return render(request,'BAI_app_v2/user_landing.html',{'user123':user123})

            else:
                return HttpResponse("Account not Active!")

        else:
            messages.add_message(request, 40, 'Invalid Login credentials')
            return redirect('/BAI_app_v2/user_login/')
    else:
        return render(request,'BAI_app_v2/login.html',{})

@login_required(login_url='/BAI_app_v2/user_login/')
def user_landing(request):
    return render(request,'BAI_app_v2/user_landing.html')

@login_required(login_url='/BAI_app_v2/user_login/')
def user_profile(request):
    return render(request,'BAI_app_v2/user_profile.html')


@login_required(login_url='/BAI_app_v2/user_login/')
def form0(request):

    filled0 = False
    if request.method == 'POST':

        category_cat = CategoryForm(data=request.POST)
        if category_cat.is_valid():
            category_cat1 = category_cat.save()
            category_cat1.users_name = request.user.username
            category_cat1.save()

            filled0 = True

        else:
            print("Chuklay ikde!")
            print(category_cat)
            print(category_cat.errors)

    else:
        category_cat = CategoryForm()
        
    messages.info(request, 'Category selected successfully!!')
    return render(request,'BAI_app_v2/form0.html',{'category_cat':category_cat,'filled0':filled0})


@login_required(login_url='/BAI_app_v2/user_login/')
def form1(request):

    filled = False
    if request.method == 'POST':

        speed_cat = SpeedForm(data=request.POST)
        project_info_cat = Project_infoForm(request.POST,request.FILES)
        quality_cat = QualityForm(request.POST,request.FILES)
        
        if speed_cat.is_valid() and project_info_cat.is_valid() and quality_cat.is_valid():
            speed_cat1 = speed_cat.save()

            speed_cat1.users_name = request.user.username
            speed_cat1.save()

            project_info_cat1 = project_info_cat.save(commit=False)
            quality_cat1 = quality_cat.save(commit=False)   

            if 'req_docs' in request.FILES:
                project_info_cat1.req_docs = request.FILES['req_docs']  
            if 'site_map' in request.FILES:
                project_info_cat1.site_map = request.FILES['site_map'] 
            if 'green_project_details' in request.FILES:
                project_info_cat1.green_project_details = request.FILES['green_project_details']  

            if 'meeting_instruction_book_minute' in request.FILES:
                quality_cat1.meeting_instruction_book_minute = request.FILES['meeting_instruction_book_minute']
            if 'sample_Checklist_followed' in request.FILES:
                quality_cat1.sample_Checklist_followed = request.FILES['sample_Checklist_followed']
            if 'sample_test_reports' in request.FILES:
                quality_cat1.sample_test_reports = request.FILES['sample_test_reports']

            project_info_cat1.users_name = request.user.username
            quality_cat1.users_name = request.user.username

            project_info_cat1.save()
            quality_cat1.save()

            filled = True


        else:
            print("Chuklay ikde!")
            print(speed_cat.errors,project_info_cat.errors,quality_cat.errors)

    else:
        speed_cat = SpeedForm()
        project_info_cat = Project_infoForm()
        quality_cat = QualityForm()

    messages.info(request, 'Form 1 Submitted successfully!!')  
    return render(request,'BAI_app_v2/form1.html',{'speed_cat':speed_cat,
                                                    'project_info_cat':project_info_cat,
                                                    'quality_cat':quality_cat,'filled':filled})

@login_required(login_url='/BAI_app_v2/user_login/')
def form2(request):
    filled2 = False
    if request.method == 'POST':

        safety_cat = SafetynWellfareForm(request.POST,request.FILES)
        others_cat = OthersForm(request.POST,request.FILES)
        economy_cat = EconomyForm(request.POST)

        if safety_cat.is_valid() and others_cat.is_valid() and economy_cat.is_valid():
            economy_cat1 = economy_cat.save()
            safety_cat1 = safety_cat.save(commit=False)
            others_cat1 = others_cat.save(commit=False)

            economy_cat1.users_name = request.user.username
            economy_cat1.save()

            if 'safety_audits' in request.FILES:
                safety_cat1.safety_audits = request.FILES['safety_audits']

            safety_cat1.users_name=request.user.username

            safety_cat1.save()

            others_cat1.accomodation = request.FILES['accomodation']
            others_cat1.sanitary = request.FILES['sanitary']
            others_cat1.polution_measures = request.FILES['polution_measures']

            if 'school' in request.FILES:
                others_cat1.school = request.FILES['school']

            if 'renewable_energy_pic' in request.FILES:
                others_cat1.renewable_energy_pic = request.FILES['renewable_energy_pic']            

            others_cat1.users_name=request.user.username
            others_cat1.save()

            filled2 = True

        else:
            print("Chuklay ikde!1")
            print(safety_cat.errors)
            print(others_cat.errors)
            print(economy_cat.errors)
            

    else:
        safety_cat = SafetynWellfareForm()
        others_cat = OthersForm()
        economy_cat = EconomyForm()

    messages.info(request, 'Form 2 submitted successfully!!')    
    return render(request,'BAI_app_v2/form2.html',{'safety_cat':safety_cat,
                                                    'others_cat':others_cat,
                                                    'economy_cat':economy_cat,'filled2':filled2})


@login_required(login_url='/BAI_app_v2/user_login/')
def form3(request):

    filled3 = False
    if request.method == 'POST':

        payment_cat = PaymentDetailsForm(data=request.POST)
        if payment_cat.is_valid():
            payment_cat1 = payment_cat.save()
            payment_cat1.users_name = request.user.username
            payment_cat1.save()

            filled3 = True

        else:
            print("Chuklay ikde!")
            print(payment_cat.errors)

    else:
        payment_cat = PaymentDetailsForm()
        
    messages.info(request, 'Payment Details filled successfully!!')
    messages.info(request, 'Application From filled sussessfully!!')
    return render(request,'BAI_app_v2/form3.html',{'payment_cat':payment_cat,'filled3':filled3})


@login_required(login_url='/BAI_app_v2/user_login/')
def change_pass(request):

    if request.method == 'POST':
        changePass = PasswordChangeForm(user=request.user,data=request.POST)
        if changePass.is_valid():
            changePass.save()
            # print(changePass)
            #update_session_auth_hash(request,changePass.user)
            return HttpResponse("Password Changed Successfully")

        # else:
        #     #print("old:{} new1:{} new2:{}".format(old_password,new_password1,new_password2))
        #     print(changePass)
        #     return HttpResponse("Request for Change Password Failed!")

    else:
        changePass = PasswordChangeForm(user=request.user)
    return render(request,'BAI_app_v2/changePassword.html',{'changePass':changePass})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



