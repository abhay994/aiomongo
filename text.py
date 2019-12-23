from datetime import datetime
import json

from mongoengine import *
from graphene_mongodb import MongoSchema
import graphene


connect('test', host='127.0.0.1', port=27017)  # make sure to your mongodb is running, if isn't, run 'mongod' in terminal

class Posts(Document):
    title = StringField()
    text = StringField()
post1 = Posts(title="Post1", text="LOL")
post2 = Posts(title="Post2", text="HEY JOE")
post1.save()
post2.save()

class Country(Document):
    name = StringField()
    area_code = IntField()

brazil = Country(name="Brazil",
                 area_code=55)

class Bank(Document):
    name = StringField()
    country = ReferenceField(Country)
    location = PointField()

bank = Bank(name="Caixa",
            country=brazil,
            location=[29.977291, 31.132493])


class User(Document):
    username = StringField()
    active = BooleanField()
    age = IntField()
    score = FloatField()
    bank = ReferenceField(Bank)
    posts = ListField(ReferenceField(Posts))
    favorite_colors = ListField(StringField())
    creation_date = DateTimeField()
    site_url = URLField()
    personal_data = DictField()
    email = EmailField()
    super_id = LongField()
    remember_pi = DecimalField(min_value=3.1, max_value=3.15, precision=11)
    ordered_favorite_colors = SortedListField(StringField())
    nickname = BinaryField()


user = User(username="John",
            active=True,
            age=18,
            score=5.5,
            bank=bank,
            posts=[post1, post2],
            favorite_colors=['blue', 'red'],
            creation_date=datetime.now(),
            site_url="https://github.com/joaovitorsilvestre/MongographQL",
            personal_data={"fullName": "John John",
                           "passport": 15874512354,
                           "children_names": ["Ross", "Chandler"]},
            email="John@server.com",
            super_id=9223372036854775807,
            remember_pi=3.14159265359,
            ordered_favorite_colors=['red', 'blue'],
            nickname=b'John armless'
            )

brazil.save()
bank.save()
user.save()


class PostsSchema(MongoSchema):
    model = Posts


class CountrySchema(MongoSchema):
    model = Country


class BankSchema(MongoSchema):
    model = Bank


class UserSchema(MongoSchema):
    model = User


class Query(graphene.ObjectType):
    user = UserSchema.single


schema = graphene.Schema(query=Query)

result = schema.execute("""query Data {
    user(username: "John") {
        id
        username
        active
        age
        score
        bank {
            name
            location
            country {
                name
                areaCode
            }
        }
        posts {
            title
            text
        }
        favoriteColors
        creationDate
        siteUrl
        personalData
        email
        superId
        rememberPi
        orderedFavoriteColors
        nickname
    }
}""")

if not result.errors:
    parsed = {k: dict(v) for k, v in dict(result.data).items()}
    print(json.dumps(parsed, indent=4, sort_keys=True))
else:
    print(errors)

