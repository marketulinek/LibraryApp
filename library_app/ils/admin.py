from django.contrib import admin
import ils.models as models

admin.site.register(models.Author)
admin.site.register(models.Book)
admin.site.register(models.Librarian)
admin.site.register(models.Publisher)
admin.site.register(models.Reader)