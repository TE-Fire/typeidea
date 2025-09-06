from django import forms

#Form跟Model耦合在一起，或者说两者的逻辑一致，Model是对数据库中字段的抽象，Form是对用户输入及Model中要展示数据的抽象
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
