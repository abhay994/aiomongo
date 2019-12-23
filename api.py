import json
import graphene
import model as UserModel
from mongoengine import connect
from graphene_mongo import MongoengineObjectType
from aiohttp import web
import pymongo
import bson.json_util  as json_util
from bson.objectid import ObjectId
import aiohttp_cors
import socketio
from collections import OrderedDict
sio = socketio.AsyncServer(async_mode='aiohttp',cors_allowed_origins='*')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["creaxt"]


# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)





async def mongo(request):


    class Query(graphene.ObjectType):

        allusers = graphene.JSONString()
        getuser = graphene.JSONString(usertype = graphene.String(),schoolId=graphene.String())
        allactivity = graphene.JSONString()
        activity = graphene.JSONString(CID = graphene.String(),activitytype = graphene.String())
        userMobileNo =   graphene.JSONString(mobileNo = graphene.String())
        parentPhoneNo = graphene.JSONString(mobileNo = graphene.String())




        def resolve_allusers(self, info):
            mycol = mydb['user']  # Collection name
            mydoc = list(mycol.find())  # add all data in a List
            response_obj = json.loads(json_util.dumps(mydoc))
            print(response_obj)
            return response_obj

        def resolve_allactivity(self, info):

            # Database Name
            mycol = mydb['activity']  # Collection name
            mydoc = list(mycol.find())  # add all data in a List
            # convert list into json
            response_obj = json.loads(json_util.dumps(mydoc))
            return response_obj

        def resolve_getuser(self, info,usertype,schoolId):
            print(usertype)
            print(schoolId)

            # Database Name
            mycol = mydb['user']  # Collection name
            if usertype and schoolId  :
                qry = {'$and':[ {"type":usertype.strip()},{"schoolId":schoolId.strip() }]}

            elif  usertype:
                qry = {"type": usertype.strip()}

            elif schoolId:
                qry = {"schoolId":schoolId.strip()}



             # add all data in a List
            # convert list into json
            mydoc = list(mycol.find(qry))
            response_obj = json.loads(json_util.dumps(mydoc))
            return response_obj

        def resolve_userMobileNo(self, info,mobileNo):


            mycol = mydb['user']
            qry ={"mobile":mobileNo.strip()}
            mydoc = list(mycol.find(qry))
            response_obj = json.loads(json_util.dumps(mydoc))
            return response_obj


        def resolve_parentPhoneNo(self, info, mobileNo):


            mycol = mydb['user']
            qry = {"phoneIndex": mobileNo.strip()}
            mydoc = list(mycol.find(qry))
            response_obj = json.loads(json_util.dumps(mydoc))
            return response_obj








    schema = graphene.Schema(query=Query)
    query = request.query['query']
    # query {
    #        users{
    #        firstName
    #        lastName
    #
    #        payment{
    #        type
    #        }
    #
    #             }
    #
    #
    # }
    # '''
    result = schema.execute(query)
    print(result.data)

    return web.Response(text=json.dumps(result.data).replace('\\',"").replace('"[',"[").replace(']"',"]"), status=200)




def convId(jsn):
    id = ObjectId()

    if jsn['type']!='principal':
        conv_id = {**jsn, **{"_id": id }}
        return  conv_id
    else:
        conv_id = {**jsn, **{"_id": id,"schoolID":jsn['UID']}}
        return conv_id


def insertUser(jsn,col):

    mycol = mydb[col] # Database Name
    data = convId(jsn)
    x =  mycol.insert_one(data)
    print('user created'+str(x.inserted_id))
    return x



def insertActivty(jsn,col):

    print("activity")
    mycol = mydb[col]
    data = convId(jsn)
    x = mycol.insert_one(data)
    print('activity created' + str(x.inserted_id))
    return x



async def create(request):
    try:
        collection = request.match_info.get('collection', "Anonymous")

        j = await request.json()

        if collection == 'user':
           print('creating user')
           x =  insertUser(j,collection)
        else:
           print('creating activity')
           x =  insertActivty(j,collection)

        response_obj = {'status': 'success',"_id":str(x.inserted_id)}
        await sio.emit(j['CID'],j )
        return web.Response(text=json.dumps(response_obj), status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        web.Response(text=json.dumps(response_obj), status=500)




# @sio.on('message')
# async def print_message(sid, message):
#     # When we receive a new event of type
#     # 'message' through a socket.io connection
#     # we print the socket ID and the message
#     print("Socket ID: " , sid)
#     print(message)
#     await sio.emit('message', message)





cors = aiohttp_cors.setup(app)

rcreate=  cors.add(app.router.add_resource('/create/{collection}'))
rqry=  cors.add(app.router.add_resource('/mongo'))
routecreate = cors.add(
    rcreate.add_route("POST", create), {
       "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })


routeqry = cors.add(
    rqry.add_route("GET", mongo), {
       "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })



# web.run_app(app)

if __name__ == '__main__':
    web.run_app(app)