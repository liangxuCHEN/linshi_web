# encoding=utf8
from django import forms

# ALGO_STYLE = (("1", u"算法1"), ("2", u"算法2"), ("3", u"算法3"))


class AlgoForm(forms.Form):
    algo_style = list()
    for i in range(0, 60):
        algo_style.append((str(i), u'算法%d' % i))
    algo_style = tuple(algo_style)
    algo_list = forms.MultipleChoiceField(
        label=u'算法类型',
        choices=algo_style,
        widget=forms.CheckboxSelectMultiple())
