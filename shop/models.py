
from django.db import models
from django.utils.text import slugify

from mptt.fields import TreeForeignKey, TreeManyToManyField
from mptt.models import MPTTModel

from user.models import User

def generate_text(text):
    """
    Для перевода кириллицы на латиницу
    :param text: str
    :return: str
    """
    if text:
        my_string = text.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_...:Y"
            )
        )
        my_string = slugify(my_string)
        return my_string
    return ""

class Сharacteristic(models.Model):
    name = models.CharField(max_length=120)
    # value =


class Category(MPTTModel):
    class Meta:
        db_table = "Category"
        verbose_name_plural = "Категории"
        verbose_name = "Категория"

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Категория",
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родитель",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Поле URL',
    )
    icon = models.ImageField(
        upload_to='icon/category',
        null=True,
        blank=True,
        default=None
    )

    def __unicode__(self):
        return self.name

    class MTTPMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent == 'self':
            self.slug = generate_text(self.category.name)
        self.slug = generate_text(self.name) + "_" + generate_text(self.parent.name)
        super().save(*args, **kwargs)




