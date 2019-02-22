from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager  ##TAGS



######USER######
################

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=50)
    portfolio_site = models.URLField(blank=True)
    BirthDate = models.DateField()
    mobile = models.CharField(max_length=11, validators=[RegexValidator(regex='^01[0|1|2|5][0-9]{8}')])
    Country = CountryField()
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True,default='profile_pics/nopic.jpeg')

    def __str__(self):
        return self.FullName





class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# class Tag(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name




####PROJECT#####
################

class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    current = models.IntegerField(default=0)
    target = models.IntegerField(default=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag, related_name="projects")
    tags = TaggableManager()
    date_lastupdated = models.DateField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)
    main_pic = models.ImageField(upload_to='projects_pics', blank=True,default='projects_pics/default.jpg')
    featuredCHOICE = (
        ('1', 'Yes'),
        ('0', 'No'),
    )
    featured_project = models.CharField(max_length=1, choices=featuredCHOICE,default=0)

    def __str__(self):
        return self.title


class Project_Images(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_img = models.ImageField(upload_to='multi', blank=True, default='projects_pics/nopic.jpeg')





def get_avg_rate(self):
    return self.rate_set.all().aggregate(models.Avg("value"))


def get_total_donations(self):
    return self.donation_set.all().aggregate(models.Sum("value"))


def get_rates_count(self):
    return self.rate_set.all().count()


def get_donations_count(self):
    return self.donation_set.all().count()


def is_cancelable(self):
    return self.get_total_donations() <= 0.25 * self.target


class Donations(models.Model):
    amount = models.IntegerField()
    donation_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Rating(models.Model):
    rate = models.IntegerField(choices=[(str(i), str(i)) for i in range(6)])
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Featured(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.project


class Comments(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.TextField()
    # date = models.DateField(auto_now= True, blank= True)


class commentReport(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add= True)
    subject = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.subject

        

class projectReport(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add= True)
    subject = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.subject





