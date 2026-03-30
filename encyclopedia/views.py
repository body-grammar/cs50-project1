from django.shortcuts import render, redirect
import random
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, 'encyclopedia/error.html', {
            "message": "Page was not found."
        })
    html_content = markdown2.markdown(entry)
    return render(request, 'encyclopedia/entry.html', {
        'title': title,
        'entry': html_content
    })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    if query in entries:
        return render(request, 'encyclopedia/entry.html', {
            'title': query,
            'entry': util.get_entry(query)
        })
    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, 'encyclopedia/search.html', {
        "query": query,
        "results": results
    })

def edit(request, title):
    content = util.get_entry(title)

    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)

        return redirect("entry", title)
    
    return render(request, 'encyclopedia/edit.html', {
        "title": title,
        "content": content,
    })

def random_page(request):
    entries = util.list_entries()     
    if not entries:                     
        return redirect("index")
    random_entry = random.choice(entries)
    return redirect("entry", random_entry)

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if util.get_entry(title) is not None:
            return render(request, 'encyclopedia/error.html', {
                "message": "An entry with this title already exists."
            })
        
        util.save_entry(title, content)

        return redirect("entry", title)
    
    return render(request, "encyclopedia/new.html")

