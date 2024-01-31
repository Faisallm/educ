from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        # adding a new definition to existing positive integer field
        # definition
        self.for_fields = for_fields
        # all existing definitions in the positiveintegerField
        # are also to be declared here
        super().__init__(*args, **kwargs)
        
    # modifying the pre_save() method of the positiveIntegerField
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # dictionary comprehension
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                    
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
                
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        
        else:
            return super().pre_save(model_instance, add)