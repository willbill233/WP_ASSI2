# -*- coding: utf-8 -*-

db.define_table('products',
                Field('name',requires=IS_NOT_EMPTY()),
                Field('image','upload'),
                Field('category',requires=IS_IN_SET(['Munchkin','Maine Coon','Scottish Fold','Persian','Somali Cat','Birman','Siberian Cat','Tortoise Shell','Birmilla','Russian Blue'])),
                Field('description','text',requires=IS_NOT_EMPTY()),
                Field('price','integer',requires=IS_NOT_EMPTY()),
                Field('stock','integer',requires=IS_NOT_EMPTY()))
