from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from profiles.models import Profile
from comments.models import Comment
from django.shortcuts import reverse


# Create your models here.
class QuestionCategoryManager(models.Manager):
    
    @staticmethod
    def popular_categories():
        #this method will return top 5 categories
        c = Category.objects.annotate(num_questions=models.Count('question'))
        cat = c.order_by('-num_questions')[:5]
        return cat

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    objects = QuestionCategoryManager()

    def __str__(self):
        return self.name

    def slug_key(self):
        return self.slug

    def get_number(self):
        # this method returns a number of related questions
        c = Category.objects.annotate(num_questions=models.Count('question')).filter(id=self.id)
        return c[0].num_questions

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Autor")
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Tytuł")
    content = models.TextField(verbose_name="Treść")
    votes = models.ManyToManyField(Profile, related_name='vote_system', through='VoteSystem')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, verbose_name="Kategoria")
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.created = timezone.now()
            self.slug = slugify(str(self.title + " " + self.author.user.username
                                    + " " + self.created.strftime('%d-%m-%Y')))
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("questions:question-detail-view", kwargs={"slug": self.slug})

    def count_score(self):
        total_score = 0
      
        for vote in self.vote_question.all().values('value'):
            if vote['value'] == 'like':
                total_score += 1
            else:
                total_score -= 1
        return total_score
        # for vote in self.votes.all():
        #     if vote.value == 'like':
        #         total_score += 1
        #     else:
        #         total_score -= 1
        # return total_score

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs


class Answer(models.Model):
    created = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET(value='Deleted'))
    text = models.TextField(null=True)
    best_answer = models.BooleanField(default=False, null=True, blank=True)
    parent = models.ForeignKey('self',null=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class VoteSystem(models.Model):
    
    VOTE_CHOICES = (
        ('like', 'Like'),
        ('unlike', 'Unlike'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='vote_question')
    value = models.CharField(choices=VOTE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question}"

    @property
    def count_score(self):
        value = 0
        if self.value == 'like':
            value += 1
        else:
            value -= 1
        return value