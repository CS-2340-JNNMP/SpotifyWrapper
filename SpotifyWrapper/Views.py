from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os

# load env variables
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = str(os.getenv('CLIENT_ID'))
CLIENT_SECRET = str(os.getenv('CLIENT_SECRET'))

