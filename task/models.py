from django.db import models

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    assignee = models.ForeignKey("user.CustomUser", on_delete=models.SET_NULL, related_name="task_assignee", null=True, blank=True)
    status = models.CharField(max_length=50)
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    hive = models.ForeignKey("hive.Hive", on_delete=models.CASCADE, related_name="task_hive")
    created_by = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name="task_created_by")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Task_detail", kwargs={"pk": self.pk})
