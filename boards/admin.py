from django.contrib import admin
from .models import Board
# Register your models here.

admin.site.register(Board)	#only admin can create board
