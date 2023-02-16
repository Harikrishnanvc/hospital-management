from .models import Customer
from haystack import indexes
from users.models import UserDetails

class CustomerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    other_names = indexes.CharField(model_attr='other_names')
    email = indexes.CharField(model_attr='email', default=" ")
    phone = indexes.CharField(model_attr='phone', default=" ")
    balance = indexes.IntegerField(model_attr='balance', default="0")
    customer_status = indexes.CharField(model_attr='customer_status')
    address = indexes.CharField(model_attr='address', default=" ")

    def get_model(self):
        return Customer

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class UserDetailsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    user_role = indexes.CharField(model_attr='user_name')

    def get_model(self):
        return UserDetails

    def index_queryset(self, using=None):
        return self.get_model().objects.all()