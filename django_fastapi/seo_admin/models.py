from django.db import models


class SimplePage(models.Model):
    name = models.CharField('Название',
                            max_length=100,
                            unique=True)
    identificator = models.CharField('Идентификатор',
                                     max_length=100,
                                     unique=True)
    title = models.TextField('title')
    description = models.TextField('description')
    keywords = models.TextField('keywords')
    upper_content = models.TextField('upper')
    lower_content = models.TextField('lower')

    class Meta:
        verbose_name = 'Seo страница'
        verbose_name_plural = 'Seo страницы'

    def __str__(self):
        return self.name
    

class FAQCategory(models.Model):
    name = models.CharField('Название',
                            max_length=100)
    
    class Meta:
        verbose_name = 'F.A.Q Категория'
        verbose_name_plural = 'F.A.Q Категории'

    def __str__(self):
        return self.name
    

class FAQPage(models.Model):
    question = models.TextField('Вопрос')
    answer = models.TextField('Ответ')
    category = models.ForeignKey(FAQCategory,
                                 verbose_name='Категория',
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = 'F.A.Q Страница'
        verbose_name_plural = 'F.A.Q Страницы'

    def __str__(self):
        return self.question