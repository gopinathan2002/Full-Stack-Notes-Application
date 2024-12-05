from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Note(models.Model):

    CATEGORY = (('BUSINESS', 'Business'),
                ('PERSONAL', 'Personal'),
                ('IMPORTANT', 'Important'))

    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.CharField(max_length=15, choices=CATEGORY, default='PERSONAL')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:  # Always update the slug if there's a title
            slug_base = slugify(self.title)
            slug = slug_base

            # Check if the slug already exists, and if so, append a random string
            if Note.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f'{slug_base}-{get_random_string(5)}'

            self.slug = slug

        super(Note, self).save(*args, **kwargs)