from django.shortcuts import render, redirect, get_object_or_404
from .models import Catagory, Character, Character_Details
from django.contrib import messages

def home(request):
    characters=Character.objects.all().order_by('priority')
    return render(request, "web/index.html",{"characters": characters,"name":"name"})

def category(request):
    categories = Catagory.objects.all() 
    return render(request, "web/category.html", {"categories": categories})

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