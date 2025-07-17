from django.db import models

# Create your models here.
class User_Type(models.Model):
    uset_id = models.AutoField(db_column='uset_id', primary_key=True)
    uset_type = models.CharField(db_column='uset_type',max_length=50)

    class Meta:
        db_table = 'user_type'
        managed = False

    def __str__(self):
        return self.uset_type


class User_Data(models.Model):
    use_id = models.AutoField(db_column='use_id', primary_key=True)
    use_name = models.CharField(db_column='use_name',max_length=100)
    uset = models.ForeignKey(User_Type, db_column='uset_id', on_delete=models.CASCADE)
    use_passwords = models.CharField(db_column='use_passwords',max_length=128)  # ⚠️ debería ser hash, no texto plano

    class Meta:
        db_table = 'user_data'
        managed = False

    def __str__(self):
        return self.use_name
    
class Email(models.Model):
    ema_email = models.EmailField(db_column='ema_email', primary_key=True, max_length=100)
    use = models.ForeignKey(User_Data, db_column='use_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'email'
        managed = False

    def __str__(self):
        return self.ema_email