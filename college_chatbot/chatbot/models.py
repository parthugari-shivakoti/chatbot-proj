from djongo import models  # Import from djongo

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    data = models.JSONField()  # Store complex data structures
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name