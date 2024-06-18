from agora_logging import logger
from agora_redis_client import redis as Redis
from enum import Enum

class RedisPattern(Enum):
    DESIRED = "desired"
    REPORTED = "reported" 
    
class CallbackResponse():
        def __init__(self, tp_id, key, value):
            self.tp_id = tp_id
            self.key = key
            self.value = value
    
class TwinPropertyObserver:
            
    def __init__(self,tp_id : str, property_name:str = None): 
        self.tp_id = tp_id
        if property_name is None:
            self.property_name = "*"
        else:
            self.property_name = property_name
        self.pattern = f"twin_properties/{self.tp_id}/desired/{self.property_name}"
        self.app_callback = None
    
    def attach(self,app_callback):
        self.app_callback = app_callback        
    
    def remove(self):
        self.app_callback = None
        
    def subscription_callback(self, msg):
        """
        Subscription callback that is called by the Redis pubsub on any event notification
        """
        try:
            channel = msg["channel"]
            keys = channel.split(":")
            prop_value = Redis.get(keys[1])
            logger.debug(f"Desired Key : {keys[1]}, value : {prop_value}")
            prop = str(keys[1]).split(sep="/")
            prop_name_value = str(keys[1]).split(sep=f"/{RedisPattern.DESIRED.value}/")
            tp_group_id= prop[1]
            prop_name =  prop_name_value[1].rstrip("/") if len(prop_name_value) > 0 else ''
            if prop_name is None: raise ValueError("Property Name is not set")

            if prop_value is None: raise ValueError("Property value is not set")

            robj =  CallbackResponse(
                tp_id= self.tp_id,
                key= prop_name,
                value= prop_value
            )            
            if self.app_callback is not None: self.app_callback(robj)

        except Exception as ex:
            logger.exception(ex, "Exception while executing callback method")
        return None