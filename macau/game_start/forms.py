from django import forms


class NickForm(forms.Form):
    nick = forms.CharField(label="nick", max_length=40)


class PinForm(forms.Form):
    pin = forms.IntegerField(label="pin", max_value=1000000, min_value=0)
