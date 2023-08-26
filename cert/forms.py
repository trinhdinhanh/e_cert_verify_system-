
# import form class from django
from django import forms
 
# import GeeksModel from models.py
from .models import WaitBlock

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from account.models import User
 
# create a ModelForm
class WaitBlockForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = WaitBlock
        fields = ["teacher", "course_name", "final_mark"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Gửi'))
        self.fields["teacher"].queryset = User.objects.filter(is_teacher=True)