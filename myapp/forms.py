from django import forms
from myapp.models import Order, Feedback, Student


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Student', 'courses', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect(),
            'order_date': forms.SelectDateWidget()
        }

class InterestForm(forms.Form):
    CHOICES = [('1', 'YES'), ('0', 'NO')]
    interested = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    levels = forms.IntegerField(initial=1)
    comments = forms.CharField(required=False, widget=forms.Textarea, label= 'Additional Comments')

# class RegisterForm(forms.Form):
#     CHOICES = [('1', 'YES'), ('0', 'NO')]
#     username = forms.CharField(required=True, widget=forms.TextInput, label= 'username')
#     password = forms.CharField(required=True, widget=forms.PasswordInput, label= 'password')
#     first_name = forms.CharField(required=True, widget=forms.TextInput, label= 'first name')
#     last_name = forms.CharField(required=True, widget=forms.TextInput, label= 'last name')
#     city = forms.CharField(required=True, widget=forms.TextInput, label= 'city')
#     interested_in = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username','password','first_name','last_name','email','city','interested_in']
        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }
        labels = {
            'username' : 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'city' : 'City',
            'interested_in': 'Topic Interested in',
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields=['name','suggestions']
        widgets = {
            'name': forms.TextInput(),
            'suggestions': forms.Textarea()
        }