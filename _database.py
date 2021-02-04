from peewee import (
    BigIntegerField,
    CharField,
    DateTimeField,
    DecimalField,
    FloatField,
    ForeignKeyField,
    MySQLDatabase,
    Model,
    CompositeKey,
    AutoField,
    SQL,
)

from utils import config_get_params

_name, _host, _port, _user, _password = config_get_params(
    [
        "database_name",
        "database_host",
        "database_port",
        "database_username",
        "database_password",
    ]
)


driver = MySQLDatabase

database = driver(
    _name, host=_host, port=_port, user=_user, password=_password, autorollback=True
)

# * Базовая модель моделей базы данных для наследования драйвера
class BaseModel(Model):
    class Meta:
        database = database
        autorollback = True


# * Модель изделий
class Product(BaseModel):
    name = CharField(max_length=64, primary_key=True,)
    size = CharField(max_length=32)


# * Модель пользователей
class User(BaseModel):
    login = CharField(max_length=16,)
    password = CharField(max_length=32,)
    role = CharField(max_length=32)
    first_name = CharField(max_length=16,)
    last_name = CharField(max_length=16,)
    patronymic = CharField(max_length=16,)
    photo_path = CharField(max_length=64,)

    class Meta:
        primary_key = CompositeKey("login", "password")


# * Модель поставщиков
class Provider(BaseModel):
    name = CharField(max_length=32, primary_key=True)
    adress = CharField(max_length=64)
    delivery_period = DateTimeField()


# * Модель заказов
class Order(BaseModel):
    order_id = BigIntegerField()
    timestamp = DateTimeField()
    name = CharField(max_length=64,)
    product = ForeignKeyField(
        Product, to_field="name", on_delete="CASCADE", on_update="CASCADE"
    )
    user = ForeignKeyField(
        User, to_field="login", on_update="CASCADE", on_delete="CASCADE"
    )
    order_manager = ForeignKeyField(
        User, to_field="login", on_update="CASCADE", on_delete="CASCADE"
    )
    purchase = DecimalField()
    planned_completion_date = DateTimeField()

    class Meta:
        primary_key = CompositeKey("order_id", "timestamp")


# * Типы оборудования
class EquipmentType(BaseModel):
    equipment_type = CharField(max_length=32, primary_key=True)


# * Модель оборудования
class Equipment(BaseModel):
    marking = CharField(max_length=32, primary_key=True)
    equipment_type = ForeignKeyField(
        EquipmentType, on_update="CASCADE", on_delete="CASCADE"
    )
    characteristics = CharField(max_length=128,)


# * Материлы
class Materials(BaseModel):
    vendor_code = CharField(max_length=32, primary_key=True)
    name = CharField(max_length=32)
    unit = CharField(max_length=16)
    amount = BigIntegerField()
    provider = ForeignKeyField(
        Provider, on_delete="CASCADE", on_update="CASCADE", null=True
    )
    photo_path = CharField(max_length=64,)
    material_type = CharField(max_length=32)
    purchase_price = DecimalField()
    gost = CharField(max_length=64,)
    length = CharField(max_length=64,)
    characteristics = CharField(max_length=128,)


# * Фурнитура
class Fittings(BaseModel):
    vendor_code = CharField(max_length=32, primary_key=True)
    name = CharField(max_length=32)
    unit = CharField(max_length=16)
    amount = BigIntegerField()
    provider = ForeignKeyField(
        Provider, on_delete="CASCADE", on_update="CASCADE", null=True
    )
    photo_path = CharField(max_length=64)
    purchase_price = DecimalField()
    accessories_type = CharField(max_length=32)
    weight = DecimalField()


class MaterialsSpecification(BaseModel):
    product = ForeignKeyField(Product)
    material = ForeignKeyField(Materials)
    amount = BigIntegerField()

    class Meta:
        primary_key = CompositeKey("product", "material")


class FittingsSpecification(BaseModel):
    product = ForeignKeyField(Product)
    fitting = ForeignKeyField(Fittings)
    amount = BigIntegerField()

    class Meta:
        primary_key = CompositeKey("product", "fitting")


class AssemblyUnitSpecification(BaseModel):
    product = ForeignKeyField(Product)
    assembly_unit = ForeignKeyField(Product)
    amount = BigIntegerField()

    class Meta:
        primary_key = CompositeKey("product", "assembly_unit")


class OperationSpecification(BaseModel):
    product = ForeignKeyField(Product)
    operation = CharField(max_length=128)
    operation_id = BigIntegerField()
    complete_time = DateTimeField()

    class Meta:
        primary_key = CompositeKey("product", "operation", "operation_id")


# * Инициализация таблиц базы данных
if database:
    Product.create_table(True)
    User.create_table(True)
    Provider.create_table(True)
    Order.create_table(True)
    EquipmentType.create_table(True)
    Equipment.create_table(True)
    Materials.create_table(True)
    Fittings.create_table(True)
    MaterialsSpecification.create_table(True)
    FittingsSpecification.create_table(True)
    AssemblyUnitSpecification.create_table(True)
    OperationSpecification.create_table(True)
