from mongoengine import (
    BooleanField,
    Document,
    DynamicDocument,
    EmailField,
    ListField,
    StringField,
    ValidationError,
)


class User(DynamicDocument):
    firstName = StringField(max_length=40, required=True)
    lastName = StringField(max_length=40, required=True)
    email = EmailField(required=True)
    password = StringField()
    userType = StringField(max_length=40, required=True)
    organization = StringField(required=False)
    location = StringField(required=False)
    isAdmin = BooleanField(default=False)
    recentDatasets = (ListField(default=[]),)
    resetId = StringField(default="")
    confirmationId = StringField(default="")
    isConfirmed = BooleanField(default=False)

    def getFullname(self):
        return self.firstName + " " + self.lastName

    meta = {"indexes": [{"fields": ["$firstName", "$lastName"]}]}
