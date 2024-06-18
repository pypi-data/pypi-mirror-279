from itertools import chain
from django.db.models.fields.files import FieldFile
from django.contrib import admin
from django.utils.html import format_html
from ...utils.model import ModelFields


class MetaClass(admin.ModelAdmin.__class__):
    def __new__(mcs, name, bases, attrs):
        new_class = super(MetaClass, mcs).__new__(mcs, name, bases, attrs)
        if new_class.model_cls:
            admin.site.register(new_class.model_cls, new_class)
        return new_class


class ModelAdminAbstract(admin.ModelAdmin, metaclass=MetaClass):
    model_cls = None


class ModelAdminBase(ModelAdminAbstract):
    img_width = 50

    @staticmethod
    def get_url(obj):
        if isinstance(obj, FieldFile):
            return obj.url
        return obj

    @classmethod
    def format_img(cls, img):
        if img:
            img = cls.get_url(img)
            return format_html('<img src="{0}" width="{1}" height="{1}"/>'.format(img, cls.img_width))
        else:
            return ""

    @classmethod
    def format_aimg(cls, img):
        if img:
            img = cls.get_url(img)
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="{1}" height="{1}"/></a>'.
                format(img, cls.img_width))
        else:
            return ""

    @classmethod
    def format_imgs(cls, img_list):
        return format_html("".join([cls.format_img(x) for x in img_list]))

    @classmethod
    def format_aimgs(cls, img_list):
        return format_html("".join([cls.format_aimg(x) for x in img_list]))

    @staticmethod
    def format_tags(tags, ml=None, sep=' '):
        if ml is not None:
            tags = sorted(tags, key=lambda x: len(x))
            r = ""
            for tag in tags:
                temp = ""
                if r:
                    temp += sep
                temp += tag
                if len(r) + len(temp) > ml:
                    return r
                r += temp
            return r
        return sep.join(tags)

    @classmethod
    def format_a(cls, url, text=None, target=None):
        if url:
            url = cls.get_url(url)
            target = target or '_blank'
            if callable(text):
                text = text(url)
            elif text == 0:
                text = url
            elif text is None:
                text = url.rsplit('/', 1)[-1]
            return format_html("<a href='{url}' target='{target}'>{text}</a>", url=url, text=text, target=target)
        return ""


def calc_list_display(model_cls, rewrite_set=None, disable_set=None, rewrite_suffix='_'):
    array = []
    mfs = ModelFields(model_cls)
    for name in chain(mfs.auto.keys(), mfs.common.keys(), mfs.ct.keys(), mfs.o2o.keys(), mfs.o2m.keys()):
        if disable_set and name in disable_set:
            continue
        if rewrite_set and name in rewrite_set:
            name += rewrite_suffix
        array.append(name)
    return tuple(array)


def admin_register(model_cls, list_display=None):
    type(
        'admin',
        (ModelAdminBase,),
        {'model_cls': model_cls, 'list_display': list_display or calc_list_display(model_cls)}
    )


def admin_register_batch(model_cls_list):
    for model_cls in model_cls_list:
        admin_register(model_cls)
