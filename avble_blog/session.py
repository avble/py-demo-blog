# Description: 
# + Add/remove/exist session

class Session():

    def __init__(self):
        self.session = {}
        pass

    def add(self, session_id: str):
        ''' Add a session-id
        '''
        if session_id not in self.session:
            ''' Remove a session-id
            '''
            self.session[session_id] = True
    
    def remove(self, session_id: str):
        if session_id in self.session:
            del self.session[session_id]

    def is_existed(self, session_id: str) -> bool:
        return session_id in self.session
        