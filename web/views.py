import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Catagory, Character, Character_Details, Quize
from django.contrib import messages

def home(request):
    characters = Character.objects.all().order_by('priority')
    return render(request, "web/index.html", {"characters": characters, "name": "name"})

def category(request):
    categories = Catagory.objects.all()
    return render(request, "web/category.html", {"categories": categories})

def quize(request):
    if 'score' not in request.session or 'questions' not in request.session:
        return redirect('reset_quiz')

    question_ids = request.session.get('questions', [])
    current_question_index = request.session.get('current_question', 0)

    valid_questions = Quize.objects.filter(id__in=question_ids).values_list('id', flat=True)
    question_ids = [qid for qid in question_ids if qid in valid_questions]
    request.session['questions'] = question_ids

    if current_question_index >= len(question_ids):
        score = request.session.get('score', 0)
        total_questions = len(question_ids)
        return render(request, "web/quize_result.html", {"score": score, "total": total_questions})

    try:
        question = Quize.objects.get(id=question_ids[current_question_index])
    except Quize.DoesNotExist:
        messages.warning(request, "The current question is no longer available. Skipping to the next one.")
        request.session['current_question'] += 1
        return redirect('quize')

    options = [
        {"text": question.op1, "img_url": question.op1_img_url},
        {"text": question.op2, "img_url": question.op2_img_url},
        {"text": question.op3, "img_url": question.op3_img_url},
        {"text": question.op4, "img_url": question.op4_img_url},
    ]
    random.shuffle(options)

    if request.method == "POST":
        selected_answer = request.POST.get('answer')
        if selected_answer == getattr(question, question.ans):
            request.session['score'] += 1

        request.session['current_question'] += 1
        return redirect('quize')

    return render(request, "web/quize.html", {
        "question": question,
        "options": options,
        "question_index": current_question_index,
        "answer": getattr(question, question.ans),
        "defaculty":question.defaculty,
    })

def reset_quiz(request):
    questions = list(Quize.objects.all())
    if not questions:
        messages.error(request, "No quiz questions available. Please try again later.")
        return redirect('home')

    random.shuffle(questions)
    request.session['questions'] = [q.id for q in questions]  # Only include valid IDs
    request.session['total_questions'] = len(questions)
    request.session['score'] = 0
    request.session['current_question'] = 0
    return redirect('quize')

def quiz_result(request):
    score = request.session.get('score', 0)
    total = request.session.get('total_questions', 0)  # Get total questions from session
    half_total = total / 2  # Divide to show half of the total for comparison

    # Handle case if total_questions is 0, which should not happen after initialization
    if total == 0:
        messages.error(request, "No questions found. Please start the quiz again.")
        return redirect('home')

    return render(request, "web/quize_result.html", {"score": score, "total": total, "half_total": half_total})

def characters(request, name):
    if Catagory.objects.filter(name=name):
        characters = Character.objects.filter(catagory__name=name).order_by('priority')
        color = Catagory.objects.filter(name=name).first().color
        return render(request, "web/characters.html", {"characters": characters, "name": name, "color": color})
    else:
        messages.warning(request, "No such category found.")
        return redirect('category')

def characterDetails(request, category, name):
    if Character.objects.filter(name=name):
        details = Character_Details.objects.filter(character__name=name)
        character = Character.objects.get(name=name)
        img = character.Character_image_url
        return render(request, "web/characterDetails.html", {"details": details, "name": name, "img": img})
    else:
        messages.warning(request, "No such character found.")
        return redirect('characters', name=category)

def search_character(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        if query:
            if Character.objects.filter(name__iexact=query).exists():
                character = Character.objects.get(name__iexact=query)
                category_name = character.catagory.name
                return redirect('characterDetails', category=category_name, name=character.name)
            else:
                messages.warning(request, f"No character found for '{query}'")
                return redirect('home')
        else:
            return redirect('home')
