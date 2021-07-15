from django.shortcuts import render,reverse,redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from datetime import datetime

from .models import Appointment




# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию


class AppointmentView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date = datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name = request.POST['client_name'],
            message = request.POST['message'],
        )
        appointment.save()

        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment':appointment,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,
            from_email='gavriloviy@mail.ru',
            to=['gavriloviy@gmail.com']
        )
        msg.attach_alternative(html_content,"text/html")
        msg.send()

        return redirect('appointments:make_appointments')

# Create your views here.
