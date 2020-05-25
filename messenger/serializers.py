from account.models import Account
from . models import Team
from  rest_framework import serializers

class AccountTeam(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'last_name', 'first_name']




class NewTeam(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Team
        fields = ['name']


