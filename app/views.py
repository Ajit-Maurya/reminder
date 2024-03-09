from math import remainder
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt

from .models import Reminder
from  .forms import ReminderForm
from .task import send_remainder_email
# Create your views here.

@csrf_exempt
@login_required
def create_reminder(request):
    if request.method == 'POST':
        # form validatation
        form = ReminderForm(request.POST)
        if form.is_valid():
            user = request.user
            message = form.cleaned_data['message']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            entered_datetime = timezone.make_aware(timezone.datetime.combine(date, time))

            if entered_datetime < timezone.now():
                return JsonResponse({'error': 'reminder cannot be in the past'}, status=400)

            # if time < timezone.now().time() or date < timezone.now().date():
            #     return JsonResponse({'error':'reminder cannot be in past'},status=400)

            reminder = Reminder(
                user=user,
                message=message,
                date=date,
                time=time,
            )
            reminder.save()

            send_remainder_email.delay(reminder.id)

            return JsonResponse({'message':'Reminder created succesfully'}, status=201)
        
        return JsonResponse({'erorrs':form.errors}, status=400)
    
    return HttpResponseBadRequest("Invalid request")


@csrf_exempt
def user_login(request):
    '''used for login
        parameters:
        username: str
        password: str

        return http status 200 or 400
    '''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return JsonResponse({'message':'Username and Password is required'},status=400)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return JsonResponse({'message':'Logged in successfuly'})
        return JsonResponse({'message':'Invalid username or password'})
    return JsonResponse({'error':'Invalid request method'}, status=400)


@csrf_exempt
@login_required    
def user_logout(request):
    '''
    used of logout

    parameter: None

    returns http status 200 or 400
    '''
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message':'Logged out succesfully'})
    return JsonResponse({'error':'Invalid request method'},status=400)