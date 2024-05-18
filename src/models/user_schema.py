from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    try:
        username = fields.String(required=True, validate=validate.Length(min=1))
        password = fields.String(required=True, validate=validate.Length(min=8, max=16))
        created_at = fields.DateTime(dump_only=True)
        updated_at = fields.DateTime(dump_only=True)
    except Exception as e:
        print(e)


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
