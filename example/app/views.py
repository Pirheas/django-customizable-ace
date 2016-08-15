from django.shortcuts import render
from .forms import MyCodeForm


def main(request):
    context = {}
    if request.method == 'POST':
        form = MyCodeForm(request.POST)
        context['form'] = form
        if form.is_valid():
            code = form.cleaned_data['code']
            print('Code:')
            print('--------------------------------------')
            print(code)
            print('--------------------------------------')
        else:
            print('INVALID FORM')
    else:
        context['form'] = MyCodeForm()
    return render(request, 'main.html', context)
