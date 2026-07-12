#!/usr/bin/env python3
import subprocess
import json
import re
import os
from datetime import datetime

def run_command(cmd):
    """Run a command and return its output as a string."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"Warning: Command '{cmd}' failed with exit code {result.returncode}")
            print(f"stderr: {result.stderr}")
            return None
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"Warning: Command '{cmd}' timed out")
        return None
    except Exception as e:
        print(f"Warning: Command '{cmd}' failed with exception: {e}")
        return None

def get_last_generated_time(report_path):
    """Extract the last generated timestamp from the report."""
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Look for the line that starts with **Generated:**
    match = re.search(r'^\*\*Generated\*\*:\s*(.+)$', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find generated timestamp in report")
    date_str = match.group(1).strip()
    # Try multiple formats
    formats = [
        "%a, %b %d, %Y %I:%M:%S %p",
        "%b %d, %Y %I:%M:%S %p",
        "%a, %b %d, %Y %I:%M %p",
        "%b %d, %Y %I:%M %p"
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt
        except ValueError:
            continue
    raise ValueError(f"Could not parse date string: {date_str}")

def get_profiles():
    """Get a list of profile names."""
    output = run_command("hermes profile list")
    if output is None:
        return []
    lines = output.splitlines()
    profiles = []
    for line in lines:
        if line.strip() == "" or "Profile" in line or "----" in line:
            continue
        parts = re.split(r'\s{2,}', line.strip())
        if parts:
            profiles.append(parts[0])
    return profiles

def get_sessions_for_profile(profile):
    """Get a list of session IDs for a given profile."""
    output = run_command(f'hermes sessions list --profile {profile} --limit 1000')
    if output is None:
        return []
    lines = output.splitlines()
    sessions = []
    for line in lines:
        if line.strip() == "" or "ID" in line or "----" in line:
            continue
        parts = re.split(r'\s{2,}', line.strip())
        if parts:
            sessions.append(parts[0])
    return sessions

def extract_timestamp_from_session_id(session_id):
    """Extract timestamp from session ID format: YYYYMMDD_HHMMSS_<random>."""
    parts = session_id.split('_')
    if len(parts) >= 3:
        date_str = parts[0]  # YYYYMMDD
        time_str = parts[1]  # HHMMSS
        if len(date_str) == 8 and len(time_str) == 6:
            try:
                dt = datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S")
                return dt
            except ValueError:
                pass
    return None

def export_session(session_id, profile):
    """Export a session as JSON."""
    output = run_command(f'hermes sessions export --session-id {session_id} --profile {profile} -o json')
    if output is None:
        return None
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print(f"Warning: Failed to parse JSON for session {session_id} in profile {profile}")
        return None

def format_session_details(session_data):
    """Format session details for the report."""
    if not session_data:
        return None
    session_id = session_data.get('id', 'unknown')
    # Get timestamp from session data or from ID
    ts = session_data.get('updated')
    if ts:
        dt = datetime.fromtimestamp(ts / 1000.0)  # assuming milliseconds
    else:
        dt = extract_timestamp_from_session_id(session_id)
        if dt is None:
            dt = datetime.now()  # fallback
    date_str = dt.strftime("%B %d, %Y at %I:%M %p")
    source = session_data.get('source', 'unknown')
    message_count = len(session_data.get('messages', []))
    # Objective: first user message
    objective = ""
    for msg in session_data.get('messages', []):
        if msg.get('role') == 'user':
            objective = msg.get('content', '')[:200]
            break
    # Key accomplishments: last two assistant messages
    accomplishments = []
    for msg in reversed(session_data.get('messages', [])):
        if msg.get('role') == 'assistant':
            accomplishments.append(msg.get('content', '')[:200])
            if len(accomplishments) >= 2:
                break
    accomplishments = list(reversed(accomplishments))
    return {
        'session_id': session_id,
        'date': date_str,
        'source': source,
        'message_count': message_count,
        'objective': objective,
        'accomplishments': accomplishments
    }

def update_report(report_path, new_sessions):
    """Update the report with new sessions and recalculate statistics."""
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the generated timestamp
    now = datetime.now()
    now_str = now.strftime("%a, %b %d, %Y %I:%M:%S %p")
    content = re.sub(r'^(\*\*Generated\*\*:).+$', r'\1 ' + now_str, content, flags=re.MULTILINE)
    
    # Get all sessions (for statistics)
    profiles = get_profiles()
    all_sessions = set()
    profile_counts = {}
    for profile in profiles:
        sessions = get_sessions_for_profile(profile)
        all_sessions.update(sessions)
        profile_counts[profile] = len(sessions)
    
    total_unique = len(all_sessions)
    
    # Update statistics section
    # Replace the total unique sessions line
    content = re.sub(r'- Total unique sessions across all profiles: \d+', 
                     f'- Total unique sessions across all profiles: {total_unique}', 
                     content)
    # Replace the profile counts in the table
    lines = content.splitlines()
    in_stats = False
    in_table = False
    new_lines = []
    for line in lines:
        if line.startswith("## Statistics"):
            in_stats = True
            new_lines.append(line)
            continue
        if in_stats and line.startswith("## Sessions by Profile"):
            in_table = True
            new_lines.append(line)
            continue
        if in_table and line.startswith("| Profile |"):
            new_lines.append(line)
            new_lines.append("|---------|---------------|")
            for profile in sorted(profile_counts.keys()):
                new_lines.append(f"| {profile} | {profile_counts[profile]} |")
            new_lines.append("")  # blank line after table
            in_table = False
            continue
        if in_stats and line.startswith("## ") and not line.startswith("## Sessions by Profile"):
            in_stats = False
            in_table = False
            new_lines.append(line)
            continue
        if in_stats:
            continue
        new_lines.append(line)
    content = "\n".join(new_lines)
    
    # Update the Update Log section
    update_log_entry = f"- {now.strftime('%Y-%m-%d %H:%M:%S')}: Added {len(new_sessions)} new session(s) since last report."
    if "## Update Log" in content:
        parts = content.split("## Update Log", 1)
        header = parts[0] + "## Update Log"
        rest = parts[1]
        new_content = header + "\n" + update_log_entry + "\n" + rest
    else:
        lines = content.splitlines()
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.startswith("# Hermes Session Master Report"):
                new_lines.append("")
                new_lines.append("## Update Log")
                new_lines.append(update_log_entry)
        new_content = "\n".join(new_lines)
    
    # Update the Recent Sessions (Top 10 by date) section
    sorted_sessions = sorted(new_sessions, key=lambda x: x['date'], reverse=True)
    top_sessions = sorted_sessions[:10]
    table_lines = ["| Session ID | Time | Source | Model | Profile |", 
                   "|------------|------|--------|-------|---------|"]
    for sess in top_sessions:
        model = "unknown"
        profile = "unknown"
        table_lines.append(f"| {sess['session_id']} | {sess['date']} | {sess['source']} | {model} | {profile} |")
    new_table = "\n".join(table_lines)
    lines = new_content.splitlines()
    in_recent = False
    in_table = False
    final_lines = []
    for line in lines:
        if line.startswith("## Recent Sessions (Top 10 by date)"):
            in_recent = True
            final_lines.append(line)
            continue
        if in_recent and line.startswith("| Session ID |"):
            in_table = True
            final_lines.append(line)
            for tl in table_lines[1:]:
                final_lines.append(tl)
            continue
        if in_table and line.strip() == "":
            in_table = False
            final_lines.append(line)
            continue
        if in_table and line.startswith("## "):
            in_table = False
            in_recent = False
            final_lines.append(line)
            continue
        if in_table:
            continue
        if in_recent and line.startswith("## "):
            in_recent = False
            final_lines.append(line)
            continue
        if not in_table:
            final_lines.append(line)
    final_content = "\n".join(final_lines)
    
    return final_content

def main():
    report_path = "/c/Users/Henry/Documents/hermes_session_master_report.md"
    try:
        last_gen_dt = get_last_generated_time(report_path)
    except Exception as e:
        print(f"Error getting last generated time: {e}")
        return 1
    
    print(f"Last generated time: {last_gen_dt}")
    
    profiles = get_profiles()
    print(f"Profiles found: {profiles}")
    
    new_sessions = []
    seen_session_ids = set()
    
    for profile in profiles:
        print(f"Checking profile: {profile}")
        session_ids = get_sessions_for_profile(profile)
        print(f"  Found {len(session_ids)} sessions")
        for session_id in session_ids:
            if session_id in seen_session_ids:
                continue
            seen_session_ids.add(session_id)
            session_dt = extract_timestamp_from_session_id(session_id)
            if session_dt is None:
                session_data = export_session(session_id, profile)
                if session_data:
                    ts = session_data.get('updated')
                    if ts:
                        session_dt = datetime.fromtimestamp(ts / 1000.0)
            if session_dt and session_dt > last_gen_dt:
                print(f"  New session: {session_id} at {session_dt}")
                session_data = export_session(session_id, profile)
                if session_data:
                    details = format_session_details(session_data)
                    if details:
                        new_sessions.append(details)
                else:
                    print(f"  Warning: Could not export session {session_id}")
    
    print(f"Found {len(new_sessions)} new sessions.")
    
    try:
        updated_content = update_report(report_path, new_sessions)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("Report updated successfully.")
        return 0
    except Exception as e:
        print(f"Error updating report: {e}")
        return 1

if __name__ == "__main__":
    exit(main())