from db import db_cur
from datetime import datetime, timedelta
import random
import string
from flask import session
import re
import uuid

#Generates a random flight number consisting of 2 letters and 3 digits
def generate_flight_no():
    letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
    digits = f"{random.randint(0, 999):03d}"
    return letters + digits

#Verifies that the flight is available for booking.
#Bookings are only allowed up to 3 hours before departure
def can_book_flight(flight_no):
    with db_cur(dictionary=True) as cur:
        cur.execute("""
            SELECT departure_time
            FROM Flights
            WHERE flight_no = %s
        """, (flight_no,))
        row = cur.fetchone()

    if not row:
        return False

    return row['departure_time'] >= datetime.now() + timedelta(hours=3)


class Airplane:
    def __init__(self, airplane_id, purchase_date, size, manufacturer):
        self.airplane_id = airplane_id
        self.manufacturer = manufacturer
        self.size = size
        self.purchase_date = purchase_date

    def purchase_airplane(self):
        #This function registers a new airplane and initializes its seat configuration based on size
        valid_man = {'Boeing', 'Airbus', 'Dassault'}
        # validate airplane name
        airplane_id = (self.airplane_id or "").strip()
        # length must be exactly 4
        if len(airplane_id) != 4:
            return "Airplane ID must be 1 uppercase letter followed by 3 digits (e.g. D400)."

        # first char: uppercase English letter
        if not airplane_id[0].isupper() or not airplane_id[0].isalpha():
            return "Airplane ID must start with one uppercase English letter."

        # next 3 chars: digits
        if not airplane_id[1:].isdigit():
            return "Airplane ID must end with exactly 3 digits."


        # validate size
        try:
            size_int = int(self.size)
        except:
            return "Size must be 0 (small) or 1 (large)."

        if size_int not in (0, 1):
            return "Size must be 0 (small) or 1 (large)."

        # validate manufacturer
        if self.manufacturer not in valid_man:
            return "Manufacturer must be one of: Boeing, Airbus, Dassault."

        # insert
        try:
            with db_cur() as cur:

                cur.execute("""
                    INSERT INTO airplanes (airplane_id, purchase_date, is_large, manufacturer)
                    VALUES (%s, %s, %s, %s)
                """, (self.airplane_id, self.purchase_date, size_int, self.manufacturer))

                seats_to_insert = []

                if size_int == 1:
                    # Large airplane:
                    # Business: rows 1-10, cols A-D
                    for r in range(1, 11):
                        for c in ["A", "B", "C", "D"]:
                            seats_to_insert.append((airplane_id, r, c, "Business"))

                    # Economy: rows 11-20, cols A-F
                    for r in range(11, 21):
                        for c in ["A", "B", "C", "D", "E", "F"]:
                            seats_to_insert.append((airplane_id, r, c, "Economy"))

                else:
                    # Small airplane: rows 1-15, cols A-F, Economy only
                    for r in range(1, 16):
                        for c in ["A", "B", "C", "D", "E", "F"]:
                            seats_to_insert.append((airplane_id, r, c, "Economy"))

                # 3) Insert all seats
                cur.executemany("""
                                INSERT INTO seats (airplane_id, seat_row, seat_col, seat_class)
                                VALUES (%s, %s, %s, %s)
                            """, seats_to_insert)
        except Exception as e:
            # duplicate PK example
            if "Duplicate" in str(e) or "1062" in str(e):
                return "Airplane ID already exists. Please choose a different ID."
            return "Database error while purchasing airplane."

        return "Airplane purchased successfully"


    def get_dimensions(self):
        # Takes an airplane as input and returns a list of its row numbers and column letters
        # We use this function in main.py in "select_seats"
        with db_cur() as cur:
            # rows
            query_rows = """
                SELECT DISTINCT seat_row
                FROM seats
                WHERE airplane_id = %s
                ORDER BY seat_row
            """
            cur.execute(query_rows, (self.airplane_id,))
            rows = [row[0] for row in cur.fetchall()]

            # cols
            query_cols = """
                SELECT DISTINCT seat_col
                FROM seats
                WHERE airplane_id = %s
                ORDER BY seat_col
            """
            cur.execute(query_cols, (self.airplane_id,))
            cols = [col[0] for col in cur.fetchall()]

            return rows, cols # the output is a tuple include 2 list: ([rows],[cols])


class Flight:
    def __init__(self, flight_id, airplane_id, origin_airport, destination_airport,departure_time, landing_time, status = "Active"):
        self.flight_id = flight_id
        self.airplane_id = airplane_id
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.departure_time = departure_time # datetime
        self.landing_time = landing_time     # datetime
        self.status = status


    def kind_of_flight(self):
        # Determines the kind of flight - LONG/SHORT
        # This function compares:
        # the total_duration_minutes (from flightdurations table) with 360 minutes (6 hours)
        with db_cur() as cur:
            query_output_duration = """
                                    SELECT flightdurations.total_duration_minutes
                                    FROM flightdurations
                                    WHERE origin_airport_name = %s 
                                      AND dest_airport_name = %s"""
            cur.execute(query_output_duration, (self.origin_airport, self.destination_airport,))
            output = cur.fetchone()
            if output != None:
                int_output = output[0]
                if int_output > 360:
                    return 1 #  flight is LONG"
                return 0 # flight is SHORT"
            return None # flight NOT FOUND"

    def get_duration_minutes(self):
        #returns the duration of the selected flight from flightdurations table
        #we are going to use this function in the next function "get_duration_hour"
        with db_cur() as cur:
            query = """
                SELECT flightdurations.total_duration_minutes
                FROM flightdurations
                WHERE origin_airport_name = %s
                  AND dest_airport_name = %s
            """
            cur.execute(query, (self.origin_airport, self.destination_airport))
            row = cur.fetchone()
            return row[0] if row else None

    def get_duration_hours(self):
        #returns the duration of the flight in hours
        minutes = self.get_duration_minutes()
        if minutes is None:
            return None
        return round(minutes / 60, 2)

    def ensure_datetime(self, time_val):
        # Helper function: Ensures the date is a real datetime object, not just a string.
        # The HTML form sends a string like '2026-01-21T12:16'. We need to change it.

        if isinstance(time_val, datetime):
            return time_val
        if isinstance(time_val, str):
            try:
                # Try parsing format from HTML (e.g., '2026-01-21T14:30')
                return datetime.strptime(time_val, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    # Try parsing format from Database (e.g., '2026-01-21 14:30:00')
                    return datetime.strptime(time_val, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    pass
        return time_val

    # These functions validate resource availability (airplanes and crew) to ensure no conflicts exist before flight creation.
    # They are utilized by `main.py` route handlers to filter and present only valid, available options to the manager during the setup process.
    def check_airplane_availability(self, required):
        # Checks for available airplanes for a specific flight
        # Step 0: Fix date format using the new helper function
        self.departure_time = self.ensure_datetime(self.departure_time)

        with db_cur() as cur:
            # step 1: Fetch flight duration from flightdurations table
            query_duration = """
                             SELECT total_duration_minutes
                             FROM flightdurations
                             WHERE origin_airport_name = %s
                               AND dest_airport_name = %s \
                             """

            cur.execute(query_duration, (self.origin_airport, self.destination_airport))
            result = cur.fetchone()

            if not result:
                raise ValueError(f"Route not found: {self.origin_airport} -> {self.destination_airport}")

            duration_minutes = result[0]

            # Step 2: Calculate landing time by last output "duration_minutes" and departure_time
            calculated_landing_time = self.departure_time + timedelta(minutes=duration_minutes)

            # Step 3: Check availability:
            query_available_airplanes = """
                                        SELECT a.airplane_id, is_large
                                        FROM airplanes a
                                        WHERE (%s = 0 OR a.is_large = 1)

                                          #-- Location Check
                                          AND COALESCE(
                                                      (SELECT f2.dest_airport_name
                                                       FROM flights f2
                                                       WHERE f2.airplane_id = a.airplane_id
                                                         AND f2.arrival_time <= %s
                                                       ORDER BY f2.arrival_time DESC
                                                      LIMIT 1 ), 'Ben Gurion airport Tel Aviv'
            ) = %s

                                          AND NOT EXISTS (SELECT 1 \
                                                          FROM flights f3 \
                                                          WHERE f3.airplane_id = a.airplane_id \
                                                            AND f3.departure_time < %s \
                                                            AND f3.arrival_time > %s);"""

            cur.execute(query_available_airplanes, (
                required,
                self.departure_time,
                self.origin_airport,
                calculated_landing_time,
                self.departure_time
            ))

            airplanes = cur.fetchall()
            return airplanes


    def get_flight_setup_options(self):
        # this function uses 'check_airplane_availability' to check if the plane is available
        # step 1-checking if we need big airplane or its doesn't matter according kind of flight
        req_size = self.kind_of_flight()
        if req_size is None:
            return "sorry, route not exist in system"
        #step 2- check available airplain accorrding the size
        airplanes_available_output = self.check_airplane_availability(req_size)
        if not airplanes_available_output:
            return "no available airplanes in this time"
        return airplanes_available_output

    #######################################################################################

    def check_pilots_availability(self, required):
        # Step 0: Fix date format using the helper function
        self.departure_time = self.ensure_datetime(self.departure_time)

        with db_cur() as cur:
            # Step 1: Fetch flight duration to calculate landing time
            # we need this query to know when a pilot finish the new flight
            query_duration = """
                             SELECT total_duration_minutes
                             FROM flightdurations
                             WHERE origin_airport_name = %s
                               AND dest_airport_name = %s
                             """
            cur.execute(query_duration, (self.origin_airport, self.destination_airport))
            result = cur.fetchone()

            if not result:
                raise ValueError(f"Route not found: {self.origin_airport} -> {self.destination_airport}")

            duration_minutes = result[0]

            # Calculate estimated landing time
            calculated_landing_time = self.departure_time + timedelta(minutes=duration_minutes)

            # Step 2: Query Available Pilots
            query_available_pilots = """
                                     SELECT p.pilot_id,
                                            p.first_name,
                                            p.last_name,
                                            p.is_certified
                                     FROM pilots p
                                     WHERE (%s = 0 OR p.is_certified = 1) -- Certification Check

                                       -- Location Check:
                                       -- Pilot must be at origin airport based on last arrival
                                       AND COALESCE(
                                                   (SELECT f2.dest_airport_name
                                                    FROM pilotsinflights pf2
                                                             JOIN flights f2 ON f2.flight_no = pf2.flight_no
                                                    WHERE pf2.pilot_id = p.pilot_id
                                                      AND f2.arrival_time <= %s
                                                    ORDER BY f2.arrival_time DESC
                                                   LIMIT 1 ),
                'Ben Gurion airport Tel Aviv'
            ) = %s

                                       -- Schedule Validation (Overlap Check):
                                       -- Ensure no other flight overlaps with the new timeframe
                                       AND NOT EXISTS (SELECT 1
                                                       FROM pilotsinflights pf3
                                                                JOIN flights f3 ON f3.flight_no = pf3.flight_no
                                                       WHERE pf3.pilot_id = p.pilot_id
                                                         -- Conflict Condition:
                                                         -- Existing flight starts before new flight ends
                                                         AND f3.departure_time < %s
                                                         -- AND existing flight ends after new flight starts
                                                         AND f3.arrival_time > %s);"""

            cur.execute(query_available_pilots, (
                required,  # Certification
                self.departure_time,  # For Location Check
                self.origin_airport,  # Required Location
                calculated_landing_time,  # For Overlap Check (End of new flight)
                self.departure_time  # For Overlap Check (Start of new flight)
            ))

            return cur.fetchall()

    def get_pilots_setup_options(self):
        # Step 1: Check the size of the airplane assigned to this flight
        # (Using your existing helper function)
        is_large = self.get_airplane_size()

        if is_large is None:
            return "Error: Airplane ID not found."

        # Step 2: Define business rules based on airplane size
        if is_large == 1:
            # Large Airplane Rules:
            req_certification = 1  # Must be certified (Senior)
            required_count = 3  # Requires 3 pilots
        else:
            # Small Airplane Rules:
            req_certification = 0  # Certification not mandatory
            required_count = 2  # Requires 2 pilots

        # Step 3: Fetch available pilots based on the certification requirement
        pilots_list = self.check_pilots_availability(req_certification)
        if not pilots_list:
            return "No available pilots found."
        # Return both the list of available pilots and the number of pilots required for the form
        return pilots_list, required_count

    def check_attendants_availability(self, required):
        # Step 0: Fix date format using the helper function
        self.departure_time = self.ensure_datetime(self.departure_time)

        with db_cur() as cur:
            # Step 1: Fetch flight duration to calculate landing time
            query_duration = """
                             SELECT total_duration_minutes
                             FROM flightdurations
                             WHERE origin_airport_name = %s
                               AND dest_airport_name = %s
                             """
            cur.execute(query_duration, (self.origin_airport, self.destination_airport))
            result = cur.fetchone()

            if not result:
                raise ValueError(f"Route not found: {self.origin_airport} -> {self.destination_airport}")

            duration_minutes = result[0]

            # Calculate estimated landing time
            calculated_landing_time = self.departure_time + timedelta(minutes=duration_minutes)

            # Step 2: Query Available Attendants
            query_available_attendants = """
                                         SELECT a.attendant_id,
                                                a.first_name,
                                                a.last_name,
                                                a.is_certified
                                         FROM flightattendants a
                                         WHERE (%s = 0 OR a.is_certified = 1) -- Certification Check

                                           -- Location Check:
                                           -- Attendant must be at origin airport based on last arrival
                                           AND COALESCE(
                                                       (SELECT f2.dest_airport_name
                                                        FROM attendantsinflights af2
                                                                 JOIN flights f2 ON f2.flight_no = af2.flight_no
                                                        WHERE af2.attendant_id = a.attendant_id
                                                          AND f2.arrival_time <= %s
                                                        ORDER BY f2.arrival_time DESC
                                                       LIMIT 1 ), 
                               'Ben Gurion airport Tel Aviv'
                  ) = %s

                                           -- Schedule Validation (Overlap Check):
                                           -- Ensure no other flight overlaps with the new timeframe
                                           AND NOT EXISTS (SELECT 1
                                                           FROM attendantsinflights af3
                                                                    JOIN flights f3 ON f3.flight_no = af3.flight_no
                                                           WHERE af3.attendant_id = a.attendant_id
                                                             -- Conflict Condition:
                                                             AND f3.departure_time < %s
                                                             AND f3.arrival_time > %s);"""

            cur.execute(query_available_attendants, (
                required,  # Certification
                self.departure_time,  # Location Check Time
                self.origin_airport,  # Required Location
                calculated_landing_time,  # Overlap Check (End)
                self.departure_time  # Overlap Check (Start)
            ))

            return cur.fetchall()

    def get_attendants_setup_options(self):
            # Step 1: Check the size of the airplane assigned to this flight
        is_large = self.get_airplane_size()

        if is_large is None:
            return "Error: Airplane ID not found."

            # Step 2: Define business rules based on airplane size
        if is_large == 1:
                # Large Airplane Rules:
            req_certification = 1  # Must be certified
            required_count = 6  # Requires 6 attendants
        else:
                # Small Airplane Rules:
            req_certification = 0  # Certification not mandatory
            required_count = 3  # Requires 3 attendants

            # Step 3: Fetch available attendants based on requirements
        attendants_list = self.check_attendants_availability(req_certification)

        if not attendants_list:
            return "No available attendants found."

            # Return both the list and the required count for the form
        return attendants_list, required_count


    def get_airplane_size(self):
        # helper function to detrmine size of airplane by query of airplanes table
        if not self.airplane_id:
            return None
        with db_cur() as cur:
            query = "SELECT is_large FROM airplanes WHERE airplane_id = %s"
            cur.execute(query, (self.airplane_id,))
            result = cur.fetchone()
            if result:
                return result[0] # return 1 -> for big airplane, 0-> for small one
            return None

    @classmethod
    def get_all_active_flights(cls):
        # Returns only future flights that can still be booked (>= 3 hours from now)
        # The output of this function is the content of flights_board_customers page
        with db_cur(dictionary=True) as cur:
            cur.execute("""
                SELECT flight_no,
                       airplane_id,
                       origin_airport_name,
                       dest_airport_name,
                       departure_time,
                       arrival_time,
                       status
                FROM Flights
                WHERE departure_time > NOW() + INTERVAL 3 HOUR
                  AND status IN ('Active', 'Full')
                ORDER BY departure_time
            """)
            rows = cur.fetchall()

        flights = []
        for row in rows:
            flights.append(
                cls(
                    flight_id=row['flight_no'],
                    airplane_id=row['airplane_id'],
                    origin_airport=row['origin_airport_name'],
                    destination_airport=row['dest_airport_name'],
                    departure_time=row['departure_time'],
                    landing_time=row['arrival_time'],
                    status=row['status']
                )
            )
        return flights

    @classmethod
    def get_all_flights(cls):
        # Returns all flights in the system (past, future, cancelled, completed)
        # The output of this function is the content of flight_board_managers page
        with db_cur(dictionary=True) as cur:
            cur.execute("""
                SELECT flight_no,
                       airplane_id,
                       origin_airport_name,
                       dest_airport_name,
                       departure_time,
                       arrival_time,
                       status
                FROM Flights
                ORDER BY departure_time DESC
            """)
            rows = cur.fetchall()

        flights = []
        for row in rows:
            flights.append(
                cls(
                    flight_id=row['flight_no'],
                    airplane_id=row['airplane_id'],
                    origin_airport=row['origin_airport_name'],
                    destination_airport=row['dest_airport_name'],
                    departure_time=row['departure_time'],
                    landing_time=row['arrival_time'],
                    status=row['status']
                )
            )
        return flights

    def cancel_flight_by_manager(self):
        # This function called by the cancel_flight route in main.py
        # to validate the time constraint and execute the cancellation process.
        time_until_flight = self.departure_time - datetime.now()

        if time_until_flight < timedelta(hours=72):
            return "Can Not Cancel - Flight Departure Time Less Than 72 Hours"

        self.status = "Cancelled"

        with db_cur() as cur:
            # should change status flights db:
            cur.execute("""
                UPDATE flights
                SET status = 'Cancelled'
                WHERE flights.flight_no = %s
            """, (self.flight_id,))

            # should add a line with new status in bookinghistory db:
            cur.execute("""
                INSERT INTO bookinghistory (booking_code, event_time, status)
                SELECT booking_code, NOW(), 'CancelSystem'
                FROM flightbookings
                WHERE flight_no = %s
            """, (self.flight_id,))

            # return payment to client:
            cur.execute("""
                UPDATE bookingseats bs
                JOIN flightbookings fb ON fb.booking_code = bs.booking_code
                SET bs.seat_price = 0.0
                WHERE fb.flight_no = %s
            """, (self.flight_id,))

        return "Flight cancelled successfully"

    # ---------- Flight.available_seat (FIXED) ----------
    def available_seat(self):
        # Called by `select_seats` in `main.py` to retrieve available seats for the booking interface.
        # It calculates availability based on the latest status in `bookinghistory` (Active/ Canceled....),
        # ensuring that canceled seats become available again since the system preserves all records.

        output_available_seats = []

        with db_cur() as cur:
            cur.execute("""
                SELECT s.seat_row, s.seat_col
                FROM seats s
                JOIN flights f
                  ON s.airplane_id = f.airplane_id

                LEFT JOIN bookingseats bs
                  ON s.airplane_id = bs.airplane_id
                 AND s.seat_row = bs.seat_row
                 AND s.seat_col = bs.seat_col

                LEFT JOIN flightbookings fb
                  ON bs.booking_code = fb.booking_code
                 AND fb.flight_no = f.flight_no

                WHERE f.flight_no = %s
                  AND (
                        fb.booking_code IS NULL
                        OR (
                            SELECT bh.status
                            FROM bookinghistory bh
                            WHERE bh.booking_code = fb.booking_code
                            ORDER BY bh.event_time DESC
                            LIMIT 1
                        ) IN ('CancelCustomer', 'CancelSystem')
                  )
                ORDER BY s.seat_row, s.seat_col
            """, (self.flight_id,))

            available_seats = cur.fetchall()

            for row in available_seats:
                output_available_seats.append(f"{row[0]}{row[1]}")

        return output_available_seats


    @classmethod
    def get_flight_by_id(cls, flight_no):
        # Called by `select_seats` (and other routes) in `main.py` to retrieve flight
        # details from the database and instantiate a Flight object, allowing access
        # to attributes like `airplane_id`.
        with db_cur(dictionary=True) as cur:
            # getting the data that we need to match the innit of this class
            query = """
                SELECT flight_no, airplane_id, origin_airport_name, 
                       dest_airport_name, departure_time, arrival_time, status 
                FROM Flights 
                WHERE flight_no = %s
            """
            cur.execute(query, (flight_no,))
            row = cur.fetchone()
            # if found, create a temporary instance
            if row:
                return Flight(
                    flight_id=row['flight_no'],
                    airplane_id=row['airplane_id'],
                    origin_airport=row['origin_airport_name'],
                    destination_airport=row['dest_airport_name'],
                    departure_time=row['departure_time'],
                    landing_time=row['arrival_time'],
                    status=row['status'])
            # if not found, return none
            return None

    def create_flight_in_db(self, pilots_str, attendants_str, economy_price, business_price):  
        # --- Validation: Check if prices are valid numbers ---
        try:
            eco = float(economy_price)
            bus = float(business_price)
        except:
            raise Exception("Invalid price values. Please enter numeric prices.")

        # --- Parsing: Convert comma-separated strings to lists and clean whitespace ---
        pilots_ids = [p.strip() for p in (pilots_str or "").split(",") if p.strip()]
        attendants_ids = [a.strip() for a in (attendants_str or "").split(",") if a.strip()]

        # --- Validation: Ensure crew is selected ---
        if not pilots_ids:
            raise Exception("No pilots selected.")
        if not attendants_ids:
            raise Exception("No attendants selected.")

        with db_cur() as cur:
            # --- Logic Replacement 1: Calculate Landing Time (previously handled by SQL Trigger) ---
            # We fetch the duration from the database to calculate the exact landing time in Python.
            cur.execute("""
                SELECT total_duration_minutes
                FROM flightdurations
                WHERE origin_airport_name = %s AND dest_airport_name = %s
            """, (self.origin_airport, self.destination_airport))
            
            row = cur.fetchone()
            if not row:
                raise Exception("Flight duration not found for this route.")
            
            duration_minutes = row[0]
            self.landing_time = self.departure_time + timedelta(minutes=duration_minutes)

            # --- Logic Replacement 2: Check for Airplane Overlap (previously handled by SQL Trigger) ---
            # We check if the selected airplane is already assigned to another flight 
            # that overlaps with the calculated time window.
            cur.execute("""
                SELECT 1 FROM Flights 
                WHERE airplane_id = %s 
                AND departure_time < %s 
                AND arrival_time > %s
            """, (self.airplane_id, self.landing_time, self.departure_time))
            
            if cur.fetchone():
                 raise Exception("The selected airplane was taken by another overlapping flight. Please choose a different airplane.")

            # --- Insertion: Create the flight record (including the calculated arrival_time) ---
            # We attempt to generate a unique flight number up to 30 times.
            for _ in range(30):
                flight_no = generate_flight_no()
                try:
                    insert_flight = """
                        INSERT INTO Flights
                          (flight_no, airplane_id, origin_airport_name, dest_airport_name,
                           departure_time, arrival_time, status, economy_price, business_price)
                        VALUES
                          (%s, %s, %s, %s, %s, %s, 'Active', %s, %s)
                    """
                    cur.execute(insert_flight, (
                        flight_no,
                        self.airplane_id,
                        self.origin_airport,
                        self.destination_airport,
                        self.departure_time,
                        self.landing_time, # Crucial: Inserting the Python-calculated time
                        float(economy_price),
                        float(business_price)
                    ))
                    break # Insert successful, exit loop

                except Exception as e:
                    msg = str(e)
                    # Handle collision of the random flight number
                    if "Duplicate entry" in msg or "1062" in msg:
                        continue
                    raise e # Raise any other database error
            else:
                # If the loop completes without 'break', we failed to find a unique ID
                raise Exception("Could not generate unique flight number. Please try again.")

            # --- Assignment: Insert pilots and attendants into their respective link tables ---
            for pid in pilots_ids:
                cur.execute("INSERT INTO PilotsInFlights (pilot_id, flight_no) VALUES (%s, %s)", (pid, flight_no))

            for aid in attendants_ids:
                cur.execute("INSERT INTO AttendantsInFlights (attendant_id, flight_no) VALUES (%s, %s)",
                            (aid, flight_no))

        return flight_no

class Employee:
#A base class representing shared employee attributes, inherited by pilot, flightattandant and manager.
    def __init__(self, id_employee,name,last_name, start_date, city,street,house_num, phone_num):
        self.id_employee = id_employee
        self.name = name
        self.last_name = last_name
        self.city = city
        self.street = street
        self.house_num = house_num
        self.start_date = start_date
        self.phone_num = phone_num

class FlightAttendant(Employee):
    def __init__(self,id_employee,name,last_name, start_date, city,street,house_num, phone_num,certification):
        super().__init__(id_employee,name,last_name, start_date, city,street,house_num, phone_num)
        self.certification = certification

    def add_a_new_flightattendant(self):
        # Called by `add_employee` in `main.py` to insert the new flight attendant record into the database.
        try:
            with db_cur() as cur:
                cur.execute("""INSERT INTO flightattendants 
                         (attendant_id, first_name,last_name,phone_number, city, street, house_number,start_date, is_certified)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (self.id_employee,self.name,self.last_name,
                                                                 self.phone_num,self.city,self.street,self.house_num, self.start_date,self.certification))
        except Exception as e:
            raise e


class Pilot(Employee):
    def __init__(self,id_employee,name,last_name, start_date, city,street,house_num, phone_num,certification):
        super().__init__(id_employee,name,last_name, start_date, city,street,house_num, phone_num)
        self.certification = certification

    def add_a_new_pilot(self):
        # Called by `add_employee` in `main.py` to insert the new pilot record into the database.
        try:
            with db_cur() as cur:
                cur.execute("""INSERT INTO pilots
                           (pilot_id, first_name,last_name,phone_number, city, street, house_number,start_date, is_certified)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",(self.id_employee,self.name,self.last_name,
                                                                 self.phone_num,self.city,self.street,self.house_num,self.start_date,self.certification))
        except Exception as e:
            raise e

class Manager(Employee):
    def __init__(self,id_employee,name,last_name, start_date, city,street,house_num, phone_num,password):
        super().__init__(id_employee,name,last_name, start_date, city,street,house_num, phone_num)
        self.password = password

class Customer:
    def __init__(self,name,last_name, email, phone_number):
        if name.isalpha() and name.isascii():
            self.name = name
        else:
            raise ValueError("Name and last name must be English")

        if last_name.isalpha() and last_name.isascii():
            self.last_name = last_name
        else:
            raise ValueError("Name and last name must be English")

        self.email = email
        self.phone_number = phone_number

class Guest(Customer):
    def __init__(self,name,last_name, email, phone_number):
        super().__init__(name,last_name, email, phone_number)

class Registered(Customer):
    def __init__(self,name,last_name, email, phone_number,password,birthday, passport_number, registered_date):
        super().__init__(name,last_name, email, phone_number)
        self.password = password
        self.birthday = birthday
        self.passport_number = passport_number
        self.registered_date = registered_date

class Booking:
    def __init__(self, email, flight_no, airplane_id):
        self.booking_id = None #update after
        self.email = email
        self.flight_no = flight_no
        self.airplane_id = airplane_id

    def get_seat_price(self, seat_row, seat_col):
        # Called by `paying_page` in `main.py`
        # to determine the cost of a specific seat based on its class (Economy/Business).
        with db_cur() as cur:
                # 1) Check seat class (Economy / Business)
            query_class = """
                SELECT seat_class
                FROM seats
                WHERE airplane_id = %s AND seat_row = %s AND seat_col = %s
                """
            cur.execute(query_class, (self.airplane_id, seat_row, seat_col))
            res = cur.fetchone()
            seat_class = res[0] if res else 'Economy'

                # 2) Get prices from Flights table
            query_price = """
                SELECT economy_price, business_price
                FROM Flights
                WHERE flight_no = %s
            """
            cur.execute(query_price, (self.flight_no,))
            res_price = cur.fetchone()

            if res_price:
                economy_price = res_price[0]
                business_price = res_price[1]
                return business_price if seat_class == 'Business' else economy_price

            raise Exception(f"Critical Error: Pricing not found for flight {self.flight_no}")


    def booking_a_ticket(self, seats_list):
        # Creates a new booking, saves selected seats, and logs booking history.
        booking_code = f"FB-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        with db_cur() as cur:
            # 1) Check if customer is registered
            query_is_registered = """SELECT 1 FROM registeredcustomers WHERE email = %s"""
            cur.execute(query_is_registered, (self.email,))
            is_registered = 1 if cur.fetchone() else 0

            # 2) Insert booking (explicit booking_code!)
            query_add_new_booking = """
                INSERT INTO flightbookings (booking_code, customer_email, is_registered_at_booking, flight_no)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(query_add_new_booking, (booking_code, self.email, is_registered, self.flight_no))

            # Save booking code on the object (keep your existing naming if other code depends on it)
            self.booking_id = booking_code  # Consider renaming to self.booking_code later

            # 3) Save seats into bookingseats
            query_save_seats = """
                INSERT INTO bookingseats (booking_code, airplane_id, seat_row, seat_col, seat_price)
                VALUES (%s, %s, %s, %s, %s)
            """

            for seat in seats_list:
                match = re.match(r"(\d+)([A-Z]+)", seat)
                if not match:
                    continue

                seat_row = match.group(1)
                seat_col = match.group(2)

                price = self.get_seat_price(seat_row, seat_col)
                cur.execute(query_save_seats, (self.booking_id, self.airplane_id, seat_row, seat_col, price))

            # 4) Add to booking history
            self.add_to_booking_history("Active")

        return self.booking_id

    def add_to_booking_history(self, history_status = "Active"):
        #Adds a new entry to the booking history table for the current booking, recording the current timestamp and the given status (defaulting to "Active").
        with db_cur() as cur:
            query = """INSERT INTO bookinghistory (booking_code, event_time, status)
                           VALUES (%s,NOW(),%s) """
            cur.execute(query,(self.booking_id,history_status))

    @staticmethod
    def get_orders_history(user_email):
        #Retrieves the booking history for a given user, including flight details, latest booking status, ticket count, and assigned seats, ordered by departure time.
        with db_cur(dictionary=True) as cur:
            query = """
                SELECT
                    fb.booking_code,
                    fb.flight_no,
                    f.origin_airport_name,
                    f.dest_airport_name,
                    f.departure_time,

                    (SELECT bh.status
                     FROM bookinghistory bh
                     WHERE bh.booking_code = fb.booking_code
                     ORDER BY bh.event_time DESC
                     LIMIT 1) AS status,

                    COUNT(bs.booking_code) AS tickets_count,

                    GROUP_CONCAT(
                        CONCAT(bs.seat_row, bs.seat_col)
                        ORDER BY bs.seat_row, bs.seat_col
                        SEPARATOR ', '
                    ) AS seats

                FROM flightbookings fb
                JOIN flights f
                    ON f.flight_no = fb.flight_no
                LEFT JOIN bookingseats bs
                    ON bs.booking_code = fb.booking_code

                WHERE fb.customer_email = %s

                GROUP BY
                    fb.booking_code,
                    fb.flight_no,
                    f.origin_airport_name,
                    f.dest_airport_name,
                    f.departure_time

                ORDER BY f.departure_time DESC
            """
            cur.execute(query, (user_email,))
            return cur.fetchall()

    def canceled_by_customer(self):
        #Cancels the booking if eligible, records the cancellation, and applies a 95% refund according to timing rules
        with db_cur() as cur:
            cur.execute("""
                SELECT f.departure_time
                FROM flights f
                JOIN flightbookings fb ON f.flight_no = fb.flight_no
                WHERE fb.booking_code = %s
            """, (self.booking_id,))

            res_time = cur.fetchone()
            if not res_time:
                return "Error: Booking not found."

            departure_time = res_time[0]

            cur.execute("""
                SELECT status 
                FROM bookinghistory 
                WHERE booking_code = %s 
                ORDER BY event_time DESC 
                LIMIT 1
            """, (self.booking_id,))

            res_status = cur.fetchone()
            current_status = res_status[0] if res_status else 'Active'

            if 'Cancel' in current_status:
                return "Error: Booking is already cancelled."

            if departure_time < datetime.now():
                return "Error: Cannot cancel a past flight."

            time_until_flight = departure_time - datetime.now()
            if time_until_flight < timedelta(hours=36):
                return "Cannot Cancel - Less than 36 hours to departure."

            cur.execute("""
                INSERT INTO bookinghistory (booking_code, event_time, status)
                VALUES (%s, NOW(), 'CancelCustomer')
            """, (self.booking_id,))

            cur.execute("""
                UPDATE bookingseats
                SET seat_price = seat_price * 0.05
                WHERE booking_code = %s
            """, (self.booking_id,))

        return "Flight cancelled successfully. 95% refunded."

    @staticmethod
    def get_bookings_for_guest(email):
        # View upcoming bookings for guest + tickets count + seats list
        with db_cur(dictionary=True) as cur:
            query = """
                SELECT
                    fb.booking_code,
                    f.flight_no,
                    f.origin_airport_name,
                    f.dest_airport_name,
                    f.departure_time,

                    -- booking status (latest event)
                    (SELECT bh.status
                     FROM bookinghistory bh
                     WHERE bh.booking_code = fb.booking_code
                     ORDER BY bh.event_time DESC
                     LIMIT 1) AS booking_status,

                    -- NEW: number of tickets (seats) in this booking
                    COUNT(bs.booking_code) AS tickets_count,

                    -- NEW: list of seats like 12A, 12B
                    GROUP_CONCAT(
                        CONCAT(bs.seat_row, bs.seat_col)
                        ORDER BY bs.seat_row, bs.seat_col
                        SEPARATOR ', '
                    ) AS seats

                FROM flightbookings fb
                JOIN flights f
                    ON fb.flight_no = f.flight_no

                LEFT JOIN bookingseats bs
                    ON bs.booking_code = fb.booking_code

                WHERE fb.customer_email = %s
                  AND f.departure_time > NOW()

                GROUP BY
                    fb.booking_code,
                    f.flight_no,
                    f.origin_airport_name,
                    f.dest_airport_name,
                    f.departure_time

                HAVING booking_status = 'Active'
                ORDER BY f.departure_time ASC;
            """
            cur.execute(query, (email,))
            return cur.fetchall()


def fetch_people(table, id_col, ids):
    #Fetches people by ID from the given table and preserves the input order in the result

    if not ids:
        return []

    ids = [x.strip() for x in ids if x and x.strip()]
    if not ids:
        return []

    placeholders = ",".join(["%s"] * len(ids))
    query = f"SELECT {id_col} AS id, first_name, last_name FROM {table} WHERE {id_col} IN ({placeholders})"

    with db_cur(dictionary=True) as cur:
        cur.execute(query, tuple(ids))
        rows = cur.fetchall()

    by_id = {r["id"]: r for r in rows}
    return [by_id[i] for i in ids if i in by_id]

def is_english_letters_only(s: str) -> bool:
    #Returns True if the string contains only English letters and is not empty after trimming whitespace."""
    if not s:
        return False
    s = s.strip()
    if not s:
        return False
    for ch in s:
        if not (('A' <= ch <= 'Z') or ('a' <= ch <= 'z')):
            return False
    return True


def is_english_with_spaces_hyphens(s: str) -> bool:
    #Validates that a string contains only English letters, spaces, and hyphens, includes at least one letter, and does not start, end, or repeat special characters.
    if not s:
        return False
    s = s.strip()
    if not s:
        return False

    allowed = set(" -")
    has_letter = False

    for ch in s:
        if ('A' <= ch <= 'Z') or ('a' <= ch <= 'z'):
            has_letter = True
        elif ch in allowed:
            continue
        else:
            return False

    if s[0] in allowed or s[-1] in allowed:
        return False
    for i in range(1, len(s)):
        if s[i] in allowed and s[i-1] in allowed:
            return False

    return has_letter


def normalize_phone(phone: str) -> str:
    #Normalizes a phone number by trimming whitespace and removing spaces and hyphens.
    if phone is None:
        return ""
    return phone.strip().replace("-", "").replace(" ", "")

def is_valid_phone_10_digits_allow_dashes(phone: str) -> bool:
    p = normalize_phone(phone)

    # must be exactly 10 digits after removing dashes/spaces
    if len(p) != 10:
        return False
    return p.isdigit()


def normalize_card_number(raw: str) -> str:
    #Normalizes a card number by stripping all non-digit characters."""
    if raw is None:
        return ""
    return re.sub(r"\D", "", raw)

def is_luhn_valid(card_digits: str) -> bool:
    # Luhn check
    if not card_digits.isdigit():
        return False
    total = 0
    reverse_digits = card_digits[::-1]
    for i, ch in enumerate(reverse_digits):
        d = ord(ch) - ord('0')
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0

