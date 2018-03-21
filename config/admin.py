from django.contrib import admin

# Register your models here.


from .models import ReDoc,DockerServer,Dockerenv


class DockerServerAdmin(admin.ModelAdmin):
    list_display = ["ip","port","role","dockerenv"]

class DockerenvAdmin(admin.ModelAdmin):
    list_display = ["envname","envdescribe"]

class RedocAdmin(admin.ModelAdmin):
    list_display = ["dockername","projectname","projecturl","projectpath","dockerenv"]



admin.site.register(ReDoc,RedocAdmin)
admin.site.register(DockerServer,DockerServerAdmin)
admin.site.register(Dockerenv,DockerenvAdmin)