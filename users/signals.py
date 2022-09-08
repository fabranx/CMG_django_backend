from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.conf import settings


# cancella l'immagine di profilo su disco quando il profilo o l'utente viene eliminato se è diverso da default.jpg

# @receiver(post_delete, sender=get_user_model())
# def post_save_image(sender, instance, *args, **kwargs):
#     """ Clean Old Image file"""
#     try:
#         if(str(instance.image) != "default.jpg"):
#             instance.image.delete(save=False)
#     except:
#         pass

# cancella l'immagine precedente di profilo da disco quando viene cambiata se è diversa da default.jpg

# @receiver(pre_save, sender=get_user_model())
# def pre_save_image(sender, instance, *args, **kwargs):
#     """ instance old image file will delete from os """
#     try:
#         old_img = instance.__class__.objects.get(id=instance.id).image.path
#         try:
#             new_img = instance.image.path
#         except:
#             new_img = None

#         print("new_img",new_img)
#         print("old_img",old_img)

#         if str(new_img) != str(old_img):
#             import os
#             if os.path.exists(old_img):
#                 if(old_img != '/backend/media/default.jpg'):
#                     os.remove(old_img)
#     except:
#         pass


# @receiver(post_save, sender=get_user_model())
# def post_save_image(sender, instance, *args, **kwargs):
#     """ set default image after delete user image """
#     try:
#         # se il codice sotto dà errore(ValueError) significa che l'immagine è stata cancellata
#         old_img = instance.__class__.objects.get(id=instance.id).image.path
#     except ValueError:
#         try:
#             # assegna l'immagine di default al user che ha cancellato l'immagine personale
#             user = get_user_model().objects.get(id=instance.id)
#             user.image = 'default.jpg'  # path riferito a setting.MEDIA_ROOT
#             user.save()

  
#         except BaseException as err:
#             print("POST_SAVE ERROR")
#             print(type(err))
#             print(err)