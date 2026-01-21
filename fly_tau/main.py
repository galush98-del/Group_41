from flask import Flask, render_template, request, redirect, url_for
from functools import wraps
from utils import *
from utils_reports import *
from flask import flash

app = Flask(__name__)
app.secret_key = '123'

'''CREATING DECORATORS'''

# Checking if the role is manager or customer, if not, sends back to log in
def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or session.get('role') != 'manager':
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)

    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or session.get('role') != 'customer':
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)

    return decorated_function


'''ERRORS CHECKING FUNCTIONS'''

def checking_validation(text):
    if not text:
        return False
    return bool(re.fullmatch(r'[A-Za-z ]+', text))

def checking_matching_password(pass_1, pass_2):
    return pass_1 == pass_2


'''HOME PAGE'''
@app.route('/')
def homepage():
    """Renders the main landing page or redirects logged-in users to their dashboards."""
    # if already connected, directing the user to their own homepage
    if session.get('logged_in'):
        role = session.get('role')
        if role == 'manager':
            return redirect(url_for('manager_linktree'))
        elif role == 'customer':
            return redirect(url_for('customer_linktree'))

    # else, general homepage
    return render_template("home_page.html")


'''GUEST COSTUMERS ACTIVE FLIGHTS'''
@app.route('/my_bookings', methods=['GET', 'POST'])
def my_bookings():
    """Allows guests to view their active flights by email."""
    flights = None
    message = None

    if request.method == 'POST':
        email = request.form.get('email')

        with db_cur() as cur:
            # if the email is of an registered customer
            # SQL SELECT: Table 'RegisteredCustomers', Column: email
            cur.execute("SELECT 1 FROM registeredcustomers WHERE email = %s", (email,))
            is_registered = cur.fetchone()
            if is_registered:
                return redirect(url_for('login_page',
                                        role='customer',
                                        error="You are a registered member! Please log in."))
            else:
                flights = Booking.get_bookings_for_guest(email)
                if not flights:
                    message = "No active future bookings found for this email."

    return render_template('my_bookings.html', flights=flights, message=message)

def sync_flights_status_db():
    with db_cur() as cur:
        # SQL UPDATE: Table 'Flights', Column: status
        cur.execute("""
            UPDATE flights
            SET status = 'Completed'
            WHERE status = 'Active'
              AND arrival_time <= NOW()
        """)
        # SQL INSERT: Table 'BookingHistory', Column: booking_code, event_time, status
        cur.execute("""
            INSERT INTO bookinghistory (booking_code, event_time, status)
            SELECT fb.booking_code, NOW(), 'Completed'
            FROM flightbookings fb
            JOIN flights f
              ON f.flight_no = fb.flight_no
            JOIN (
                SELECT bh1.booking_code, bh1.status
                FROM bookinghistory bh1
                JOIN (
                    SELECT booking_code, MAX(event_time) AS max_time
                    FROM bookinghistory
                    GROUP BY booking_code
                ) last
                  ON last.booking_code = bh1.booking_code
                 AND last.max_time = bh1.event_time
            ) last_status
              ON last_status.booking_code = fb.booking_code
            WHERE f.arrival_time <= NOW()
              AND last_status.status = 'Active'
        """)


'''FLIGHT BOARD CUSTOMERS'''
@app.route('/flights_board_customers')
def flights_board_customers():
    """Displays a board of all currently active flights for customers."""
    sync_flights_status_db()
    #updating the DB
    flights_data = Flight.get_all_active_flights()  # returning only the active flights
    return render_template("flights_board_customers.html", flights_data=flights_data)

'''FLIGHT BOARD MANAGERS'''
@app.route('/flight_board_managers')
@manager_required
def flight_board_managers():
    """Manager's view of all flights with filtering and status management."""
    sync_flights_status_db()
    # updating the DB
    q = request.args.get('q', '').strip().lower()

    flights = Flight.get_all_flights()  # not just active flights

    if q:
        flights = [
            f for f in flights
            if q in f.flight_id.lower()
            or q in f.origin_airport.lower()
            or q in f.destination_airport.lower()
            or q in f.status.lower()
        ]

    return render_template(
        "flight_board_managers.html",
        flights_data=flights
    )

'''SIGN UP PAGE'''
@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    """Handles new customer registration, including validation and DB insertion."""
    if request.method == "POST":
        #getting the info from the post method
        registration_date = datetime.now()
        signup_first_name = request.form.get('signup_first_name')
        signup_last_name = request.form.get('signup_last_name')
        email_user = request.form.get('email_user')
        phones_list = request.form.getlist('phone_number_user')
        phone_1 = phones_list[0] if len(phones_list) > 0 else ""
        phone_2 = phones_list[1] if len(phones_list) > 1 else ""
        phone_3 = phones_list[2] if len(phones_list) > 2 else ""
        passport_code = request.form.get('passport_code')
        birth_date = request.form.get('birth_date')
        password_user = request.form.get('password_user')
        confirm_password_user = request.form.get('confirm_password_user')

        # Validation: English letters for names
        if not checking_validation(signup_first_name) or not checking_validation(signup_last_name):
            return render_template("signup_page.html",
                                   error_message_name="Name must contain only English letters",
                                   signup_first_name=signup_first_name,
                                   signup_last_name=signup_last_name,
                                   email_user=email_user,
                                   passport_code=passport_code,
                                   birth_date=birth_date,
                                   phone_1=phone_1, phone_2=phone_2, phone_3=phone_3)
        # Validation: Birth date in the past
        if birth_date:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
            if birth_date_obj.date() >= datetime.now().date():
                return render_template("signup_page.html",
                                       error_message_date="Birth date must be in the past",
                                       signup_first_name=signup_first_name,
                                       signup_last_name=signup_last_name,
                                       email_user=email_user,
                                       passport_code=passport_code,
                                       birth_date=birth_date,
                                       phone_1=phone_1, phone_2=phone_2, phone_3=phone_3)

        # Validation: Password matching
        if not checking_matching_password(password_user, confirm_password_user):
            return render_template("signup_page.html",
                                   error_message_pass="Unmatched passwords",
                                   signup_first_name=signup_first_name,
                                   signup_last_name=signup_last_name,
                                   email_user=email_user,
                                   passport_code=passport_code,
                                   birth_date=birth_date,
                                   phone_1=phone_1, phone_2=phone_2, phone_3=phone_3)

        try:
            # Validation: Phone numbers - exactly 10 digits (dashes/spaces allowed)
            if not is_valid_phone_10_digits_allow_dashes(phone_1):
                return render_template("signup_page.html",
                                       error_message_phone="Phone number must contain exactly 10 digits (dashes are allowed). Example: 054-123-4567",
                                       signup_first_name=signup_first_name,
                                       signup_last_name=signup_last_name,
                                       email_user=email_user,
                                       passport_code=passport_code,
                                       birth_date=birth_date,
                                       phone_1=phone_1, phone_2=phone_2, phone_3=phone_3)

            if phone_2 and phone_2.strip() and not is_valid_phone_10_digits_allow_dashes(phone_2):
                return render_template("signup_page.html",
                                       error_message_phone="Additional phone must contain exactly 10 digits (dashes are allowed).",
                                       signup_first_name=signup_first_name,
                                       signup_last_name=signup_last_name,
                                       email_user=email_user,
                                       passport_code=passport_code,
                                       birth_date=birth_date,
                                       phone_1=phone_1, phone_2=phone_2, phone_3=phone_3)

            if phone_3 and phone_3.strip() and not is_valid_phone_10_digits_allow_dashes(phone_3):
                return render_template("signup_page.html",
                                       error_message_phone="Additional phone must contain exactly 10 digits (dashes are allowed).",
                                       signup_first_name=signup_first_name,
                                       signup_last_name=signup_last_name,
                                       email_user=email_user,
                                       passport_code=passport_code,
                                       birth_date=birth_date,
                                       phone_1=phone_1, phone_2=phone_2, phone_3=phone_3)

            with db_cur() as cursor:
                # SQL INSERT: Table 'RegisteredCustomers', Column: email, first_name, last_name, password, passport_number, birth_date, registration_date
                query_costumer = """
                            INSERT INTO RegisteredCustomers 
                            (email, first_name, last_name, password, passport_number, birth_date, registration_date) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                val_customer = (
                email_user, signup_first_name, signup_last_name, password_user, passport_code, birth_date,
                registration_date)
                cursor.execute(query_costumer, val_customer)

                # SQL INSERT: Table 'CustomerPhones', Column: customer_email, phone_number
                query_phone = "INSERT INTO CustomerPhones (customer_email, phone_number) VALUES (%s, %s)"
                for phone in phones_list:
                    if phone and phone.strip():
                        normalized = normalize_phone(phone)
                        if normalized:  # extra safety
                            cursor.execute(query_phone, (email_user, normalized))


        except Exception as e:
            print(f"Database Error: {e}")
            return render_template("signup_page.html",
                                   # Changed variable name to separate it from name errors
                                   error_message_email="Error saving user. Email might already exist.",
                                   signup_first_name=signup_first_name,
                                   signup_last_name=signup_last_name,
                                   email_user=email_user,
                                   passport_code=passport_code,
                                   birth_date=birth_date,
                                   phone_1=phone_1)

        return render_template("signup_success_page.html", name=signup_first_name)
    else:
        return render_template("signup_page.html")


'''LOG IN PAGE'''
@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    """Authenticates customers and managers and sets session variables."""
    # if already connected, directing the user to their own homepage
    if session.get('logged_in'):
        role = session.get('role')
        if role == 'manager':
            return redirect(url_for('manager_linktree'))
        elif role == 'customer':
            return redirect(url_for('customer_linktree'))

    current_role = request.args.get('role', 'customer')

    if request.method == "POST":
        form_type = request.form.get('which_form_is_this')

        if form_type == 'customer':
            email = request.form.get('email_user')
            password = request.form.get('password_user')

            with db_cur(dictionary=True) as cursor:
                # SQL SELECT: Table 'RegisteredCustomers', Column: email, password
                query = "SELECT * FROM RegisteredCustomers WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                user = cursor.fetchone()

            if user:
                session['logged_in'] = True
                session['role'] = 'customer'
                session['name'] = user['first_name']
                session['email'] = user['email']
                return redirect(url_for('customer_linktree'))
            else:
                return render_template("login_page.html", role='customer',
                                       error_message="Wrong email or password")

        elif form_type == 'manager':
            manager_id = request.form.get('manager_id')
            password = request.form.get('password_manager')

            with db_cur(dictionary=True) as cursor:
                # SQL SELECT: Table 'Managers', Column: manager_id, password
                query = "SELECT * FROM Managers WHERE manager_id = %s AND password = %s"
                cursor.execute(query, (manager_id, password))
                manager = cursor.fetchone()

            if manager:
                session['logged_in'] = True
                session['role'] = 'manager'
                session['name'] = manager['first_name']
                return redirect(url_for('manager_linktree'))
            else:
                return render_template("login_page.html", role='manager',
                                       error_message="Wrong Manager ID or password")

    return render_template("login_page.html", role=current_role)

'''LOG OUT'''
@app.route('/logout')
def logout():
    """Clears the user session and redirects to the homepage."""
    session.clear() # delete the info from session
    return redirect(url_for('homepage')) #redirect for FLYTAU homepage

'''LINKTREE CUSTOMER'''
@app.route('/customer_linktree')
@customer_required
def customer_linktree():
    """Main dashboard for logged-in customers with a time-based greeting."""
    name = session.get('name', 'Customer')

    hour = datetime.now().hour
    #setting the time for a special message to the customer
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good night"

    return render_template(
        "customer_linktree.html",
        name=name,
        greeting=greeting
    )



'''LINKTREE MANAGER'''
from datetime import datetime

@app.route('/manager_linktree')
@manager_required
def manager_linktree():
    """Main dashboard for managers with quick links and greeting."""
    name = session.get('name', 'Manager')

    hour = datetime.now().hour
    # setting the time for a special message to the manager
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good night"

    return render_template(
        "manager_linktree.html",
        name=name,
        greeting=greeting
    )



''''PAYING PAGE'''
@app.route('/paying_page', methods=['GET', 'POST'])
def paying_page():
    """Handles the payment process and finalizes the flight booking."""
    if session.get('role') == "manager":
        return render_template("manager_cannot_buy.html")

    flight_no = session.get('current_flight_no')
    selected_seats = session.get('selected_seats')
    num_passengers = session.get('num_passengers')

    if not flight_no or not selected_seats:
        return redirect(url_for('flights_board_customers'))

    current_flight = Flight.get_flight_by_id(flight_no)
    if not current_flight:
        return "Critical Error: Flight not found."

    # Calculate total price for display
    temp_booking = Booking(
        email="calc@temp.com",
        flight_no=flight_no,
        airplane_id=current_flight.airplane_id
    )

    total_price = 0.0
    for seat in selected_seats:
        match = re.match(r"(\d+)([A-Z]+)", seat)
        if match:
            p = temp_booking.get_seat_price(match.group(1), match.group(2))
            total_price += float(p)

    total_price = round(total_price, 2)
    if abs(total_price) < 0.005:
        total_price = 0.0

    if request.method == 'POST':
        raw_card = request.form.get('credit_card', '')
        card_num = normalize_card_number(raw_card)

        # basic checks
        if not (13 <= len(card_num) <= 19):
            return render_template(
                "paying_page.html",
                flight=current_flight,
                seats=selected_seats,
                total_price=total_price,
                count=len(selected_seats),
                error="Invalid credit card number length. Please enter 13–19 digits."
            )
        customer_email = session.get('email') or session.get('guest_email')

        if customer_email:
            try:
                real_booking = Booking(customer_email, flight_no, current_flight.airplane_id)
                booking_code = real_booking.booking_a_ticket(selected_seats)
                session['last_booking_code'] = booking_code

                session.pop('selected_seats', None)
                session.pop('current_flight_no', None)

                return redirect(url_for('paying_success_page'))

            except Exception as e:
                return f"An error occurred: {e}"

        else:
            return "Error: No email found for booking."

    return render_template(
        "paying_page.html",
        flight=current_flight,
        seats=selected_seats,
        total_price=total_price,
        count=len(selected_seats))

'''PAYING SUCCESS PAGE'''
@app.route('/paying_success_page')
def paying_success_page():
    """Displays a success message and booking code after payment."""
    return render_template('paying_success_page.html', name=session.get('name', 'Guest'))

''''ORDERS HISTORY'''
@app.route('/orders_history')
@customer_required
def orders_history():
    """Displays a history of past and upcoming bookings for the user."""
    user_email = session.get('email')
    orders_data = Booking.get_orders_history(user_email)
    message = request.args.get('msg')
    q = request.args.get('q', '').strip().lower()
    if q and orders_data:
        orders_data = [
            order for order in orders_data
            if q in str(order['flight_no']).lower()
               or q in str(order['booking_code']).lower()
               or q in order['origin_airport_name'].lower()
               or q in order['dest_airport_name'].lower()
               or q in order['status'].lower()]
    return render_template("orders_history.html", orders_data=orders_data,message=message)


'''CREATE FLIGHT (MANAGER ONLY)'''
@app.route('/create_flight', methods=['GET', 'POST'])
@manager_required
def create_flight():
    """Step 1 of flight creation: Selecting origin and destination airports."""
    with db_cur(dictionary=True) as cursor:
        # SQL SELECT: Table 'Airports', Column: airport_name
        cursor.execute("SELECT airport_name FROM Airports")
        airports = cursor.fetchall()

    selected_origin = request.args.get('origin')
    selected_destination = request.args.get('destination')

    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        tlv_name = "Ben Gurion airport Tel Aviv"

        route_error = None

        if origin == destination:
            route_error = "Please select a valid flight route (Origin and Destination cannot be the same)."
        elif origin != tlv_name and destination != tlv_name:
            route_error = "All flight must depart or return to Ben Gurion Airport."

        if route_error:
            return render_template(
                "create_flight.html",
                airports=airports,
                route_error=route_error,
                selected_origin=origin,
                selected_destination=destination
            )

        return redirect(url_for('create_flight_time', origin=origin, destination=destination))

    return render_template(
        "create_flight.html",
        airports=airports,
        selected_origin=selected_origin,
        selected_destination=selected_destination
    )


''''CREATE FLIGHT TIME'''
@app.route('/create_flight_time',methods=['GET','POST'])
@manager_required
def create_flight_time():
    """Step 2 of flight creation: Selecting a valid flight date and time."""
    origin=request.args.get('origin')
    destination=request.args.get('destination')
    min_dt = datetime.now() + timedelta(hours=3)
    min_time = min_dt.strftime('%Y-%m-%dT%H:%M')

    if request.method=='POST':
        flight_date=request.form.get('flight_date')

        chosen_dt = datetime.strptime(flight_date, '%Y-%m-%dT%H:%M')
        if chosen_dt < min_dt:
            return render_template(
                "create_flight_time.html",
                origin=origin,
                destination=destination,
                min_time=min_time,
                error="Please choose a time at least 3 hours from now."
            )
        return redirect(url_for('create_flight_plane', origin=origin,destination=destination, flight_date=flight_date))

    return render_template("create_flight_time.html",origin=origin,
                           destination=destination,min_time=min_time)



''''CREATE FLIGHT PLANE'''
@app.route('/create_flight_plane', methods=['GET', 'POST'])
@manager_required
def create_flight_plane():
    """Step 3 of flight creation: Selecting an available airplane."""
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        flight_date_str = request.form.get('flight_date')
        selected_airplane_id = request.form.get('airplane_id')

        return redirect(url_for('create_flight_pilots',
                                origin=origin,
                                destination=destination,
                                flight_date=flight_date_str,
                                airplane_id=selected_airplane_id))


    origin = request.args.get('origin')
    destination = request.args.get('destination')
    flight_date_str = request.args.get('flight_date')

    available_planes = []
    error_msg = None

    if flight_date_str and origin and destination:
        try:
            flight_date_dt = datetime.strptime(flight_date_str, '%Y-%m-%dT%H:%M')

            temp_flight = Flight(
                flight_id=None,
                airplane_id=None,
                origin_airport=origin,
                destination_airport=destination,
                departure_time=flight_date_dt,
                landing_time=None
            )

            result = temp_flight.get_flight_setup_options()

            if isinstance(result, list):
                available_planes = result
                if len(available_planes) == 0:
                    error_msg = "No airplanes are available for this route and time."
            else:
                error_msg = result

        except Exception as e:
            print(f"Error processing flight data: {e}")
            error_msg = "Error processing flight data."

    return render_template("create_flight_plane.html",
                           origin=origin,
                           destination=destination,
                           flight_date=flight_date_str,
                           available_planes=available_planes,
                           error=error_msg)


''''CREATE FLIGHT PILOTS'''
@app.route('/create_flight_pilots', methods=['GET', 'POST'])
@manager_required
def create_flight_pilots():
    """Step 4 of flight creation: Assigning qualified pilots."""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    flight_date_str = request.args.get('flight_date')
    airplane_id = request.args.get('airplane_id')

    available_pilots = []
    error_msg = None
    required_count = 0

    if flight_date_str and origin and destination and airplane_id:
        try:
            flight_date_dt = datetime.strptime(flight_date_str, '%Y-%m-%dT%H:%M')

            temp_flight = Flight(
                flight_id=None,
                airplane_id=airplane_id,
                origin_airport=origin,
                destination_airport=destination,
                departure_time=flight_date_dt,
                landing_time=None
            )

            result = temp_flight.get_pilots_setup_options()

            if isinstance(result, tuple):
                available_pilots, required_count = result
            else:
                error_msg = result

        except Exception as e:
            print(f"Error fetching pilots: {e}")
            error_msg = "Error processing pilot data"

    #getting the choice
    if request.method == 'POST':
        selected_pilots_ids = request.form.getlist('pilot_ids')

        #if there's no demand, not continuing
        if required_count == 0:
            return render_template(
                "create_flight_pilots.html",
                origin=origin,
                destination=destination,
                flight_date=flight_date_str,
                airplane_id=airplane_id,
                available_pilots=available_pilots,
                required_count=required_count,
                error="System error. Please refresh the page and try again."
            )

        # checking amount
        if len(selected_pilots_ids) != required_count:
            error_msg = f"Incorrect number of pilots. Please select exactly {required_count}."
            return render_template(
                "create_flight_pilots.html",
                origin=origin,
                destination=destination,
                flight_date=flight_date_str,
                airplane_id=airplane_id,
                available_pilots=available_pilots,
                required_count=required_count,
                error=error_msg
            )

        pilots_str = ",".join(selected_pilots_ids)

        #redirecting to flight attendants
        return redirect(
            f"/create_flight_attendants"
            f"?origin={origin}"
            f"&destination={destination}"
            f"&flight_date={flight_date_str}"
            f"&airplane_id={airplane_id}"
            f"&pilots={pilots_str}"
        )


    return render_template(
        "create_flight_pilots.html",
        origin=origin,
        destination=destination,
        flight_date=flight_date_str,
        airplane_id=airplane_id,
        available_pilots=available_pilots,
        required_count=required_count,
        error=error_msg
    )



''''CREATE FLIGHT ATTENDANTS'''
@app.route('/create_flight_attendants', methods=['GET', 'POST'])
@manager_required
def create_flight_attendants():
    """Step 5 of flight creation: Assigning flight attendants."""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    flight_date_str = request.args.get('flight_date')
    airplane_id = request.args.get('airplane_id')
    pilots_str = request.args.get('pilots')

    available_attendants = []
    error_msg = None
    required_count = None

    if flight_date_str and origin and destination and airplane_id:
        try:
            flight_date_dt = datetime.strptime(flight_date_str, '%Y-%m-%dT%H:%M')
            temp_flight = Flight(None, airplane_id, origin, destination, flight_date_dt, None)

            result = temp_flight.get_attendants_setup_options()
            if isinstance(result, tuple):
                available_attendants, required_count = result
            else:
                error_msg = result

        except Exception as e:
            print(f"Error fetching attendants: {e}")
            error_msg = "Error processing attendant data"

    if request.method == 'POST':
        selected_attendants_ids = request.form.getlist('attendant_ids')

        if required_count is None:
            error_msg = "System error: missing required attendants count."
            return render_template("create_flight_attendants.html",
                                   origin=origin, destination=destination,
                                   flight_date=flight_date_str, airplane_id=airplane_id,
                                   pilots=pilots_str,
                                   available_attendants=available_attendants,
                                   required_count=required_count,
                                   error=error_msg)

        if len(selected_attendants_ids) != required_count:
            error_msg = f"Incorrect number of attendants. Please select exactly {required_count}."
            return render_template("create_flight_attendants.html",
                                   origin=origin, destination=destination,
                                   flight_date=flight_date_str, airplane_id=airplane_id,
                                   pilots=pilots_str,
                                   available_attendants=available_attendants,
                                   required_count=required_count,
                                   error=error_msg)

        attendants_str = ",".join(selected_attendants_ids)

        return redirect(url_for('create_flight_confirm',
                                origin=origin,
                                destination=destination,
                                flight_date=flight_date_str,
                                airplane_id=airplane_id,
                                pilots=pilots_str,
                                attendants=attendants_str))

    return render_template("create_flight_attendants.html",
                           origin=origin,
                           destination=destination,
                           flight_date=flight_date_str,
                           airplane_id=airplane_id,
                           pilots=pilots_str,
                           available_attendants=available_attendants,
                           required_count=required_count,
                           error=error_msg)

''''CREATE FLIGHT CONFIRM'''
@app.route('/create_flight_confirm', methods=['GET', 'POST'])
@manager_required
def create_flight_confirm():
    """Step 6 of flight creation: Reviewing details before pricing."""
    origin = request.values.get('origin')
    destination = request.values.get('destination')
    flight_date_str = request.values.get('flight_date')
    airplane_id = request.values.get('airplane_id')
    pilots_str = request.values.get('pilots', '')
    attendants_str = request.values.get('attendants', '')

    pilot_ids = [p.strip() for p in pilots_str.split(",") if p.strip()]
    attendant_ids = [a.strip() for a in attendants_str.split(",") if a.strip()]

    pilots = fetch_people("pilots", "pilot_id", pilot_ids)
    attendants = fetch_people("flightattendants", "attendant_id", attendant_ids)

    if request.method == "POST":
        return redirect(url_for('create_flight_pricing',
                                origin=origin,
                                destination=destination,
                                flight_date=flight_date_str,
                                airplane_id=airplane_id,
                                pilots=pilots_str,
                                attendants=attendants_str))

    return render_template("create_flight_confirm.html",
                           origin=origin, destination=destination,
                           flight_date=flight_date_str, airplane_id=airplane_id,
                           pilots=pilots, attendants=attendants,
                           pilots_str=pilots_str, attendants_str=attendants_str)

'''CREATE FLIGHT PRICING'''
@app.route('/create_flight_pricing', methods=['GET', 'POST'])
@manager_required
def create_flight_pricing():
    """Step 7 of flight creation: Setting ticket prices and finalizing."""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    flight_date = request.args.get('flight_date')
    airplane_id = request.args.get('airplane_id')
    pilots_str = request.args.get('pilots')
    attendants_str = request.args.get('attendants')

    if request.method == 'POST':
        economy_price = request.form.get('economy_price')
        business_price = request.form.get('business_price')

        try:
            departure_dt = datetime.strptime(flight_date, '%Y-%m-%dT%H:%M')


            flight = Flight(
                flight_id=None,
                airplane_id=airplane_id,
                origin_airport=origin,
                destination_airport=destination,
                departure_time=departure_dt,
                landing_time=None
            )
            is_large = flight.get_airplane_size()

            #if there is small plane, there is no business class
            if is_large == 0:
                business_price = "0"

            flight_no = flight.create_flight_in_db(
                pilots_str=pilots_str,
                attendants_str=attendants_str,
                economy_price=economy_price,
                business_price=business_price
            )

            return redirect(url_for(
                'create_flight_success',
                flight_no=flight_no
            ))

        except Exception as e:
            msg = str(e)

            # special case :Airplane is already assigned
            if "Airplane is already assigned" in msg or "overlap" in msg:
                return redirect(url_for(
                    'create_flight_plane',
                    origin=origin,
                    destination=destination,
                    flight_date=flight_date,
                    error="The selected airplane was taken by another flight. Please choose a different airplane."
                ))

            departure_dt = datetime.strptime(flight_date, '%Y-%m-%dT%H:%M')
            flight = Flight(
                flight_id=None,
                airplane_id=airplane_id,
                origin_airport=origin,
                destination_airport=destination,
                departure_time=departure_dt,
                landing_time=None
            )
            is_large = flight.get_airplane_size()
            duration_hours = flight.get_duration_hours()

            # every other error, staying at the pricing page
            return render_template(
                'create_flight_pricing.html',
                origin=origin,
                destination=destination,
                flight_date=flight_date,
                airplane_id=airplane_id,
                pilots_str=pilots_str,
                attendants_str=attendants_str,
                is_large=is_large,
                duration_hours=duration_hours,
                error=msg
            )


    departure_dt = datetime.strptime(flight_date, '%Y-%m-%dT%H:%M')
    tmp = Flight(None, airplane_id, origin, destination, departure_dt, None)
    is_large = tmp.get_airplane_size()
    duration_hours = tmp.get_duration_hours()

    return render_template(
        'create_flight_pricing.html',
        origin=origin,
        destination=destination,
        flight_date=flight_date,
        airplane_id=airplane_id,
        pilots_str=pilots_str,
        attendants_str=attendants_str,
        is_large=is_large,
        duration_hours=duration_hours
    )



''''CREATE FLIGHT SUCCESS'''
@app.route('/create_flight_success')
@manager_required
def create_flight_success():
    """Displays a success message with the new flight number."""
    flight_no = request.args.get('flight_no')
    return render_template("create_flight_success.html", flight_no=flight_no)


'''CANCEL FLIGHT (MANAGER ONLY)'''
@app.route('/cancel_flight/<flight_no>', methods=['POST'])
@manager_required
def cancel_flight(flight_no):
    """Allows managers to cancel a specific flight if conditions are met."""
    flight = Flight.get_flight_by_id(flight_no)
    if not flight:
        flash("Flight not found.", "error")
        return redirect(url_for('flight_board_managers'))

    result_message = flight.cancel_flight_by_manager()

    # can be result_message
    # "Flight cancelled successfully"
    # או "Can Not Cancel - Flight Departure Time Less Than 72 Hours"
    if "Can Not Cancel" in result_message:
        flash(result_message, "error")
    else:
        flash(result_message, "success")

    return redirect(url_for('flight_board_managers'))


'''PURCHASE AN AIRPLANE (MANAGER ONLY)'''
@app.route('/purchase_airplane', methods=['GET','POST'])
@manager_required
def add_new_airplane():
    """Handles the addition of a new airplane to the company fleet."""
    if request.method == 'GET':
        return render_template('purchase_airplane.html')

    airplane_id = request.form.get('airplane_id', '').strip()
    purchase_date = request.form.get('purchase_date', '').strip()
    size = request.form.get('size', '').strip()
    manufacturer = request.form.get('manufacturer', '').strip()

    airplane = Airplane(airplane_id, purchase_date, size, manufacturer)
    result = airplane.purchase_airplane()

    if result != "Airplane purchased successfully":
        return render_template(
            'purchase_airplane.html',
            airplane_id=airplane_id,
            purchase_date=purchase_date,
            size=size,
            manufacturer=manufacturer,
            error_message=result
        )

    return redirect(url_for(
        'purchase_airplane_success',
        airplane_id=airplane_id,
        purchase_date=purchase_date,
        size=size,
        manufacturer=manufacturer
    ))

'''PURCHASE AIRPLANE SUCCESS'''
@app.route('/purchase_airplane_success')
@manager_required
def purchase_airplane_success():
    """Displays confirmation details for a newly purchased airplane."""
    airplane_id = request.args.get('airplane_id')
    purchase_date = request.args.get('purchase_date')
    size = request.args.get('size')
    manufacturer = request.args.get('manufacturer')

    size_label = "Large" if str(size) == "1" else "Small"

    return render_template(
        'purchase_airplane_success.html',
        airplane_id=airplane_id,
        purchase_date=purchase_date,
        size_label=size_label,
        manufacturer=manufacturer
    )

'''ADD EMPLOYEE'''
@app.route('/add_employee', methods=['GET', 'POST'])
@manager_required
def add_employee():
    """Form to add new pilots or flight attendants with extensive validation."""
    if request.method == 'POST':
        # getting the data
        id_employee = request.form.get('id_employee')
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        city = request.form.get('city')
        street = request.form.get('street')
        house_num = request.form.get('house_num')
        start_date = request.form.get('start_date')
        phone_num = request.form.get('phone_num')
        role = request.form.get('role')
        is_certified = bool(request.form.get('is_certified'))

        #value check : ID
        if not (id_employee.isdigit() and len(id_employee) == 9):
            flash("ID must contain exactly 9 digits.", "error")
            return render_template("add_employee.html", today=date.today())

        # value check : first and last name
        if not (is_english_with_spaces_hyphens(name) and is_english_with_spaces_hyphens(last_name)):
            flash("First and Last Name must contain English letters only (spaces/hyphens allowed).", "error")
            return render_template("add_employee.html", today=date.today())

        # value check : date
        try:
            input_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if input_date < date.today():
                flash("Start Date cannot be in the past.", "error")
                return render_template("add_employee.html", today=date.today())
        except ValueError:
            flash("Invalid date format.", "error")
            return render_template("add_employee.html", today=date.today())

        #value check : city and street
        if not (is_english_with_spaces_hyphens(city) and is_english_with_spaces_hyphens(street)):
            flash("City and Street must contain English letters only (spaces/hyphens allowed).", "error")
            return render_template("add_employee.html", today=date.today())

        #value check : phone number
        is_valid_phone = (
                len(phone_num) == 11 and
                phone_num.startswith('05') and
                phone_num[3] == '-' and
                phone_num[2].isdigit() and
                phone_num[4:].isdigit()
        )

        if not is_valid_phone:
            flash("Phone must be in format 05X-XXXXXXX (e.g., 054-1234567)", "error")
            return render_template("add_employee.html", today=date.today())

        #data base checks
        try:
            with db_cur() as cur:
                # checking for doubels ID's at different tables
                for table in ['managers', 'pilots', 'flightattendants']:
                    id_col = 'manager_id' if table == 'managers' else (
                        'pilot_id' if table == 'pilots' else 'attendant_id')
                    # SQL SELECT: Table 'Managers'/'Pilots'/'FlightAttendants', Column: [id_col]
                    cur.execute(f"SELECT 1 FROM {table} WHERE {id_col} = %s", (id_employee,))
                    if cur.fetchone():
                        flash(f"Error: Employee ID {id_employee} already exists in {table}!", "error")
                        return render_template("add_employee.html", today=date.today())

                # checking for doubels phone numbers at different tables
                for table in ['managers', 'pilots', 'flightattendants']:
                    # SQL SELECT: Table 'Managers'/'Pilots'/'FlightAttendants', Column: phone_number
                    cur.execute(f"SELECT 1 FROM {table} WHERE phone_number = %s", (phone_num,))
                    if cur.fetchone():
                        flash(f"Error: Phone number {phone_num} is already in use in {table}!", "error")
                        return render_template("add_employee.html", today=date.today())

                #insetion of the data
                if role == "pilot":
                    new_employee = Pilot(id_employee, name, last_name, start_date,
                                         city, street, house_num, phone_num, is_certified)
                    new_employee.add_a_new_pilot()

                elif role == "flightattendant":
                    new_employee = FlightAttendant(id_employee, name, last_name, start_date,
                                                   city, street, house_num, phone_num, is_certified)
                    new_employee.add_a_new_flightattendant()

            return redirect(url_for('employee_added_success', employee_name=name))

        except Exception as e:
            print(f"FAILED TO ADD EMPLOYEE: {e}")
            flash(f"System Error: {e}", "error")
            return render_template("add_employee.html", today=date.today())

    return render_template("add_employee.html", today=date.today())

@app.route('/employee_added_success')
@manager_required
def employee_added_success():
    """Confirmation page shown after successfully adding a new employee."""
    name = request.args.get('employee_name')
    return render_template("employee_added_success.html", name=name)

'''PASSENGERS AMOUNT'''
@app.route('/passengers_amount/<flight_no>',methods=['GET','POST'])
def passengers_amount(flight_no):
    """Sets the number of passengers and guest details before seat selection."""
    if not can_book_flight(flight_no):
        flash("Booking for this flight is closed (less than 3 hours before departure).", "error")
        return redirect('/flights_board_customers')
    session['current_flight_no'] = flight_no
    if request.method == 'POST':
        session['num_passengers'] = int(request.form.get('num_passengers'))
        if not session.get('logged_in'):
            session['guest_email'] = request.form.get('email')
            session['guest_first_name'] = request.form.get('first_name')
            session['guest_last_name'] = request.form.get('last_name')
        return redirect('/select_seats')
    return render_template('passengers_amount.html', flight_no=flight_no)

'''SELECT SEATS'''
@app.route('/select_seats', methods=['GET', 'POST'])
def select_seats():
    """Displays the seat map and handles seat selection for the booking."""
    flight_no = session.get('current_flight_no')
    flash("Please choose a flight first.", "error")
    num_passengers = session.get('num_passengers', 1)

    if not flight_no:
        return redirect(url_for('flights_board_customers'))

    if not can_book_flight(flight_no):
        flash("Booking for this flight is closed (less than 3 hours before departure).", "error")
        return redirect('/flights_board_customers')

    flight = Flight.get_flight_by_id(flight_no)
    if not flight:
        session.pop('current_flight_no', None)
        return redirect(url_for('flights_board_customers'))

    airplane = Airplane(flight.airplane_id, None, None, None)
    rows, cols = airplane.get_dimensions()

    # map of EXISTING seats -> class (from DB),
    seat_class_map = {}
    with db_cur(dictionary=True) as cur:
        # SQL SELECT: Table 'Seats', Column: seat_row, seat_col, seat_class
        cur.execute("""
            SELECT seat_row, seat_col, seat_class
            FROM seats
            WHERE airplane_id = %s
        """, (flight.airplane_id,))
        for r in cur.fetchall():
            seat_id = f"{r['seat_row']}{r['seat_col']}"
            seat_class_map[seat_id] = r['seat_class']  # "Business" / "Economy"

    # Available seats for THIS flight
    available_seats = flight.available_seat()

    with db_cur() as cur:
        # SQL SELECT: Table 'Flights', Column: economy_price, business_price
        cur.execute("""
            SELECT economy_price, business_price
            FROM flights
            WHERE flight_no = %s
        """, (flight.flight_id,))
        prices_row = cur.fetchone()

    economy_price = prices_row[0] if prices_row and prices_row[0] is not None else 0
    business_price = prices_row[1] if prices_row and prices_row[1] is not None else 0

    error = None
    if request.method == 'POST':
        selected_seats = request.form.getlist('seat_choice')
        if len(selected_seats) != num_passengers:
            error = f"Please select exactly {num_passengers} seats."
        else:
            session['selected_seats'] = selected_seats
            return redirect(url_for('paying_page'))

    return render_template(
        'select_seats.html',
        rows=rows,
        cols=cols,
        available_seats=available_seats,
        count=num_passengers,
        error=error,
        seat_class_map=seat_class_map,
        economy_price=economy_price,
        business_price=business_price
    )


'''CANCEL REGISTERED CUSTOMER ORDER'''
@app.route('/cancel_order/<booking_code>', methods=['POST'])
@customer_required
def cancel_order(booking_code):
    """Cancels a booking for a registered customer and updates history."""
    user_email = session.get('email')

    # crating temporary object for cancellation
    temp_booking = Booking(user_email, None, None)
    temp_booking.booking_id = booking_code

    # cancelling throughout the function in utils
    result_text = temp_booking.canceled_by_customer()

    #sending the text with the url
    return redirect(url_for('orders_history', msg=result_text))

'''CANCEL GUEST CUSTOMER ORDER'''
@app.route('/cancel_guest_booking', methods=['POST'])
def cancel_guest_booking():
    """Cancels a booking for a guest user and refreshes their view."""
    # getting the info from the post form
    booking_code = request.form.get('booking_code')
    email = request.form.get('email')

    #canceling the booking
    temp_booking = Booking(email, None, None)
    temp_booking.booking_id = booking_code

    # checking with the class method
    result_message = temp_booking.canceled_by_customer()

    # refreshing and displaying the page
    remaining_flights = Booking.get_bookings_for_guest(email)

    if not remaining_flights and "successfully" in result_message:
        # if canceled his last flight
        result_message += " (No more active flights found)."

    return render_template('my_bookings.html',
                           flights=remaining_flights,
                           message=result_message,
                           searched_email=email)


'''REPORTS'''
@app.route('/reports')
@manager_required
def reports():
    """Generates and displays management analytics charts."""
    chart_1 = get_revenue_chart_image()
    chart_2 = get_utilization_heatmap_image()
    chart_3 = get_cancellation_rate_chart_image()
    return render_template("reports.html", name=session.get('name'),chart_1=chart_1, chart_2=chart_2,chart_3=chart_3)


@app.context_processor
def inject_topbar_user():
    name = session.get('name')  # if theres none, returns none
    if not name:
        return dict(topbar_name=None, topbar_greeting=None)

    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good night"

    return dict(topbar_name=name, topbar_greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)