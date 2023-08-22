from telnetlib import LOGOUT
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from Softprojetdjangobeya.models import Project
from .forms import LoginForm, ProjectUploadForm, SignUpForm, SubmissionForm


def home(request):
    return render(request, 'index.html')


def adminPage(request):
    return render(request, 'admin/admin.html')


def teacherPage(request):
    return render(request, 'teacher/teacher.html')


def studentPage(request):
    return render(request, 'student/student.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('/login')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('/adminpage/')
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('/teacherpage/')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('/studentpage/')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'auth/login.html', {'form': form, 'msg': msg})


@login_required
def logout_view(request):
    LOGOUT(request)
    # Redirige vers la page d'accueil ou une autre page de votre choix
    return redirect('/')


@login_required  # Assure que l'administrateur est connecté
def upload_project(request):
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.uploaded_by = request.user
            project.status = 'in_progress'  # Statut initial du projet
            project.save()
            return redirect('/')  # Rediriger vers la page d'accueil
    else:
        form = ProjectUploadForm()
    return render(request, 'admin/uploadprojectAdmin.html', {'form': form})


@login_required  # Assure que l'administrateur est connecté
def manage_projects(request):
    projects = Project.objects.all()
    return render(request, 'admin/manageprojectAdmin.html', {'projects': projects})


User = get_user_model()


@login_required  # Assure que l'administrateur est connecté
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manageuser.html', {'users': users})


@login_required
def upload_project_teacher(request):
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.uploaded_by = request.user
            project.status = 'in_progress'
            project.save()
            # Rediriger vers la liste des projets de l'enseignant
            return redirect('my_projects_teacher')
    else:
        form = ProjectUploadForm()
    return render(request, 'upload_project_teacher.html', {'form': form})


@login_required
def my_projects_teacher(request):
    projects = Project.objects.filter(uploaded_by=request.user)
    return render(request, 'my_projects_teacher.html', {'projects': projects})


@login_required
def my_projects_student(request):
    projects = Project.objects.filter(uploaded_by=request.user)
    return render(request, 'student/my_projects_student.html', {'projects': projects})


@login_required
def submit_project(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.project = project
            submission.user = request.user
            submission.save()
            # Rediriger vers la liste des projets de l'étudiant
            return redirect('my_projects_student')
    else:
        form = SubmissionForm()

    context = {'form': form, 'project': project}
    return render(request, 'submit_project.html', context)
