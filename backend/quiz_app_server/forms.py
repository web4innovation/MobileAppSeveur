__author__ = 'wissem'

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FieldList, IntegerField, Field
from wtforms.validators import DataRequired
from wtforms.widgets import TextInput


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

class UniqueTagListField(TagListField):
    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(UniqueTagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(UniqueTagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class PostQuestionForm(Form):
    question = StringField('question', validators=[DataRequired()])
    answers = UniqueTagListField(label='answers')
    solutionIndex = IntegerField(label='solutionIndex')
    tags = UniqueTagListField(label='tags')



