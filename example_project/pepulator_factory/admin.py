from django.contrib import admin
from pepulator_factory.models import Pepulator, Distributor, Jamb, Knuckle

class KnuckleInline (admin.StackedInline):
    model = Knuckle

class JambInline (admin.StackedInline):
    model = Jamb

class PepulatorAdmin (admin.ModelAdmin):
    inlines = [KnuckleInline, JambInline]

admin.site.register(Pepulator, PepulatorAdmin)
admin.site.register(Distributor)
