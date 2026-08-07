from django.shortcuts import render, redirect
from .models import User, Job, JobApplication, SavedJob
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def download_improved_resume(request):

    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Improved_Resume.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI IMPROVED RESUME</b>", styles['Title']))
    story.append(Paragraph("<br/>", styles['Normal']))

    story.append(
        Paragraph(f"<b>Name:</b> {user.full_name}", styles['Normal'])
    )

    story.append(
        Paragraph(f"<b>Email:</b> {user.email}", styles['Normal'])
    )

    story.append(
        Paragraph(f"<b>Phone:</b> {user.phone}", styles['Normal'])
    )

    story.append(Paragraph("<br/><b>Professional Summary</b>", styles['Heading2']))
    story.append(
        Paragraph(
            "Motivated Computer Engineering student with strong knowledge of Python, Django, SQL and AI.",
            styles['Normal']
        )
    )

    story.append(Paragraph("<br/><b>Technical Skills</b>", styles['Heading2']))
    story.append(
        Paragraph(
            "Python, Django, HTML, CSS, JavaScript, SQL, Machine Learning",
            styles['Normal']
        )
    )

    story.append(Paragraph("<br/><b>Projects</b>", styles['Heading2']))
    story.append(
        Paragraph(
            "AI Job Portal, Quiz Management System",
            styles['Normal']
        )
    )

    story.append(Paragraph("<br/><b>AI Improvements</b>", styles['Heading2']))
    story.append(
        Paragraph(
            "ATS Friendly Resume<br/>Added Keywords<br/>Improved Project Description",
            styles['Normal']
        )
    )

    doc.build(story)

    return response

def home(request):
    return render(request, 'index.html')


def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(
            email=username,
            password=password
        ).first()

        if user:

            request.session['user_id'] = user.id
            request.session['user_name'] = user.full_name

            return redirect('dashboard')

        else:
            return render(request, 'login.html', {
                'error': 'Invalid Email or Password'
            })


    return render(request, 'login.html')



def dashboard(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')


    user = User.objects.get(id=user_id)


    applications = JobApplication.objects.filter(
        user=user
    )


    return render(request, 'dashboard.html', {

        'username': user.full_name,

        'applications': applications

    })
  
def jobs(request):

    jobs = Job.objects.all()

    experience = request.GET.get('experience')
    skills = request.GET.get('skills')
    job_type = request.GET.get('job_type')

    if experience:
        jobs = jobs.filter(experience=experience)

    if skills:
        jobs = jobs.filter(skills__icontains=skills)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    return render(request, 'jobs.html', {
        'jobs': jobs
    })

def saved_jobs(request):

    user_id = request.session.get('user_id')

    user = User.objects.get(id=user_id)

    saved_jobs = SavedJob.objects.filter(user=user)

    return render(request, 'saved_jobs.html', {
        'saved_jobs': saved_jobs
    })



def profile(request):

    user_id = request.session.get('user_id')

    user = User.objects.get(id=user_id)

    if request.method == "POST":

        if request.FILES.get('photo'):

            user.photo = request.FILES['photo']
            user.save()

    return render(request, 'profile.html', {
        'user': user
    })

def improve_resume(request):

    return render(request, 'improve_resume.html')

def register(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        User.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')



def user_logout(request):

    request.session.flush()

    return redirect('login')


def apply_job(request, job_id):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')


    user = User.objects.get(id=user_id)

    job = Job.objects.get(id=job_id)


    JobApplication.objects.create(
        user=user,
        job=job
    )

    return redirect('jobs')    

def search_jobs(request):

    job = request.GET.get('job', '')
    location = request.GET.get('location', '')

    jobs = Job.objects.filter(
        title__icontains=job,
        location__icontains=location
    )

    return render(request, 'jobs.html', {
        'jobs': jobs
    })

def edit_profile(request):

    user_id = request.session.get('user_id')

    user = User.objects.get(id=user_id)

    if request.method == "POST":

        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')

        user.save()

        return redirect('profile')


    return render(request, 'edit_profile.html', {
        'user': user
    })

def upload_resume(request):
    if request.method == "POST":

        user_id = request.session.get('user_id')

        user = User.objects.get(id=user_id)

        resume = request.FILES.get('resume')

        if resume:
            user.resume = resume
            user.save()

            print("Saved Resume:", user.resume)

    return redirect('profile')

def generated_resume(request):
    return render(request, 'generated_resume.html')

def save_job(request, job_id):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    job = Job.objects.get(id=job_id)

    SavedJob.objects.get_or_create(
        user=user,
        job=job
    )

    return redirect('jobs')   