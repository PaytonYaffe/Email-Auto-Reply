import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import model_util
from . import llm_util

def home(request): 
    #return HttpResponse("Hello from Open Avenues Build Project!")
    #return render(request,'home.html')
    all_inquiry_questions = model_util.retrieve_all_inquiry_questions()
    return render(request, 'auto_reply.html', {'inquiry_questions': all_inquiry_questions})
    

@csrf_exempt
def auto_reply_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_content = data.get("paragraph", "")

            # Now using LLM
            sender_name, receiver_name, inquiry_questions = llm_util.extract_sender_and_receiver_names(email_content)
            # Save extracted questions to database
            if inquiry_questions:
                model_util.save_inquiry_question(inquiry_questions, email_content)

            if sender_name and receiver_name:
                reply_message = (
                    f"Hi {sender_name},\n\n"
                    f"Thanks for your email. I will get back to you soon.\n\n"
                    f"Best, {receiver_name}."
                )
            else:
                reply_message = "Hi there, thanks for your email. I will get back to you soon."

            return JsonResponse({
                'reply': reply_message,
                'status': 'success',
                'receiver_name': receiver_name,
                'sender_name': sender_name,
                'inquiry_questions': inquiry_questions
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format', 'status': 'failure'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed', 'status': 'failure'}, status=405)