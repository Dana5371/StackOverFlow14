from django.contrib import admin

from .models import *


class ImageInLine(admin.TabularInline):
    model = CodeImage
    max_num = 5
    min_num = 1


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [ImageInLine,]


admin.site.register(Reply)
admin.site.register(Comment)