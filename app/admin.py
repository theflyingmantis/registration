from django.contrib import admin

from .models import *
admin.site.site_header = 'IIT Jodhpur Admin'
admin.site.register(student)
admin.site.register(course)
admin.site.register(faculty)
admin.site.register(branch_mentor)
admin.site.register(compulsary)
# admin.site.register(accounts)
# admin.site.register(fulldetail)
# admin.site.register(request1)
# admin.site.register(message)
# admin.site.register(final_fulldetail)
