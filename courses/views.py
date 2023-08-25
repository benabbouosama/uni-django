from django.shortcuts import redirect , render
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from courses.models import Course , Filiere , Level , Module , News
import os
from django.http import JsonResponse
from django.http import HttpResponse
from Accounts.models import Professor , CoordinatorFiliere , CustomUser
from django.shortcuts import get_object_or_404
from django.contrib import messages
from app import settings
from django.http import FileResponse
from .forms import LevelSelectForm

# Create your views here.


@login_required
def create_course(request, pk):
    fname = request.GET.get('fname')
    success_message = ""

    if request.method == 'POST':
        try:
            course_title = request.POST.get('course_title')
            filiere_title = request.POST.get('filiere')  # Get selected filiere title
            level_title = request.POST.get('level')  # Get selected level title
            module_title = request.POST.get('module')  # Get selected module title
            course_description = request.POST.get('course_description')
            pdf_file = request.FILES.get('pdf_file')

            # Sanitize the directory names
            sanitized_filiere = filiere_title.replace(':', '-')
            sanitized_level = level_title.replace(':', '-')
            sanitized_module = module_title.replace(':', '-')

            # Create the path using the sanitized values
            pathDb =  os.path.join(sanitized_filiere, sanitized_level, sanitized_module)
            path = os.path.join('CreatedCourses',sanitized_filiere, sanitized_level, sanitized_module)

            # Create the directories if they don't exist
            os.makedirs(path, exist_ok=True)
            file_path = os.path.join(path, pdf_file.name)
            file_pathDb = os.path.join(pathDb, pdf_file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)
                    
            # Retrieve the corresponding instances for filiere, level, and module
            filiere = get_object_or_404(Filiere, titleFiliere=filiere_title)
            level = get_object_or_404(Level, title=level_title)
            module = get_object_or_404(Module, title=module_title)

            new_course = Course(
                title=course_title,
                description=course_description,
                filiere=filiere,
                level=level,
                module=module,
                pdf_file=file_pathDb,
            )
            new_course.save()
            success_message = "Course created :)"
            print(success_message)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print("error", e)
            messages.error(request, error_message)

        return render(request, 'internal/homeprof.html', {'fname': fname, 'id': pk , 'success_message' :success_message})

    return render(request, 'Accounts/login.html')

@login_required
def display_pdf(request):
    if request.method == 'POST':
        user = request.user
        fname = user.first_name
        lname = user.last_name
        levels = Level.objects.all()
        filieres = Filiere.objects.all()
        modules = Module.objects.all()
        id = user.idUser
        
        filiere = request.POST.get('filiere')
        level = request.POST.get('level')
        module = request.POST.get('module')
        filiere = Filiere.objects.get(idFiliere = filiere)
        level = Level.objects.get(idLevel = level)
        module = Module.objects.get(idModule = module)

        courses = Course.objects.filter(module__title=module.title, level__title=level.title, filiere__titleFiliere=filiere.titleFiliere)
        context = {'user': user,
                    'id' : id,
                    'levels': levels, 
                    'filieres': filieres,
                    'modules': modules,
                    'fname' : fname ,
                    'lname' : lname ,
                    'courses': courses ,
                    }
        print(courses)
        return render(request, 'internal/myCourses.html', context )
    
    return render(request, 'internal/myCourses.html')

def download_pdf_file(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if course.pdf_file:
        file_path = os.path.join(settings.BASE_DIR, 'CreatedCourses', str(course.pdf_file))
        # Open the file using FileResponse and return it directly
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{course.pdf_file}"'
        return response
    else:
        return HttpResponse("PDF file not found.", status=404)

    
@login_required 
def choose_level_submit(request) :
    user = request.user
    userId = user.idUser
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    users = CustomUser.objects.all()
    fname = user.first_name
    lname = user.last_name
    try:
        prof = Professor.objects.get(user_id=userId)
        profId = prof.idEnseignant

        try:
            coor = CoordinatorFiliere.objects.get(idCoordinator_id=profId)
            filiereId = coor.filiereId_id
            levels_of_filiere = Level.objects.filter(idFiliere_id=filiereId)

        except CoordinatorFiliere.DoesNotExist:
            filiereId = None
            levels_of_filiere = []

    except Professor.DoesNotExist:
        profId = None
        filiereId = None
        levels_of_filiere = []
    return render(request, 'internal/levelSchedule.html' , {'levels_of_filiere' : levels_of_filiere , 'id': userId,
        'lname': lname,
        'fname': fname, 
        'levels': levels, 
        'filieres': filieres, 
        'modules': modules, 
        'users': users,  })

@login_required
def create_schedule(request):
    user = request.user
    userId = user.idUser
    users = CustomUser.objects.all()
    fname = user.first_name
    lname = user.last_name
    if request.method == 'POST':
        selected_level = request.POST.get('selected_level')
        if selected_level:
            modules = Module.objects.filter(idNiveau_id=selected_level)
            level = Level.objects.get(idLevel=selected_level)
            return render(request, 'internal/Cschedules.html', {'modules': modules, 'level': level , 'id': userId,
        'lname': lname,
        'fname': fname, 
        'users': users,})
        else:
            # Handle the case where no level is selected
            return redirect('choose_level_submit')

@login_required      
def save_schedule(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        print(level)
        schedule_html = request.POST.get('schedule_html')

        file_path = os.path.join(settings.BASE_DIR, 'schedules', f'{level}.html')

        with open(file_path, 'w') as file:
            file.write(schedule_html)

        return JsonResponse({'message': 'Schedule saved successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def download_news_pdf(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    
    if news_item.pdf:
        file_path = os.path.join(settings.MEDIA_ROOT, str(news_item.pdf))
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    else:
        return HttpResponse("PDF file not found.", status=404)
    
@login_required
def display_schedule(request, level):
    schedule_path = os.path.join(settings.BASE_DIR, 'schedules', f'{level}.html')
    user = request.user
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    users = CustomUser.objects.all()
    fname = user.first_name
    lname = user.last_name
    
    try:
        with open(schedule_path, 'r') as html_file:
            content = html_file.read()
            return render(request, 'internal/display_schedule.html', {'content': content , 'lname': lname,
        'fname': fname, 
        'levels': levels, 
        'filieres': filieres, 
        'modules': modules, 
        'users': users ,})
    except FileNotFoundError:
        return render(request, 'schedule_not_found.html')

@login_required
def select_level(request):
    user = request.user
    levels = Level.objects.all()
    filieres = Filiere.objects.all()
    modules = Module.objects.all()
    users = CustomUser.objects.all()
    fname = user.first_name
    lname = user.last_name
   
    if request.method == 'POST':
        form = LevelSelectForm(request.POST)
        if form.is_valid():
            selected_level = form.cleaned_data['levels']
            return redirect('display_schedule', level=selected_level)
    else:
        form = LevelSelectForm()
    return render(request, 'internal/choose_level.html', { 'lname': lname,
        'fname': fname, 
        'levels': levels, 
        'filieres': filieres, 
        'modules': modules, 
        'users': users ,
        'form': form} )

@login_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, idModule=module_id)
    user = request.user
    professor = Professor.objects.get(user_id=user.idUser)
    coordinator_filiere = None
    fname = user.first_name
    lname = user.last_name
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

    if request.method == 'POST':
        module.delete()
        messages.success(request, 'Module deleted successfully.')
    else:
        messages.error(request, 'Invalid request method.')
    return render(request, 'internal/coord.html', context)
           