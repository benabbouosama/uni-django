from django.shortcuts import redirect, render , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from Accounts.models import Account , CustomUser , CadreAdministrateur , Professor , Student , CoordinatorFiliere
from courses.models import Level , Module , Filiere , News
from django.contrib import messages 
from django.contrib.auth import authenticate , login , logout
from app import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from Accounts.tokens import generate_token
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist





# Create your views here.
@login_required
def homeprof(request, pk):
    user = request.user
    fname = user.first_name
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    news = News.objects.all()
    return render(request, 'internal/homeprof.html', {'fname': fname, 'news' : news , 'id':pk , 'levels': levels, 'filieres': filieres, 'modules': modules})
def signup(request):
    if request.method == "POST":
        cin = request.POST.get('cin')
        username = request.POST.get('email')
        last_name = request.POST.get('last_name')
        arabic_last_name = request.POST.get('ArabicLast_name')
        picture = request.FILES.get('picture')
        first_name = request.POST.get('first_name')
        arabic_first_name = request.POST.get('ArabicFirst_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        pass2 = request.POST.get('confirm_password')

        if CustomUser.objects.filter(username=username):
            messages.error(request , "username already exists")
            return render(request , 'Accounts/signup.html',{'message' : 'Email exists'})
        if password != pass2 :
            return render(request , 'Accounts/signup.html',{'message' : 'passwords should match'})
        # You can now create the user instance and save it to the database
        try:
            if picture is not None :
                user = CustomUser.objects.create(
                    cin=cin,
                    username=username,
                    last_name=last_name,
                    ArabicLast_name=arabic_last_name,
                    picture=picture,
                    first_name=first_name,
                    ArabicFirst_name=arabic_first_name,
                    phone=phone,
                    
                )
            else :
                user = CustomUser.objects.create(
                    cin=cin,
                    username=username,
                    last_name=last_name,
                    ArabicLast_name=arabic_last_name,
                    first_name=first_name,
                    ArabicFirst_name=arabic_first_name,
                    phone=phone,
                )
            # Hash the password before saving it
            user.set_password(password)
            user.is_active = False
            user.save()
            
            account = Account.objects.create(
                 login = last_name+first_name ,
                 password = user.password ,
            )
            account.save() 
            
            if user_type == "cadre_administrateur":
                grade = request.POST.get('grade')
                CadreAdmin = CadreAdministrateur.objects.create(
                    grade=grade,
                    User = user,
                )
                CadreAdmin.save()
            
            elif user_type == "professor":
                specialite = request.POST.get('specialite')
                professor = Professor.objects.create(
                    specialite=specialite,
                    user = user,
                )
                professor.save()
            
            elif user_type == "student":
                cne = request.POST.get('cne')
                birth = request.POST.get('dateNaissance')
                stdent = Student.objects.create(
                    cne=cne,
                    dateNaissance=birth,
                    User=user,
                )
                stdent.save()
            
            #The following part of code is designed for email confirmation :
        #================================================================================================
            # subject = "NOREPLY"
            # message = "Hello "+ user.last_name + "!! \n" + " Welcome to ou e-services, please confirm your email adress , we have sent a confirmation email ."
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [user.username]
            # send_mail(subject , message , from_email , to_list , fail_silently=True)
            # messages.success(request, "Your account has been created and needs admin approval.")


            # #Email adress confirmation email : 
            # print(user.username)
            # current_site = get_current_site(request)
            # email_subject = " Confirmation email. "
            # message2 = render_to_string('email_confirmation.html',{
            #     'name': user.first_name ,
            #     'domain' : current_site.domain ,
            #     'uid' : urlsafe_base64_encode(force_bytes(user.pk)) ,
            #     'token' : generate_token.make_token(user)
            # })
            # email = EmailMessage(
            #     email_subject, 
            #     message2 ,
            #     settings.EMAIL_HOST_USER ,
            #     [user.username],
            # )
            # email.fail_silently = True
            # email.send()
        #================================================================================================

            return render(request, "Accounts/success.html")
        except Exception as e:
            # Handle any errors that may occur during user creation
            # For example, if a user with the same email already exists, you can display an error message
            error_message = str(e)
            print(error_message)
            return render(request, "Accounts/signup.html", {"error_message": error_message})

    return render(request, "Accounts/signup.html")

def signin(request):
    if request.method == "POST":
        myUsername = request.POST.get('username')
        myPassword = request.POST.get('password')
        user = authenticate(username=myUsername, password=myPassword)
        if 'next' in request.POST:
            return redirect(request.POST.get("next"))
        else :
            if user is not None:
                login(request, user)
                levels = Level.objects.all()
                filieres = Filiere.objects.all()
                modules = Module.objects.all()
                publishers = Professor.objects.all()
                users = CustomUser.objects.all()
                fname = user.first_name
                lname = user.last_name
                news = News.objects.all()
                if user.is_active == False :
                    return render(request , 'Accounts/login.html', {'fmessage' : '**Your account is not activated'})

                try:
                    student = Student.objects.get(User_id=user.idUser)
                    students = Student.objects.all()
                    return render(request, 'internal/home.html', {'lname': lname, 'news' : news , 'fname': fname, 'levels': levels, 'students': students, 'filieres': filieres, 'modules': modules, 'users': users})
                except Student.DoesNotExist:
                    pass

                try:
                    professor = Professor.objects.get(user_id=user.idUser)
                    return render(request, 'internal/homeprof.html', {'fname': fname, 'news' : news, 'id':user.idUser , 'levels': levels, 'filieres': filieres, 'modules': modules, 'publishers': publishers, 'users': users})
                except Professor.DoesNotExist:
                    pass

                try:
                    cadre_admin = CadreAdministrateur.objects.get(User_id=user.idUser)
                    return render(request, 'internal/home.html', {'fname': fname, 'news' : news, 'levels': levels, 'filieres': filieres, 'modules': modules, 'publishers': publishers, 'users': users})
                except CadreAdministrateur.DoesNotExist:
                    pass
            else:
                messages.error(request, 'Bad credentials')
                fmessage = "Bad credentials, try again please!"
                return render(request, 'Accounts/login.html', {'fmessage': fmessage})

    return render(request, 'Accounts/login.html')


def signout(request):
    logout(request)
    messages.success(request , "Logged Out successfully .")
    return redirect('/')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
    
def homeint(request, pk):
    user = request.user
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    users = CustomUser.objects.all()
    fname = user.first_name
    lname = user.last_name
    news = News.objects.all()
    context = {
        'id': pk,
        'lname': lname,
        'fname': fname, 
        'levels': levels, 
        'filieres': filieres, 
        'modules': modules, 
        'users': users ,
        'news' : news 
    }
    return render(request, 'internal/home.html' , context)

@login_required
def coordination(request, pk):
    user = CustomUser.objects.get(pk=pk)
    professor = Professor.objects.get(user_id=user.idUser)
    coordinator_filiere = None
    fname = user.first_name
    lname = user.last_name
    try:
        coordinator_filiere = CoordinatorFiliere.objects.get(idCoordinator=professor.idEnseignant)
        levels = Level.objects.filter(idFiliere=coordinator_filiere.filiereId)
        modules_by_level = {}
        for level in levels:
            modules_by_level[level] = Module.objects.filter(idNiveau=level)
        context = {
            'fname' : fname ,
            'lname' : lname ,
            'user': user,
            'coordinator_filiere': coordinator_filiere,
            'levels': levels,
            'modules_by_level': modules_by_level,
        }
    except CustomUser.DoesNotExist:
        context = {
            'message': 'User does not exist.',
        }
    except CoordinatorFiliere.DoesNotExist:
        print('no')
        context = {
            'fname' : fname ,
            'lname' : lname ,
            'user': user,
            'coordinator_filiere': coordinator_filiere,
            'message': 'You are not a coordinator at the moment, sorry!',
        }

    return render(request, 'internal/coord.html', context)
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.ArabicFirst_name = request.POST.get('ArabicFirst_name')
        user.ArabicLast_name = request.POST.get('ArabicLast_name')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()
    user = request.user
    fname = user.first_name
    lname = user.last_name
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    users = CustomUser.objects.all()
    lname = user.last_name
    try:
        student = Student.objects.get(User_id=user.idUser)
        students = Student.objects.all()
        return render(request, 'internal/settingsStudent.html', {'lname': lname, 'fname': fname, 'levels': levels, 'students': students, 'filieres': filieres, 'modules': modules, 'users': users})
    except Student.DoesNotExist:
        pass

    try:
        professor = Professor.objects.get(user_id=user.idUser)
        return render(request, 'internal/settings.html', {'fname': fname, 'id':user.idUser , 'levels': levels, 'filieres': filieres, 'modules': modules, 'users': users})
    except Professor.DoesNotExist:
        pass
    context = {'user': user,
            'fname' : fname ,
                'lname' : lname }
    return render(request, 'internal/settings.html', context)

@login_required
def user_settings(request):
    user = request.user
    fname = user.first_name
    lname = user.last_name
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    users = CustomUser.objects.all()
    lname = user.last_name
    try:
        student = Student.objects.get(User_id=user.idUser)
        students = Student.objects.all()
        return render(request, 'internal/settingsStudent.html', {'lname': lname, 'fname': fname, 'levels': levels, 'students': students, 'filieres': filieres, 'modules': modules, 'users': users})
    except Student.DoesNotExist:
        pass

    try:
        professor = Professor.objects.get(user_id=user.idUser)
        return render(request, 'internal/settings.html', {'fname': fname, 'id':user.idUser , 'levels': levels, 'filieres': filieres, 'modules': modules, 'users': users})
    except Professor.DoesNotExist:
        pass
    context = {'user': user,
            'fname' : fname ,
                'lname' : lname }
    return render(request, 'Accounts/index.html', context)

@login_required
def courses(request):
    user = request.user
    fname = user.first_name
    lname = user.last_name
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    id = user.idUser
    context = {'user': user,
                'id' : id,
                'levels': levels, 
                'filieres': filieres,
                'modules': modules,
                'fname' : fname ,
                'lname' : lname 
                }
    try:
        student = Student.objects.get(User_id=user.idUser)
        students = Student.objects.all()
        return render(request, 'internal/myCourses.html', context)
    except Student.DoesNotExist:
        pass

    try:
        professor = Professor.objects.get(user_id=user.idUser)
        return render(request, 'internal/courses.html', context)
    except Professor.DoesNotExist:
        pass
    return render(request, 'internal/courses.html', context)


def home(request):
    return render(request , 'Accounts/index.html')
 
    

