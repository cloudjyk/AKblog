from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import UserManager


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, db_index=True, unique=True, default='')
    password = models.CharField(max_length=100, default='')
    # avatar = models.FileField(upload_to='uploads/', max_length=100, default='')
    avatar = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=100, unique=True, validators=[validate_email], default='')
    about_me = models.TextField(max_length=100, default='hello')
    last_seen = models.DateTimeField(default='2018-03-20 23:36:40')
    followers = models.ManyToManyField('User', related_name='followeds')
    thumb_up_posts = models.ManyToManyField('Post', related_name='thumbupeds')
    thumb_up_users = models.ManyToManyField('User', related_name='thumbupeds')

    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    objects = UserManager()

    def check_password(self, password):
        return True


    @staticmethod
    def make_unique_nickname(username):
        if User.objects.filter(username=username).first() == None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.objects.filter(username=new_username).first() == None:
                break
            version += 1
        return new_username

    def follow(self, user):
        if not self.is_following(user):
            self.followed.add(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return user in self.followeds.all()

    def __str__(self):
        return '<User %r>' % self.username

    __repr__ = __str__


class Post(models.Model):
    body = models.TextField(default='')
    post_time = models.DateTimeField(default='2018-03-20 23:36:40')
    author = models.ForeignKey('User', related_name='posts', on_delete=models.CASCADE, default='')

    def __repr__(self):
        return '<Post %r>' % (self.body)

    __str__ = __repr__


class Comment(models.Model):
    body = models.TextField(default='')
    comment_time = models.DateTimeField(default='2018-03-20 23:36:40')
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE, default='')
    author = models.ForeignKey('User', related_name='comments', on_delete=models.CASCADE, default='')

    def __repr__(self):
        return '<Comment %r>' % (self.body)

    __str__ = __repr__
