#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
import re

class LoginForm(forms.Form):
    username = forms.CharField(initial='pick a username', widget=forms.TextInput, required=True, help_text='pick a username', error_messages={'required': 'Please enter your name'})
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='your password', error_messages={'required': 'Please enter password here'})

    def email_check(self):
        if re.match(r'^[0-9a-zA-Z][0-9a-zA-Z\-\_\s]*@[a-zA-Z0-9]+\.com(\.cn)?$', self.cleaned_data['email']):
            return True

class RegForm(forms.Form):
    username = forms.CharField(initial='pick a username', widget=forms.TextInput, required=True, help_text='pick a username', error_messages={'required': 'Please enter your name'})
    email = forms.EmailField(widget=forms.EmailInput, required=True, help_text='me@example.com', error_messages={'required': 'Please enter an email address'})
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='your password', error_messages={'required': 'Please enter password here'})
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, help_text='your password again', error_messages={'required': 'Please enter password again'})
    # remember_me = forms.BooleanField(widget=forms.CheckboxInput, required=True)

    def pw_check(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            return True

    def email_check(self):
        # print(self.cleaned_data['email'])
        if re.match(r'^[0-9a-zA-Z][0-9a-zA-Z\-\_\s]*@[a-zA-Z0-9]+\.com(\.cn)?$', self.cleaned_data['email']):
            return True

    def name_check(self):
        if re.match(r'^[a-zA-Z0-9]{1,20}$', self.cleaned_data['username']):
            return True

class EditForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    about_me = forms.CharField(widget=forms.TextInput)

class PostForm(forms.Form):
    body = forms.CharField(widget=forms.TextInput,  required=True, help_text='What a nice day!', error_messages={'required': 'Tell friends what\'s new!'})