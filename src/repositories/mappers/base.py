class DataMapper:
    db_model = None
    schema = None

    @classmethod
    def mapper_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def mappet_to_persistence(cls, data):
        return cls.db_model(**data.model_dump())
