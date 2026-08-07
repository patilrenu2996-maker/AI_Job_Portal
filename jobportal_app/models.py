from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name

class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    description = models.TextField()
    experience = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=200, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.full_name} - {self.job.title}"

class JobApplication(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    applied_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=50,
        default="Pending"
    )

    def __str__(self):
        return self.user.full_name + " - " + self.job.title

