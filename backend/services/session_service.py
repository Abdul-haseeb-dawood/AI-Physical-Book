import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from models.user_session import UserSession


class SessionService:
    """
    Service to manage user sessions (for anonymous users)
    """
    
    def __init__(self, session_timeout_minutes: int = 30):
        self.sessions: Dict[str, UserSession] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self, user_id: Optional[str] = None) -> UserSession:
        """
        Create a new user session
        """
        session_id = str(uuid.uuid4())
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            created_timestamp=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            active_status=True
        )
        
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[UserSession]:
        """
        Get a session by ID, checking if it's still active
        """
        session = self.sessions.get(session_id)
        if session:
            # Check if session is still active (not expired)
            if datetime.utcnow() - session.last_activity > self.session_timeout:
                self.end_session(session_id)
                return None
            return session
        return None
    
    def update_session_activity(self, session_id: str) -> bool:
        """
        Update the last activity timestamp for a session
        """
        session = self.get_session(session_id)
        if session:
            session.last_activity = datetime.utcnow()
            return True
        return False
    
    def end_session(self, session_id: str) -> bool:
        """
        End a session (remove from active sessions)
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """
        Remove all expired sessions
        """
        expired_sessions = []
        now = datetime.utcnow()
        
        for session_id, session in self.sessions.items():
            if now - session.last_activity > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]