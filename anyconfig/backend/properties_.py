#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
from anyconfig.compat import StringIO, iteritems
from anyconfig.globals import LOGGER as logging

import anyconfig.backend.base as Base
import sys

import pyjavaproperties


SUPPORTED = True


def load_impl(config_fp, container):
    p = pyjavaproperties.Properties()
    p.load(config_fp)

    return container(p.getPropertyDict())

def dump_impl(data, config_fp):
    """TODO: How to encode nested dicts?
    """
    p = pyjavaproperties.Properties()
    for k, v in iteritems(data):
        p.setProperty(k, v)

    p.store(config_fp)


class PropertiesParser(Base.ConfigParser):

    _type = "properties"
    _extensions = ["properties"]
    _supported = SUPPORTED

    # FIXME:
    #@classmethod
    #def loads(cls, config_content, *args, **kwargs):
    #    config_fp = StringIO(config_content)
    #    return load_impl(config_fp, cls.container())

    @classmethod
    def load(cls, config_path, **kwargs):
        return load_impl(open(config_path), cls.container())

    @classmethod
    def dumps(cls, data, **kwargs):
        config_fp = StringIO()
        dump_impl(data, config_fp)
        return config_fp.getvalue()

    @classmethod
    def dump(cls, data, config_path, **kwargs):
        """TODO: How to encode nested dicts?
        """
        Base.mk_dump_dir_if_not_exist(config_path)
        dump_impl(data, open(config_path, 'w'))


# vim:sw=4:ts=4:et:
