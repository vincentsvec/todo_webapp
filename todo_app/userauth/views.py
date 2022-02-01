from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login


def signup(response):
    """
    signing up a user to database
    """

    if response.method == 'POST':
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(response, new_user)

            return redirect("/")

    form = RegisterForm()

    return render(response, "userauth/signup.html", {"form": form})
