from django import forms
class FileForm(forms.Form):
    file = forms.FileField(
    # 支持多文件上传
    #widget=forms.ClearableFileInput(attrs={'multiple': True}),
    # 支持单文件上传
    widget=forms.FileInput,
    label='请选择文件',
    )