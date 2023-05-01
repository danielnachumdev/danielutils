from ..Classes import Counter


class InstanceCacheMeta(type):
    """Adds automatic caching of all instances of the class

        Adds the following API to the class
        @staticmethod
        instances() -> returns a generator of all of the instances

        @staticmethod
        get_id(instance) -> returns the id of the instance

        @staticmethod
        get_instance(id) -> return the id of an instance

    """
    def __new__(mcs, name, bases, namespace):
        INIT = "__init__"
        instance_2_id = dict()
        id_2_instance = dict()
        counter = Counter()
        original_init = None
        if INIT in namespace:
            original_init = namespace[INIT]

        def new_init(*args, **kwargs):
            id_2_instance[counter.get()] = args[0]
            instance_2_id[args[0]] = counter.get()
            counter.increment()
            if original_init:
                original_init(*args, **kwargs)

        @staticmethod
        def get_id(instance):
            yield from instance_2_id[instance]

        @staticmethod
        def get_instance(id):
            return id_2_instance[id]

        @staticmethod
        def instances():
            return instance_2_id.keys()

        namespace["instances"] = instances
        namespace["get_id"] = get_id
        namespace["get_instance"] = get_instance
        namespace[INIT] = new_init

        return super().__new__(mcs, name, bases, namespace)
