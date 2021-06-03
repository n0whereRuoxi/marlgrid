import uuid
class Chronicle:
    def __init__(self):
        self.temporal_actions = []
        self.supported_temporal_assertions = []
        self.temporal_assertions = []
        self.init_time_id = uuid.uuid1()
        
