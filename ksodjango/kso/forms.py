from django import forms
from django.forms.util import ErrorList

class mailingListForm(forms.Form):
    firstName = forms.CharField(max_length=50, label="First name")
    lastName = forms.CharField(max_length=50, label="Last name")
    emailAddress = forms.EmailField(label="Email address")

class DivErrorList(ErrorList):
     def __unicode__(self):
         return self.as_divs()
     def as_divs(self):
         if not self: return u''
         return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])
