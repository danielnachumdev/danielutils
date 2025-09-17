import logging
from ..better_builtins.counter import Counter
from ..logging_.utils import get_logger

logger = get_logger(__name__)


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
        logger.info(f"Creating InstanceCacheMeta class: {name}")
        
        INIT = "__init__"
        instance_2_id: dict = {}
        id_2_instance: dict = {}
        counter = Counter()
        original_init = None
        if INIT in namespace:
            original_init = namespace[INIT]

        def new_init(*args, **kwargs):
            instance_id = counter.get()
            instance = args[0]
            id_2_instance[instance_id] = instance
            instance_2_id[instance] = instance_id
            counter.increment()
            if original_init:
                original_init(*args, **kwargs)

        def get_id(instance):
            if instance not in instance_2_id:
                logger.warning(f"Instance {instance} not found in cache")
                raise KeyError(f"Instance {instance} not found in cache")
            return instance_2_id[instance]

        def get_instance(id_: int):
            if id_ not in id_2_instance:
                logger.warning(f"Instance with ID {id_} not found in cache")
                raise KeyError(f"Instance with ID {id_} not found in cache")
            return id_2_instance[id_]

        def instances():
            return instance_2_id.keys()

        namespace["instances"] = staticmethod(instances)
        namespace["get_id"] = staticmethod(get_id)
        namespace["get_instance"] = staticmethod(get_instance)
        namespace[INIT] = new_init

        logger.info(f"InstanceCacheMeta: {name} created with instance caching enabled")
        return super().__new__(mcs, name, bases, namespace)
__all__ =[
    "InstanceCacheMeta"
]