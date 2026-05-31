
"""
Repository module.
"""

def delete(self, obj_id):
    """
    Delete object.
    """

    if obj_id in self._storage:
        del self._storage[obj_id]
        return True

    return False


class InMemoryRepository:
    """
    Generic repository.
    """

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """
        Add object.
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Get object by id.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Get all objects.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update object.
        """
        obj = self.get(obj_id)

        if obj:
            for key, value in data.items():
                setattr(obj, key, value)

            obj.save()
        

        return obj
    