from django.shortcuts import render

# Create your views here.
data = [
{"title": "Users", "count": 150},
{"title": "Orders", "count": 320},
{"title": "Revenue", "count": "12450"},
]

def index(request):
    return render(request, "pages/dashboard.html", {"data": data})