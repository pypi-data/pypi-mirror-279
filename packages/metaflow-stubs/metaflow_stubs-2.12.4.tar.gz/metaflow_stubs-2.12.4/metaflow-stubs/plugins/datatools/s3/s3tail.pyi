##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.4                                                             #
# Generated on 2024-06-18T20:28:20.563390                                        #
##################################################################################

from __future__ import annotations


def aws_retry(f):
    ...

def get_s3_client(s3_role_arn = None, s3_session_vars = None, s3_client_params = None):
    ...

class S3Tail(object, metaclass=type):
    def __init__(self, s3url):
        ...
    def reset_client(self, hard_reset = False):
        ...
    def clone(self, s3url):
        ...
    @property
    def bytes_read(self):
        ...
    @property
    def tail(self):
        ...
    def __iter__(self):
        ...
    def _make_range_request(self, *args, **kwargs):
        ...
    ...

