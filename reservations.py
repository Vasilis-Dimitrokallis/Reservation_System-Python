import numpy as np
import pandas as pd
import os
from datetime import datetime
"""Data Initialization"""
#May=np.zeros((10, 31), dtype=object)
#June = np.zeros((10, 30), dtype=object)
#July = np.zeros((10, 31), dtype=object)
#August = np.zeros((10, 31), dtype=object)
#September = np.zeros((10, 30), dtype=object)
#months = {'June': June, 'July': July, 'August': August, 'September': September}
def save_reservations():
    np.save('May.npy', May)
    np.save('June.npy', June)
    np.save('July.npy', July)
    np.save('August.npy', August)
    np.save('September.npy', September)
def load_reservations():
    global May, June, July, August, September, months
    May = np.load('May.npy', allow_pickle=True)
    June = np.load('June.npy', allow_pickle=True)
    July = np.load('July.npy', allow_pickle=True)
    August = np.load('August.npy', allow_pickle=True)
    September = np.load('September.npy', allow_pickle=True)
    months = {'May': May, 'June': June, 'July': July, 'August': August, 'September': September}
file_names = ['May.npy', 'June.npy', 'July.npy', 'August.npy', 'September.npy']
if not all(os.path.exists(f) for f in file_names):
    May = np.zeros((10, 31), dtype=object)
    June = np.zeros((10, 30), dtype=object)
    July = np.zeros((10, 31), dtype=object)
    August = np.zeros((10, 31), dtype=object)
    September = np.zeros((10, 30), dtype=object)
    np.save('May.npy', May)
    np.save('June.npy', June)
    np.save('July.npy', July)
    np.save('August.npy', August)
    np.save('September.npy', September)
load_reservations()
save_reservations()
"""Availability Functions"""
def is_available(room_number, arrival_date, departure_date):
    arrival_month, arrival_day = arrival_date.split()
    departure_month, departure_day = departure_date.split()
    arrival_day = int(arrival_day) - 1
    departure_day = int(departure_day) - 1
    month_order = ['May', 'June', 'July', 'August', 'September']
    arrival_index = month_order.index(arrival_month)
    departure_index = month_order.index(departure_month)
    if arrival_index == departure_index:
        month = months[arrival_month]
        if np.all(month[room_number-1, arrival_day:departure_day] == 0):
            return True
        else:
            return False
    else:
        for month in month_order[arrival_index:departure_index+1]:
            if month == arrival_month:
                month_array = months[month]
                if np.all(month_array[room_number-1, arrival_day:] == 0):
                    return True
                else:                    return False   
            elif month == departure_month:
                month_array = months[month]
                if np.all(month_array[room_number-1, :departure_day] == 0):
                    return True 
                else:
                    return False
            else:
                month_array = months[month]
                if np.all(month_array[room_number-1, :] == 0):
                    return True
                else:
                    return False

    
def search_availability():
    arrival_date=input("Enter the check-in date (e.g., June 15): ")
    arrival_month, arrival_day = arrival_date.split()
    departure_date=input("Enter the check-out date (e.g., June 20): ")
    departure_month, departure_day = departure_date.split()
    available_rooms = []
    for room_number in range(1, 11):
        if is_available(room_number, arrival_date, departure_date):
            available_rooms.append(room_number)
    if available_rooms:
        print("Available rooms:", available_rooms)
    else:
        print("No rooms available for the selected dates.")

def show_availability():
    month=input("Enter the month to view availability (May, June, July, August, September): ")
    month_array = months[month]
    print(f"Availability for {month}:")
    for room_number in range(10):
        available_days = np.where(month_array[room_number] == 0)[0] + 1
        if available_days.size > 0:
            print(f"Room {room_number + 1}: Available days: {available_days.tolist()}")
        else:
            print(f"Room {room_number + 1}: No available days.")

"""Reservation Functions"""
def reservation(room_number, arrival_date, departure_date, guest_name):
    reservation_info = [str(guest_name), str(arrival_date), str(departure_date)]
    if is_available(room_number, arrival_date, departure_date):
        arrival_month, arrival_day = arrival_date.split()
        departure_month, departure_day = departure_date.split()
        arrival_day = int(arrival_day) - 1
        departure_day = int(departure_day) - 1
        month_order = ['May', 'June', 'July', 'August', 'September']
        arrival_index = month_order.index(arrival_month)
        departure_index = month_order.index(departure_month)
        if arrival_index == departure_index:
            month = months[arrival_month]
            for day in range(arrival_day, departure_day):
                month[room_number-1, day] = reservation_info
        else:
            for month in month_order[arrival_index:departure_index+1]:
                if month == arrival_month:
                    month_array = months[month]
                    for day in range(arrival_day, month_array.shape[1]):
                        month_array[room_number-1, day] = reservation_info

                elif month == departure_month:
                    month_array = months[month]
                    for day in range(0, departure_day):
                         month_array[room_number-1, day] = reservation_info
                else:
                    month_array = months[month]
                    for day in range(month_array.shape[1]):
                        month_array[room_number-1, day] = reservation_info
        print(f"Reservation made for room {room_number} from {arrival_date} to {departure_date}.")
    else:
        print("The selected room is not available for the chosen dates.")
    save_reservations()

def make_reservation():
    room_number=int(input("Enter room number to reserve (1-10): "))
    arrival_date=input("Enter the check-in date (e.g., June 15): ")
    departure_date=input("Enter the check-out date (e.g., June 20): ")
    guest_name=input("Enter guest name: ")
    reservation(room_number, arrival_date, departure_date, guest_name)
    

def find_reservations(room_number, guest_name, dates): 
    # ΠΕΡΙΠΤΩΣΗ 1: Αναζήτηση με Ημερομηνίες (Dates)
    if room_number == 100 and guest_name == "0": 
        dates_split = dates.split(" to ")
        arrival_month = dates_split[0].split()[0]
        arrival_day = int(dates_split[0].split()[1])
        departure_month = dates_split[1].split()[0]
        departure_day = int(dates_split[1].split()[1])
        
        df = pd.DataFrame(columns=["Room Number", "Guest Name", "Arrival Date", "Departure Date"])
        seen_reservations = set() 
        
        check_range_start = arrival_day - 1
        check_range_end = departure_day

        for room in range(1, 11):
            if arrival_month not in months: continue
            current_month_data = months[arrival_month]
            
            for day_index in range(check_range_start, check_range_end):
                if day_index >= current_month_data.shape[1]:
                    break
                
                cell = current_month_data[room-1, day_index]
                
                if isinstance(cell, list) or (isinstance(cell, np.ndarray) and len(cell) > 0):
                    guest = cell[0]
                    r_arrival = cell[1]
                    r_departure = cell[2]
                    
                    unique_key = (room, guest, r_arrival, r_departure)
                    
                    if unique_key not in seen_reservations:
                        seen_reservations.add(unique_key)
                        new_row = pd.DataFrame([{
                            "Room Number": room, 
                            "Guest Name": guest,
                            "Arrival Date": r_arrival,
                            "Departure Date": r_departure
                        }])
                        df = pd.concat([df, new_row], ignore_index=True)
        print(df)
    elif room_number != 100 and guest_name == "0" and dates != "0":
        dates_split = dates.split(" to ")
        arrival_month = dates_split[0].split()[0]
        arrival_day = int(dates_split[0].split()[1])
        departure_month = dates_split[1].split()[0]
        departure_day = int(dates_split[1].split()[1])
        df = pd.DataFrame(columns=["Room Number", "Guest Name", "Arrival Date", "Departure Date"])
        seen_reservations = set() 
        
        check_range_start = arrival_day - 1
        check_range_end = departure_day

        if arrival_month in months:
            current_month_data = months[arrival_month]
            
            for day_index in range(check_range_start, check_range_end):
                if day_index >= current_month_data.shape[1]:
                    break
                
                cell = current_month_data[room_number-1, day_index]
                
                if isinstance(cell, list) or (isinstance(cell, np.ndarray) and len(cell) > 0):
                    guest = cell[0]
                    r_arrival = cell[1]
                    r_departure = cell[2]
                    
                    unique_key = (room_number, guest, r_arrival, r_departure)
                    
                    if unique_key not in seen_reservations:
                        seen_reservations.add(unique_key)
                        new_row = pd.DataFrame([{
                            "Room Number": room_number, 
                            "Guest Name": guest,
                            "Arrival Date": r_arrival,
                            "Departure Date": r_departure
                        }])
                        df = pd.concat([df, new_row], ignore_index=True)
        print(df)
    elif room_number == 100 and dates == "0":
        df = pd.DataFrame(columns=["Room Number", "Guest Name", "Arrival Date", "Departure Date"])
        # Χρησιμοποιούμε set για να μην εμφανίζεται η ίδια κράτηση πολλές φορές
        seen_reservations = set()

        for month in months.keys():
            month_array = months[month]
            rows, cols = month_array.shape
            for day in range(cols):
                for room_idx in range(rows):
                    cell = month_array[room_idx, day]
                    if cell is not None and cell != 0:
                        try:
                            guest = str(cell[0]) # Μετατροπή σε string για ασφάλεια
                            arrival = cell[1]
                            departure = cell[2]
                        except Exception:
                            continue

                        if str(guest_name).lower() in guest.lower():
                            
                            unique_key = (room_idx + 1, guest, arrival, departure)
                            
                            if unique_key not in seen_reservations:
                                seen_reservations.add(unique_key)
                                new_row = pd.DataFrame([{
                                    "Room Number": room_idx + 1, 
                                    "Guest Name": guest,
                                    "Arrival Date": arrival,
                                    "Departure Date": departure
                                }])
                                df = pd.concat([df, new_row], ignore_index=True)
        print(df)
        
    elif guest_name == "0" and dates == "0":
        display_calendar()
    else:
        print("Please provide at least two parameters as '0' to search reservations.")
def search_reservation():
    room_number=int(input("Enter room number to view reservations (1-10). Press 100 if you are not sure: "))
    guest_name=input("Enter guest name to search for. Press 0 if you don't know the guest name: ")
    dates=input("Enter reservation dates to search for (e.g., June 15 to June 20). Press 0 if you don't know the dates: ")
    find_reservations(room_number, guest_name, dates)


def cancelation(room_number, arrival_date, departure_date):
    arrival_month, arrival_day = arrival_date.split()
    departure_month, departure_day = departure_date.split()
    arrival_day = int(arrival_day) - 1
    departure_day = int(departure_day) - 1
    month_order = ['May', 'June', 'July', 'August', 'September']
    arrival_index = month_order.index(arrival_month)
    departure_index = month_order.index(departure_month)
    if arrival_index == departure_index:
        month = months[arrival_month]
        month[room_number-1, arrival_day:departure_day] = 0
    else:
        for month in month_order[arrival_index:departure_index+1]:
            if month == arrival_month:
                month_array = months[month]
                month_array[room_number-1, arrival_day:] = 0
            elif month == departure_month:
                month_array = months[month]
                month_array[room_number-1, :departure_day] = 0
            else:
                month_array = months[month]
                month_array[room_number-1, :] = 0
    print(f"Reservation for room {room_number} from {arrival_date} to {departure_date} has been canceled.")
    save_reservations()
def cancel_reservation():
    room_number=int(input("Enter room number to cancel reservation (1-10): "))
    arrival_date=input("Enter the check-in date of the reservation to cancel (e.g., June 15): ")
    departure_date=input("Enter the check-out date of the reservation to cancel (e.g., June 20): ")
    cancelation(room_number, arrival_date, departure_date)
    


def change_reservation():
    room_number=int(input("Enter room number of the reservation to change (1-10): "))
    old_arrival_date=input("Enter the current check-in date of the reservation (e.g., June 15): ")
    old_departure_date=input("Enter the current check-out date of the reservation (e.g., June 20): ")
    new_arrival_date=input("Enter the new check-in date (e.g., June 15): ")
    new_departure_date=input("Enter the new check-out date (e.g., June 20): ")
    guest_name=input("Enter guest name: ")
    cancelation(room_number, old_arrival_date, old_departure_date)
    if is_available(room_number, new_arrival_date, new_departure_date):
        reservation(room_number, new_arrival_date, new_departure_date, guest_name)
    else:
        print("The selected room is not available for the new dates. Reverting to old reservation.")
        arrival_month, arrival_day = old_arrival_date.split()
        departure_month, departure_day = old_departure_date.split()
        arrival_day = int(arrival_day) - 1
        departure_day = int(departure_day) - 1
        month_order = ['May', 'June', 'July', 'August', 'September']
        arrival_index = month_order.index(arrival_month)
        departure_index = month_order.index(departure_month)
        if arrival_index == departure_index:
            month = months[arrival_month]
            month[room_number-1, arrival_day:departure_day] =[str(guest_name),str(old_arrival_date),str(old_departure_date)]
        else:
            for month in month_order[arrival_index:departure_index+1]:
                if month == arrival_month:
                    month_array = months[month]
                    month_array[room_number-1, arrival_day:] = [guest_name, old_arrival_date, old_departure_date]
                elif month == departure_month:
                    month_array = months[month]
                    month_array[room_number-1, :departure_day] = [guest_name, old_arrival_date, old_departure_date]
                else:
                    month_array = months[month]
                    month_array[room_number-1, :] = [guest_name, old_arrival_date, old_departure_date]
        save_reservations()
        print(f"Reverted to old reservation for room {room_number} from {old_arrival_date} to {old_departure_date}.")

""""Calendar Display Function"""

def reservations_to_dataframe(month):
    """Return a DataFrame for a specific month with rows as rooms and
    columns as unique reservations within that month.

    Parameters
    - month (str): one of 'June', 'July', 'August', 'September'

    Each column represents one reservation (guest + arrival to departure).
    The cell contains the reservation label for the room that holds that
    reservation and is empty for other rooms.
    """
    global months
    if month not in months:
        raise ValueError(f"month must be one of {list(months.keys())}")

    month_array = months[month]
    rows, cols = month_array.shape

    reservations = {}
    for day in range(cols):
        for room_idx in range(rows):
            cell = month_array[room_idx, day]
            if cell is not None and cell != 0:
                try:
                    guest = cell[0]
                    arrival = cell[1]
                    departure = cell[2]
                except Exception:
                    continue
                key = (guest, arrival, departure)
                if key not in reservations:
                    label = f"{guest}: {arrival} to {departure}"
                    reservations[key] = {"room": room_idx + 1, "label": label}

    index = [f"Room {i}" for i in range(1, rows + 1)]
    col_labels = [v["label"] for v in reservations.values()]
    df = pd.DataFrame(index=index, columns=col_labels)
    df[:] = ""
    for info in reservations.values():
        room = info["room"]
        label = info["label"]
        df.at[f"Room {room}", label] = label

    return df

def display_calendar():
    month=input("Enter the month to display calendar (May, June, July, August, September). Press Enter to display all months: ")
    if month == "":
        for m in months.keys():
            df = reservations_to_dataframe(m)
            print(f"Reservation Calendar for {m}:")
            print(df)
    elif month in months:
        df = reservations_to_dataframe(month)
        print(f"Reservation Calendar for {month}:")
        print(df)
    else:
        print("Invalid month entered.")

def export_calendar_to_excel(filename):
    with pd.ExcelWriter(filename) as writer:
        month=input("Enter the month to export calendar (May, June, July, August, September). Press Enter to export all months: ")
        if month != "" and month in months:
            df = reservations_to_dataframe(month)
            df.to_excel(writer, sheet_name=month)
        else:   
            for month in months.keys():
                df = reservations_to_dataframe(month)
                df.to_excel(writer, sheet_name=month)
"""Import Airbnb Reservations"""
def get_guest_details(guest_name):
    """Βοηθητική συνάρτηση που επιστρέφει (room, arrival, departure) αν βρεθεί ο πελάτης."""
    for month in months.keys():
        month_array = months[month]
        rows, cols = month_array.shape
        for day in range(cols):
            for room_idx in range(rows):
                cell = month_array[room_idx, day]
                if isinstance(cell, (list, np.ndarray)) and len(cell) > 0:
                    try:
                        g_name = str(cell[0])
                        if guest_name.lower() == g_name.lower():
                            return room_idx + 1, cell[1], cell[2]
                    except:
                        continue
    return None

def get_reservation_at_location(room_number, date_str):
    """Ελέγχει αν υπάρχει κράτηση σε συγκεκριμένο δωμάτιο και ημερομηνία έναρξης."""
    try:
        month_str, day_str = date_str.split()
        day_idx = int(day_str) - 1
        
        if month_str in months:
            cell = months[month_str][room_number-1, day_idx]
            # Ελέγχουμε αν το κελί έχει λίστα/πίνακα (άρα κράτηση)
            if isinstance(cell, (list, np.ndarray)) and len(cell) > 0:
                # Επιστρέφουμε (Όνομα, Άφιξη, Αναχώρηση)
                return str(cell[0]), cell[1], cell[2]
    except:
        pass
    return None

def import_airbnb_calendar():
    csv_path = r"C:\Users\User\Downloads\reservations.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: File {csv_path} does not exist.")
        return

    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig', engine='python')
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    print(f"\n📂 Loaded {len(df)} records. Identifying columns...")

    # --- ΕΞΥΠΝΗ ΑΝΙΧΝΕΥΣΗ ΣΤΗΛΩΝ ---
    col_map = {
        'status': ['Status', 'Κατάσταση', 'Status (English)', 'State'],
        'guest': ['Guest Name', 'Guest name', 'Όνομα επισκέπτη', 'Ονοματεπώνυμο', 'Guest'],
        'start': ['Start Date', 'Start date', 'Ημερομηνία άφιξης', 'Άφιξη', 'Check-in'],
        'end': ['End Date', 'End date', 'Ημερομηνία αναχώρησης', 'Αναχώρηση', 'Check-out'],
        'listing': ['Listing', 'Listing Title', 'Καταχώρηση', 'Τίτλος καταχώρησης', 'Room']
    }

    found_cols = {}
    for target, possibilities in col_map.items():
        match = next((c for c in df.columns if c in possibilities), None)
        if match:
            found_cols[target] = match
    
    if len(found_cols) < 5:
        print("\n⛔ The process stopped. Please check the column names.")
        return

    room_map = {
        "'Surfers Harmony' Apartment": 1,
        "\"Surfer's Peace\" Apartment": 3,
        "'Meltemi' Sea View Apartment": 4,
        "\"Surfers's Dream\" Studio": 6,
        "Cycladic Sea View Apartment near Surf Spot": 7,
        "\"Kiter's Base\" Studio": 8,
        "'Surfer's Dream' Apartment": 9,
        "Villa Rock&Surf": 10,
        "Surfers Harmony Apartment": 1,
        "Surfers Peace Apartment": 3,
        "Meltemi Sea View Apartment": 4,
        "Surferss Dream Studio": 6,
        "Kiters Base Studio": 8,
        "Surfers Dream Apartment": 9
    }

    new_bookings = 0
    updated_names = 0
    modified_bookings = 0
    cancelled_bookings = 0
    
# --- ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ---
    
    def convert_date(date_str):
        if pd.isna(date_str): return None
        date_str = str(date_str).strip()
        
        formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']
        
        english_months = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April', 
            5: 'May', 6: 'June', 7: 'July', 8: 'August', 
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                # Αν βρούμε έτος < 1900 ή > 2100 μάλλον είναι λάθος format, συνέχισε
                if dt.year < 2000 or dt.year > 2100: continue
                
                day = dt.strftime("%d").lstrip('0') 
                return f"{english_months[dt.month]} {day}"
            except ValueError:
                continue
        return None

    def clean_listing_name(name):
        name = str(name)
        replacements = {'„': '"', '“': '"', '”': '"', "’": "'", "‘": "'"}
        for old, new in replacements.items():
            name = name.replace(old, new)
        return name.strip()

    def update_guest_name_force(room_num, arr_date, dep_date, new_name):
        try:
            arr_parts = arr_date.split()
            dep_parts = dep_date.split()
            arr_m = arr_parts[0]; arr_d = int(arr_parts[1])
            dep_m = dep_parts[0]; dep_d = int(dep_parts[1])
            
            month_order = ['May', 'June', 'July', 'August', 'September']
            
            arr_idx = month_order.index(arr_m)
            dep_idx = month_order.index(dep_m)
            info = [str(new_name), str(arr_date), str(dep_date)]

            if arr_idx == dep_idx:
                for d in range(arr_d-1, dep_d-1): months[arr_m][room_num-1, d] = info
            else:
                current_idx = arr_idx
                while current_idx <= dep_idx:
                    c_month = month_order[current_idx]
                    start_d = arr_d - 1 if current_idx == arr_idx else 0
                    end_d = dep_d - 1 if current_idx == dep_idx else months[c_month].shape[1]
                    for d in range(start_d, end_d): months[c_month][room_num-1, d] = info
                    current_idx += 1
        except: pass

    def find_existing_reservation_by_name(room_num, search_name, search_month):
        """Ψάχνει αν υπάρχει ο πελάτης στο δωμάτιο τον συγκεκριμένο μήνα, ανεξαρτήτως ημερομηνίας."""
        if search_month not in months: return None
        
        month_data = months[search_month]
        search_name_clean = search_name.split()[0].lower() 
        
        for d in range(month_data.shape[1]):
            cell = month_data[room_num-1, d]
            if isinstance(cell, (list, np.ndarray)) and len(cell) > 0:
                current_name = str(cell[0])
                if search_name_clean in current_name.lower() or current_name.lower() in search_name.lower():
                    return current_name, cell[1], cell[2] 
        return None

    # --- ΚΥΡΙΟΣ ΒΡΟΧΟΣ ---
    print("\n--- Έλεγχος Εγγραφών ---")

    for index, row in df.iterrows():
        status = str(row.get(found_cols['status'], '')).strip()
        guest_name = str(row.get(found_cols['guest'], 'Unknown')).strip()
        raw_listing = str(row.get(found_cols['listing'], '')).strip()
        listing = clean_listing_name(raw_listing)
        
        arrival_date = convert_date(row.get(found_cols['start']))
        departure_date = convert_date(row.get(found_cols['end']))

        if not arrival_date or not departure_date: continue
        arr_month = arrival_date.split()[0]
        if arr_month not in months: continue

        room_number = room_map.get(listing)
        if room_number is None: room_number = room_map.get(raw_listing)

        # Αν δεν βρέθηκε δωμάτιο
        if room_number is None and status in ['Confirmed', 'Επιβεβαιωμένη', 'Accepted']:
            print(f"⚠️  Uknown Room: '{listing}' ({guest_name})")
            while True:
                try:
                    r = input(f"   Give number (1-10) or 0: ")
                    if r == '0': break
                    if r.isdigit() and 1 <= int(r) <= 10:
                        room_number = int(r); room_map[listing] = room_number; break
                except: pass
        
        if room_number is None: continue

        is_confirmed = status in ['Confirmed', 'Επιβεβαιωμένη', 'Accepted']
        is_cancelled = status in ['Cancelled', 'Ακυρωμένη', 'Canceled']

        if is_confirmed:
            # ΒΗΜΑ 1: Ψάχνουμε ΑΚΡΙΒΩΣ στην ημερομηνία άφιξης
            existing_booking = get_reservation_at_location(room_number, arrival_date)
            
            # ΒΗΜΑ 2: Αν δεν βρέθηκε εκεί, ψάχνουμε ΜΕ ΒΑΣΗ ΤΟ ΟΝΟΜΑ στο δωμάτιο
            if not existing_booking:
                existing_booking = find_existing_reservation_by_name(room_number, guest_name, arr_month)

            if existing_booking:
                e_name, e_arr, e_dep = existing_booking
                
                # ΠΕΡΙΠΤΩΣΗ: Ακριβώς ίδιες ημερομηνίες
                if e_arr == arrival_date and e_dep == departure_date:
                    if e_name.lower() != guest_name.lower() and guest_name != "nan":
                        print(f"✏️  Updated name: '{e_name}' -> '{guest_name}'")
                        update_guest_name_force(room_number, arrival_date, departure_date, guest_name)
                        updated_names += 1
                
                # ΠΕΡΙΠΤΩΣΗ: Διαφορετικές ημερομηνίες (ΤΡΟΠΟΠΟΙΗΣΗ)
                else:
                    if (guest_name.split()[0].lower() in e_name.lower() or e_name.split()[0].lower() in guest_name.lower()):
                        print(f"🔄 Updated dates: {guest_name} ({e_arr}-{e_dep} -> {arrival_date}-{departure_date})")
                        
                        # 1. Ακύρωση παλιάς
                        cancelation(room_number, e_arr, e_dep)
        
                        # 2. Εισαγωγή νέας
                        if is_available(room_number, arrival_date, departure_date):
                            reservation(room_number, arrival_date, departure_date, guest_name)
                            modified_bookings += 1
                        else:
                            print(f"❌ Failed to move reservation. The new dates are already taken.")
                            # Επαναφορά (προαιρετικά) - εδώ απλά μένει ακυρωμένο
            
            else:
                # ΝΕΑ ΚΡΑΤΗΣΗ (Δεν βρέθηκε πουθενά)
                if is_available(room_number, arrival_date, departure_date):
                    reservation(room_number, arrival_date, departure_date, guest_name)
                    print(f"✅ New: {guest_name} -> Room {room_number}")
                    new_bookings += 1

        elif is_cancelled:
            # Για ακύρωση ψάχνουμε επίσης με όνομα αν δεν βρούμε ημερομηνία
            existing_booking = get_reservation_at_location(room_number, arrival_date)
            if not existing_booking:
                existing_booking = find_existing_reservation_by_name(room_number, guest_name, arr_month)
                
            if existing_booking:
                e_name, e_arr, e_dep = existing_booking
                if guest_name.split()[0].lower() in e_name.lower(): 
                    cancelation(room_number, e_arr, e_dep) # Προσοχή: Ακυρώνουμε τις e_arr, e_dep που ΒΡΗΚΑΜΕ
                    print(f"❌ Cancellation: {guest_name}")
                    cancelled_bookings += 1

    save_reservations()
    print(f"\n--- End: New:{new_bookings} | Names:{updated_names} | Modified:{modified_bookings} | Cancelled:{cancelled_bookings}")
"""Season Restart Function"""
def clear_all():
    print("Attention: This will clear all reservations for all months.")
    password = input("Enter the admin password to proceed: ")
    if password == "admin":
        global May, June, July, August, September, months
        May=np.zeros((10, 31), dtype=object)
        June = np.zeros((10, 30), dtype=object)
        July = np.zeros((10, 31), dtype=object)
        August = np.zeros((10, 31), dtype=object)
        September = np.zeros((10, 30), dtype=object)
        months = {'May': May, 'June': June, 'July': July, 'August': August, 'September': September}
        save_reservations()
        print("All reservations have been cleared.")
    else:
        print("Incorrect password. Operation aborted.")
"""Free Mode Function"""
def free_mode():
    print("\n--- Free Mode (Developer Console) ---")
    print("Type 'exit' to return to the main menu.")
    while True:
        try:

            command = input(">>> ")

            if command.strip() == "exit":
                print("Επιστροφή στο μενού...")
                break

            try:
                result = eval(command, globals())
                if result is not None:
                    print(result)
            except SyntaxError:
                exec(command, globals())
                
        except Exception as e:
            print(f"Error: {e}")
"""Menu """
print("Welcome to the Hotel Reservation System")
while True:
    print("\nMenu:")
    print("1. Search Room Availability")
    print("2. Show Monthly Availability")
    print("3. Make a Reservation")
    print("4. Search Reservations")
    print("5. Cancel a Reservation")
    print("6. Change a Reservation")
    print("7. Display Reservation Calendar")
    print("8. Export Reservation Calendar to Excel")
    print("9. Import Airbnb Reservations from CSV")
    print("10. Clear All Reservations (Admin Only)")
    print("11. Free Mode")
    print("0. Exit")
    print("-------------------------------")
    choice = input("Enter your choice: ")
    if choice == '1':
        search_availability()
    elif choice == '2':
        show_availability()
    elif choice == '3':
        make_reservation()
    elif choice == '4':
        search_reservation()
    elif choice == '5':
        cancel_reservation()
    elif choice == '6':
        change_reservation()
    elif choice == '7':
        display_calendar()
    elif choice == '8':
        filename = input("Enter the filename to export (e.g., reservations.xlsx): ")
        export_calendar_to_excel(filename)
        print(f"Reservation calendar exported to {filename}.")
    elif choice == '10':
        clear_all()
    elif choice == '9':
        import_airbnb_calendar()
    elif choice == '11':
        free_mode()
    elif choice == '0':
        print("Exiting the system. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")