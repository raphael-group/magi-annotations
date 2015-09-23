from django.contrib import admin
from .models import Cancer, Mutation, Reference, Annotation

# Register your models here.
admin.site.register(Cancer)
admin.site.register(Mutation)
admin.site.register(Reference)
admin.site.register(Annotation)
