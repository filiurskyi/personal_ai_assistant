from django.shortcuts import render
from dashboard.tasks import run_framework, restart_framework, stop_framework, terminate_framework

def dashboard(request):
    action = None
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'run':
            run_framework(None)
        elif action == 'restart':
            restart_framework(None)
        elif action == 'stop':
            stop_framework(None)
        elif action == 'terminate':
            terminate_framework(None)

    return render(request, 'dashboard/dashboard.html', context={"text": action})
