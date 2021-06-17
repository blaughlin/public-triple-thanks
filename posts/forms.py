from django import forms
from .models import *
from localflavor.us.forms import USStateSelect


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['post','private']
		labels = {'post': ""}
		widgets = {
		'post': forms.Textarea(
			attrs={'class':'form-control form-rounded','rows':"7", 'placeholder': "Enter gratitude here"}),
		}

class ProfileForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name','last_name','city','state','zip_code','about','profile_pic','lattitude', 'longitude',)
		widgets = {
		'lattitude':forms.HiddenInput(),
		'longitude':forms.HiddenInput(),

		'first_name': forms.TextInput(
			attrs={
				'class': 'form-control',
			}),
		'last_name': forms.TextInput(
			attrs={
				'class': 'form-control',
			}),
		'city': forms.TextInput(
			attrs={
				'class': 'form-control',
			}),
		'state': forms.Select(
		attrs={
		'class': 'form-control',
		}),
		'zip_code': forms.NumberInput(
			attrs={
				'class': 'form-control',
			}),
		'about': forms.Textarea(
			attrs={
				'class': 'form-control', 'rows':3
			})
		}


