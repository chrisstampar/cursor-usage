import rumps
import sqlite3
import json
import os
import urllib.request
import urllib.parse
import urllib.error
import ssl
from datetime import datetime

class CursorUsageApp(rumps.App):
    def __init__(self):
        super(CursorUsageApp, self).__init__("--%", icon=None)
        
        self.menu_renewal = rumps.MenuItem("Renews in: -- days", callback=self.do_nothing)
        self.menu_total = rumps.MenuItem("Total: --%", callback=self.do_nothing)
        self.menu_auto = rumps.MenuItem("Auto: --%", callback=self.do_nothing)
        self.menu_api = rumps.MenuItem("API: --%", callback=self.do_nothing)
        self.menu_ondemand = rumps.MenuItem("On Demand: $--", callback=self.do_nothing)
        
        self.menu = [
            self.menu_renewal,
            rumps.separator,
            self.menu_total,
            self.menu_auto,
            self.menu_api,
            self.menu_ondemand,
            rumps.separator,
            rumps.MenuItem("Refresh", callback=self.manual_refresh),
            rumps.separator,
            rumps.MenuItem("Quit", callback=rumps.quit_application)
        ]
        
        # Don't show the default quit button since we added our own with a separator
        self.quit_button = None
        
        # Fetch initial usage immediately on startup
        self.refresh_usage(None)

    def do_nothing(self, _):
        # Dummy callback to make the menu items clickable/enabled
        # This prevents macOS from rendering them as greyed out (opaque/dim)
        pass

    def manual_refresh(self, _):
        self.refresh_usage(_)

    @rumps.timer(300)
    def timer_refresh(self, _):
        self.refresh_usage(_)

    def get_session_token(self):
        """Extracts the cursorAuth/accessToken from the local SQLite DB."""
        db_path = os.path.expanduser('~/Library/Application Support/Cursor/User/globalStorage/state.vscdb')
        if not os.path.exists(db_path):
            raise FileNotFoundError("state.vscdb not found.")

        # Convert path to URI format to properly handle spaces and use read-only mode
        db_uri = urllib.parse.quote(db_path)
        conn = sqlite3.connect(f'file:{db_uri}?mode=ro', uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM ItemTable WHERE key = 'cursorAuth/accessToken'")
        token_row = cursor.fetchone()
        conn.close()
        
        if not token_row:
            raise ValueError("Token missing from DB.")
            
        return token_row[0]

    def fetch_api_data(self, token):
        """Makes the RPC request to Cursor's DashboardService."""
        url = 'https://api2.cursor.sh/aiserver.v1.DashboardService/GetCurrentPeriodUsage'
        req = urllib.request.Request(url, data=b'{}', headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Connect-Protocol-Version': '1',
            'User-Agent': 'CursorUsageApp/1.0'
        })
        
        # Strict SSL/TLS verification is enabled by default in create_default_context().
        ctx = ssl.create_default_context()

        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            return json.loads(response.read().decode())

    def update_ui(self, data):
        """Updates the menu bar UI with the parsed JSON data."""
        plan = data.get('planUsage', {})
        spend = data.get('spendLimitUsage', {})
        
        total_pct = plan.get('totalPercentUsed', 0)
        auto_pct = plan.get('autoPercentUsed', 0)
        api_pct = plan.get('apiPercentUsed', 0)
        
        limit = spend.get('individualLimit', 0)
        remaining = spend.get('individualRemaining', 0)
        on_demand_cents = limit - remaining
        on_demand_dollars = on_demand_cents / 100.0
        
        billing_end_ms = data.get('billingCycleEnd')
        if billing_end_ms:
            # billingCycleEnd comes back as a string timestamp in ms, e.g., "1777962382000"
            end_date = datetime.fromtimestamp(int(billing_end_ms) / 1000.0)
            now = datetime.now()
            delta = end_date - now
            days_left = delta.days
            date_str = end_date.strftime("%b %d")
            
            if days_left < 0:
                self.menu_renewal.title = f"Renews: {date_str} (Past due)"
            elif days_left == 0:
                self.menu_renewal.title = f"Renews: Today!"
            elif days_left == 1:
                self.menu_renewal.title = f"Renews: Tomorrow"
            else:
                self.menu_renewal.title = f"Renews: {date_str} ({days_left} days)"
        else:
            self.menu_renewal.title = "Renews: Unknown"
        
        # Use round() for a more accurate representation in the title
        self.title = f"{round(total_pct)}%"
        self.menu_total.title = f"Total: {total_pct:.1f}%"
        self.menu_auto.title = f"Auto: {auto_pct:.1f}%"
        self.menu_api.title = f"API: {api_pct:.1f}%"
        self.menu_ondemand.title = f"On Demand: ${on_demand_dollars:.2f}"

    def refresh_usage(self, _):
        """Coordinates fetching the token, querying the API, and updating the UI."""
        try:
            token = self.get_session_token()
            data = self.fetch_api_data(token)
            self.update_ui(data)
            
        except FileNotFoundError:
            self.title = "No DB"
            print("Database Error: state.vscdb not found.")
        except ValueError:
            self.title = "No Token"
            print("Database Error: Token not found in DB.")
        except sqlite3.Error as e:
            self.title = "DB Error"
            print(f"Database Error: Failed to read state.vscdb")
        except urllib.error.HTTPError as e:
            self.title = "API Err"
            print(f"API HTTP Error: {e.code}")
        except urllib.error.URLError as e:
            self.title = "Net Err"
            print(f"Network Error: {getattr(e, 'reason', 'Unknown reason')}")
        except json.JSONDecodeError:
            self.title = "JSON Err"
            print("API Error: Failed to decode JSON response.")
        except Exception as e:
            self.title = "Error"
            print(f"Unexpected error occurred of type: {type(e).__name__}")

if __name__ == "__main__":
    CursorUsageApp().run()