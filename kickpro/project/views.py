from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from pprint import pprint
from django.db.models import Q

from .models import *
from .forms import *
from django.http import HttpResponse
# from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.forms import modelformset_factory
from django.forms import inlineformset_factory

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext


###### Sha'lan Edit ####

########Registration with Confirmation#######
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            # profile = profile_form.save(commit=False)
            # user.is_active = False
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            # registered = True
            #######CONFIRMATION##########
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            mail_subject = 'Activate your KickPro account.'
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            ######################################
            ######################################
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


##########################################
##########################################
######Activation Function#################
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist()):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # profile.save()
        # registered = True
        login(request, user)

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return redirect('home')
    else:
        return HttpResponse('Activation link is invalid or Expired!')


def index(request):
    return render(request,'index.html')
@login_required(login_url='/#login')
def special(request):
    return HttpResponse("You are logged in !")
@login_required(login_url='/#login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'profile_pic' in request.FILES:
#                 print('found it')
#                 profile.profile_pic = request.FILES['profile_pic']
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors,profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileInfoForm()
#     return render(request,'registration.html',
#                           {'user_form':user_form,
#                            'profile_form':profile_form,
#                            'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})

###### Hossam Edit #####


def search(request):
    searchText = request.POST['searchText']
    print(searchText)
    Projects = Project.objects.filter(title__icontains =searchText)

    context = {'projects':Projects,'word':searchText}
    return render(request,'search.html',context)



def home(request):

    PopularProjects = Project.objects.order_by('current').reverse()[:4]
    Top5 = Project.objects.order_by('current').reverse()[:5]
    featuredProjects = Project.objects.filter(featured_project =1)
    Cats = Category.objects.all()
    context = {'popular':PopularProjects,'featured':featuredProjects,'cats':Cats,'top':Top5}
    return render(request,'home.html',context)

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#
#         if form.is_valid():
#
#             form.save()
#             return HttpResponse('Done')
#         else:
#             return HttpResponse('Validation Error !')
#
#     else:
#         form = RegisterForm()
#         return render(request,'register.html',{'form':form})

#User Add Project Form
@login_required(login_url='/#login')
def newProject(request):
    ImageFormSet = modelformset_factory(Project_Images, fields=('project_img',), extra=2)

    if request.method == 'POST':
        PostRequest = request.POST.copy()
        print('testing ####')
        print(request.session['_auth_user_id'])
        PostRequest['user'] = request.session['_auth_user_id']
        form = CreateProjectForm(PostRequest)
        formset = ImageFormSet(PostRequest, request.FILES)

        print(PostRequest)
        if form.is_valid() and formset.is_valid():
            post_form = form.save(commit=False)
            post_form.user = request.user.userprofileinfo
            if 'main_pic' in request.FILES:
                print('found it')
                post_form.main_pic = request.FILES['main_pic']
            post_form.save()
            form.save_m2m()
            #####JO
            for pic in formset:
                try:
                    picture = Project_Images(project_img=pic.cleaned_data['project_img'], project= post_form)
                    picture.save()
                except Exception as e:
                    break


            

            return HttpResponse('Project Created')
        else:
            return render(request, 'new_project.html', {'form': form, 'form_errors': form.errors})
            # print(form.errors)
            # return HttpResponse('Validation Failed!')
    else:
        form = CreateProjectForm()
        formset = ImageFormSet(queryset=Project_Images.objects.none())
        # return render(request,'new_project.html',{'form':form})
        return render(request, 'new_project.html',
                      {'form': form, 'formset': formset})

@login_required(login_url='/#login')
#User Profile
def UserProfile(request):
    if(request.method == 'POST'):

        form = UserProfileInfoForm(request.POST)
        if form.is_valid():
            PostRequest = request.POST
            User_ID =request.user
            user = UserProfileInfo.objects.get(user=User_ID)
            Postform = UserProfileInfoForm(PostRequest, instance=user)
            print(PostRequest)
            Postform.save()
            return HttpResponse('Data updated')

        else:
            return HttpResponse('Validation Failed!')

    else:
        form = UserProfileInfoForm()
        User_Projects = Project.objects.filter(user=request.user.userprofileinfo)
        context = {'User_Projects':User_Projects,'form':form}
        return render(request, 'user_profile.html',context)



#Discover Section
def Discover(request):
    All_Projects = Project.objects.all()

    Projects_Num = len(All_Projects)
    All_Cats = Category.objects.all()
    #Today_Date = datetime.datetime.today().strftime('%Y-%m-%d')

    context = {'projects':All_Projects,'Projects_Num':Projects_Num,'Cats':All_Cats}

    return render(request, 'discover.html',context)

#Single Project Section
def singleProject(request,project_id):

    Single_Project = Project.objects.get(id=project_id)
    ###COMMENTS###
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user.userprofileinfo
            comment.project = Single_Project
            comment.save()
            return HttpResponseRedirect(reverse('view_project', args=[Single_Project.id]))


    Project_Owner = UserProfileInfo.objects.get(id=Single_Project.user.id)
    Progress = (Single_Project.current/Single_Project.target)*100

    #COMMENTS
    comment_form = CommentForm()
    comments = Single_Project.comments_set.all()


    print(Project_Owner)
    context = {'project':Single_Project,'Project_Owner':Project_Owner,'Progress':Progress, 'comment_form':comment_form, 'comments':comments}
    print (context)
    return render(request, 'single_project.html',context)

#User Public Profile View
def publicProfile(request,user_id):
    User_Data = User.objects.get(id=user_id+1)
    NumProjects = Project.objects.filter(user_id=user_id).count()
    context = {'PublicUser':User_Data,'NumProjects':NumProjects}
    return render(request,'single_user.html',context)




    ###########Comments

# @login_required()
# def comments(request,id):
#     selected_project= Project.objects.get(id=id)
#     if request.method == 'POST':
#         comment_form = CommentModelForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.user = request.user.profile  # will be replaced with session user
#             comment.project = selected_project
#             comment.save()
#             return HttpResponseRedirect(reverse('info', args=[selected_project.id]))
#     else:
#         comment_form = CommentModelForm()
#         comments= selected_project.comments_set.all()
#         # tags = selected_project.tags_set.all()
#         context = {'project': selected_project, 'form': comment_form ,'comments' : comments,}
#         return render(request, 'single_project.html', context)

    ##########################################################


@login_required()
def report_comment(request,id):
    reported_comment = Comments.objects.get(id=id)

    if request.method == 'POST':
        form = CommentReport(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user.userprofileinfo
            report.comment = reported_comment
            report.save()
            return HttpResponse('Thanks For Feedback..',)
    else:
        form = CommentReport()
        context = {'form':form}
        return render(request,'report.html',context)


@login_required()
def report_project(request,id):
    reported_project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = ReportProject(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user.userprofileinfo
            report.project = reported_project
            report.save()
            return HttpResponse('Thanks For Feedback..', )
    else:
        form = ReportProject()
        context = {'form':form}
        return render(request, 'report.html', context)
