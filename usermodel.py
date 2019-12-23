# from aiohttp import web
# import json
# from bson import json_util
# import graphene
# from graphene.relay import Node
# from graphene import relay
# import model as UserModel
# from graphene_mongo.fields import MongoengineConnectionField
# from mongoengine import  connect
# from graphene_mongo import MongoengineObjectType
#
# async def mongo(request):
#    connect('creaxt', host='127.0.0.1', port=27017)
#
#
#    class Users(MongoengineObjectType):
#            class Meta:
#                model = UserModel.User
#                # interfaces = (Node,)
#    class User(MongoengineObjectType):
#            class Meta:
#                model = UserModel.User
#                interfaces = (Node,)
#
#
#
#    class Activity(MongoengineObjectType):
#        class Meta:
#            model = UserModel.Activity
#            # interfaces = (Node,)
#    class Query(graphene.ObjectType):
#            node = Node.Field()
#            ur = MongoengineConnectionField(User)
#            user = MongoengineConnectionField(User)
#            alluser = graphene.List(Users)
#            users = graphene.List(Users,types=graphene.String(),ids=graphene.String())
#            singleuser = graphene.List(Users, ids=graphene.String())
#            # activity = graphene.List(Activity)
#            def resolve_users(self, info,types,ids):
#                objects = UserModel.User.objects.filter(type=types,uid=ids)
#                # objects = objects.filter(UserModel.activity.cid==ids)
#                return objects
#            def resolve_singleuser(self, info, ids):
#                objects = UserModel.User.objects.filter(mobile=ids)
#                return objects
#            # def resolve_activity(self, info):
#            #     objects = UserModel.Activity.objects.all()
#            #     # objects = objects.filter(UserModel.activity.cid==ids)
#            #     return objects
#            def resolve_alluser(self, info):
#                objects = list(UserModel.User.objects.all())
#                # objects = objects.filter(UserModel.activity.cid==ids)
#                return objects
#    schema = graphene.Schema(query=Query,types=[Users])
#    query = request.query['query']
#    # query = '''query
#    # {
#    #     users(first: 10,type:"guardian")
#    #     {
#    #
#    #
#    #           edges { node {  name } }
#    #
#    #     }
#    # }'''
#    res = query
#    print(res)
#    result = schema.execute(res)
#    return web.Response(text=json.dumps(result.data),status=200)
# app = web.Application()
# app.router.add_get('/mongo',mongo)
# web.run_app(app)