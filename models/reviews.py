# -*- coding: utf-8 -*-

db.define_table('blog_post',
                Field('product',db.products),
                Field('title',requires=IS_NOT_EMPTY()),
                Field('body','text',requires=IS_NOT_EMPTY()),
                Field('time_stamp','datetime'),
                Field('username',requires=IS_NOT_EMPTY()),
                Field('user_id', db.auth_user))
               # Field('profilepicture','upload',requires=IS_IMAGE(maxsize=(80, 80), minsize=(80, 80))))
