import json
from datetime import datetime
from typing import Dict, Any, Optional
from config.settings import settings


class AnalyticsService:
    """
    Service to track usage analytics without storing PII
    """
    
    def __init__(self):
        self.analytics_file = "analytics.json"
        
        # Initialize analytics file if it doesn't exist
        try:
            with open(self.analytics_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {
                "total_queries": 0,
                "daily_stats": {},
                "top_queries": {},
                "error_count": 0
            }
    
    def track_query(self, query: str, response_length: int, success: bool = True):
        """
        Track a query without storing the actual content
        """
        try:
            # Update total count
            self.data["total_queries"] += 1
            
            # Update daily stats
            today = datetime.utcnow().date().isoformat()
            if today not in self.data["daily_stats"]:
                self.data["daily_stats"][today] = {
                    "queries": 0,
                    "successful_queries": 0,
                    "failed_queries": 0,
                    "total_response_length": 0
                }
            
            self.data["daily_stats"][today]["queries"] += 1
            if success:
                self.data["daily_stats"][today]["successful_queries"] += 1
            else:
                self.data["daily_stats"][today]["failed_queries"] += 1
                self.data["error_count"] += 1
                
            self.data["daily_stats"][today]["total_response_length"] += response_length

            # Update top query patterns (without storing the actual query)
            # Just tracking length and some characteristics
            query_length = len(query)
            if query_length < 10:
                query_category = "very_short"
            elif query_length < 50:
                query_category = "short"
            elif query_length < 100:
                query_category = "medium"
            else:
                query_category = "long"
                
            if query_category not in self.data["top_queries"]:
                self.data["top_queries"][query_category] = 0
            self.data["top_queries"][query_category] += 1

            # Save to file
            with open(self.analytics_file, 'w') as f:
                json.dump(self.data, f)
                
        except Exception as e:
            # Don't let analytics errors affect the main application
            print(f"Error tracking analytics: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get current analytics stats
        """
        return self.data

    def track_error(self):
        """
        Track an error occurrence
        """
        try:
            self.data["error_count"] += 1
            
            # Save to file
            with open(self.analytics_file, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Error tracking error: {e}")