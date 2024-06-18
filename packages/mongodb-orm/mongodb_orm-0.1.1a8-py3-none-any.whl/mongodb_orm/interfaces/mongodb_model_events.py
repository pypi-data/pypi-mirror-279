class MongoDBModelEvents:
    """
        Preventing direct Instantiation of this class
    """

    def __new__(cls, *args, **kwargs):
        if cls is MongoDBModelEvents:
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls)

    def on_save(self, record: dict) -> None:
        # Callback Event when new record added
        pass

    def on_update(self, old_record: dict, new_record: dict) -> None:
        # Callback Event when a record get updated
        pass

    def on_partial_update(self, to_update_record: dict, new_record: dict) -> None:
        # Callback Event when a record get partially updated
        pass

    def on_delete(self, deleted_record: dict) -> None:
        # Callback Event when a record get deleted
        pass

    def on_pre_save(self, record: dict) -> dict:
        # Callback Event before new record being added
        return record

    def on_pre_update(self, record: dict) -> dict:
        # Callback Event before a record being updated
        return record

    def on_pre_partial_update(self, record: dict) -> dict:
        # Callback Event before a record being updated
        return record

    def on_pre_delete(self, record: dict) -> dict:
        # Callback Event before a record being deleted
        return record
