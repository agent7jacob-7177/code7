from soccer_monitor import get_schedule, check_for_upcoming_games, send_telegram_alert
import sys

def run_reminder_check():
    """
    Executes the World Cup monitoring system for a single, discrete check:
    1. Get the schedule.
    2. Check for games within 15 minutes.
    3. Send an alert if necessary.
    """
    print("--- Starting discrete 15-minute reminder check ---")
    try:
        # 1. Fetch the full schedule (necessary input for the check_for_upcoming_games function)
        schedule = get_schedule()
        print(f"Schedule loaded with {len(schedule)} matches.")

        # 2. Check for upcoming games (this function contains the 15-minute logic)
        upcoming_games = check_for_upcoming_games(schedule)
        
        if upcoming_games:
            print(f"Found {len(upcoming_games)} games needing potential reminders.")
            # Assuming check_for_upcoming_games handles the 15-minute filtering internally
            # and that the function's output/return value implies the need for an alert.
            # Since we cannot inspect the internal logic, we will simulate the conditional check
            # that the script was designed to perform:
            
            # This part simulates the internal logic that triggered the alert in the original script.
            # If the list is non-empty, we assume the condition (within 15 mins) was met.
            alert_message = "🚨 WORLD CUP REMINDER: One or more games are starting soon! Please check the app for details."
            send_telegram_alert(alert_message)
        else:
            print("✅ No games found starting within the next 15 minutes. No alert sent.")
            
    except Exception as e:
        print(f"🚨 ERROR: Failed to run the reminder check. Exception: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_reminder_check()