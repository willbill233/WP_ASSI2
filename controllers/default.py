# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    rows = db((db.auth_user.id == db.blog_post.user_id)).select(limitby=(0,4),orderby=~(db.blog_post.time_stamp))
    postcount = 0
    return locals()

def hasRecords(tableCountQuery):
    if db(tableCountQuery).count() > 0:
        return True
    else:
        return False

def viewproducts():
    countQuery = (db.products.id > 0)
    noOfPages = getNoOfPages(db(countQuery).count())
    rows = db(db.products).select(limitby=((request.args(0, cast=int) * 2) - 2, request.args(0, cast=int) * 2))
    pageIncrement = getPageIncrement(0)
    remainder = getPageRemainder(noOfPages, pageIncrement, 0)
    
    if hasRecords(countQuery):
        showPagination = True
    else:
        showPagination = False
    return locals()

def getNoOfPages(noOfRecords):
    if noOfRecords % 2 == 0 :
        return noOfRecords / 2
    else:
        noOfRecords += 1
        return noOfRecords / 2

def getPageIncrement(argPos):
    if (request.args(argPos, cast=int) >= 5):
        if (request.args(argPos, cast=int) % 5 == 0):
            return  request.args(argPos, cast=int)
        else:
            return request.args(argPos, cast=int) - (request.args(argPos, cast=int) % 5)
    else:
        return  1

def getPageRemainder(noOfPages, pageIncrement, argPos):
    lastIncrement = noOfPages - noOfPages % 5
    if request.args(argPos, cast=int) >= lastIncrement:
        return pageIncrement + noOfPages % 5

    else:
        return pageIncrement + 5



def manageproducts():
    grid = SQLFORM.grid(db.products,maxtextlength=100, paginate=10)
    return locals()

## handles posting product reviews
def product():
    if auth.is_logged_in():
        ## define what fields are presented and their default values where applicable - should be refactored to another function where we define our own validation messages
        db.blog_post.time_stamp.default = request.now
        db.blog_post.time_stamp.writable = False
        db.blog_post.time_stamp.readable = False
        db.blog_post.user_id.writable = False
        db.blog_post.user_id.readable = False
        db.blog_post.user_id.default = auth.user_id
        db.blog_post.product.default = request.args(0)
        db.blog_post.product.readable = False
        db.blog_post.product.writable = False
        db.blog_post.username.default = auth.user.first_name + " " + auth.user.last_name
        db.blog_post.username.readable = False
        db.blog_post.username.writable = False
        #db.blog_post.product.requires = IS_IN_DB(db,db.products.id,'%(product)s') This should ensure that the args for product_id should be in the DB but this doesnt work sad face - Ben
        form = SQLFORM(db.blog_post).process()
        if form.accepted:
            redirect(URL('product/'+request.args(0)+'/1'))
            auth.user.postcount += 1
        elif form.errors: response.flash = 'An error has occured.' #Can somebody find a way to test this? I cant generate any errors - Ben
    else: form=auth.login()
    post = db.products(request.args(0))
    countQuery = (db.blog_post.id > 0) & (db.blog_post.product==request.args(0))
    noOfPages = getNoOfPages(db(countQuery).count())
    rows = db((db.blog_post.product==request.args(0)) & (db.auth_user.id == db.blog_post.user_id)).select(limitby=((request.args(1, cast=int) * 2) - 2, request.args(1, cast=int) * 2))
    pageIncrement = getPageIncrement(1)
    remainder = getPageRemainder(noOfPages, pageIncrement, 1)
    postcount='0'
    
    if hasRecords(countQuery):
        showPagination = True
    else:
        showPagination = False
    return locals()

def addproduct():
    form = SQLFORM(db.products).process()
    if form.accepted: redirect(URL('viewproducts'))
    return locals()





@auth.requires_login()
def create():
    db.blog_post.time_stamp.default = request.now
    db.blog_post.time_stamp.writable = False
    db.blog_post.time_stamp.readable = False
    db.blog_post.product.default = request.args(0)
    db.blog_post.product.readable = False
    db.blog_post.product.writable = False
    db.blog_post.username.default = auth.user.first_name
    db.blog_post.username.readable = False
    db.blog_post.username.writable = False
    #db.blog_post.product.requires = IS_IN_DB(db,db.products.id,'%(product)s') This should ensure that the args for product_id should be in the DB but this doesnt work sad face - Ben
    form = SQLFORM(db.blog_post).process()
    if form.accepted: redirect(URL('product/'+request.args(0)))
    elif form.errors: response.flash = 'An error has occured.' #Can somebody find a way to test this? I cant generate any errors - Ben
    return locals()

def showreview():
    post = db.blog_post(request.args(0,cast=int))
    return locals()


@auth.requires_membership('Manager')
def management():
    grid = SQLFORM.grid(db.blog_post)
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    db.auth_user.postcount.writable = False
    db.auth_user.postcount.readable = False
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
