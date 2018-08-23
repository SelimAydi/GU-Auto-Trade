# import modeltranslation
from modeltranslation.translator import register, translator, TranslationOptions
from oscar.apps.catalogue.models import Product, Category
from .models import Vehicles


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Category, CategoryTranslationOptions)

class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

translator.register(Product, ProductTranslationOptions)

# class VehiclesTranslationOptions(TranslationOptions):
#     fields = ('headline', 'description',)
#
# translator.register(Vehicles, VehiclesTranslationOptions)


print("IS ANY OF THIS TAKING PLACE?")
# from oscar.apps.catalogue.models import *