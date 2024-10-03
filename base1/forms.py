from django.forms import ModelForm
from .models import Room, Topic

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
