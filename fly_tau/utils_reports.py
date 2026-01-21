import matplotlib
matplotlib.use('Agg')
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
from db import db_cur


def report_1():
    with db_cur(dictionary=True) as cur:
        # getting the output from the query
        query = """
WITH last_event AS (
    SELECT bh.booking_code, bh.status, bh.event_time
    FROM bookinghistory bh
    JOIN (
        SELECT booking_code, MAX(event_time) AS max_time
        FROM bookinghistory
        GROUP BY booking_code
    ) x
    ON x.booking_code = bh.booking_code
    AND x.max_time = bh.event_time
),
order_totals AS (
    SELECT
        fb.booking_code,
        f.flight_no,
        s.seat_class,
        SUM(bs.seat_price) AS order_total, 
        le.status AS last_status,
        le.event_time AS last_event_time,
        f.departure_time,
        a.is_large,
        a.manufacturer
    FROM flightbookings fb
    JOIN bookingseats bs
        ON bs.booking_code = fb.booking_code
    JOIN flights f
        ON f.flight_no = fb.flight_no
    JOIN seats s
        ON s.airplane_id = f.airplane_id
        AND s.seat_row = bs.seat_row
        AND s.seat_col = bs.seat_col
    JOIN last_event le
        ON le.booking_code = fb.booking_code
    JOIN airplanes a
        ON a.airplane_id = f.airplane_id
    GROUP BY
        fb.booking_code,
        f.flight_no,
        s.seat_class,
        le.status,
        le.event_time,
        f.departure_time,
        a.is_large,
        a.manufacturer
),
revenue_per_order AS (
    SELECT
        is_large,
        manufacturer,
        seat_class,
        CASE
            WHEN last_status = 'Completed' THEN order_total

            WHEN last_status = 'cancelcustomer'
                AND TIMESTAMPDIFF(HOUR, last_event_time, departure_time) >= 36
            THEN order_total  

            WHEN last_status = 'cancelcustomer'
                AND TIMESTAMPDIFF(HOUR, last_event_time, departure_time) < 36
            THEN order_total

            WHEN last_status = 'Active' THEN order_total 

            ELSE 0
        END AS revenue
    FROM order_totals)

    SELECT
        is_large,
        manufacturer,
        seat_class,
        SUM(revenue) AS total_revenue
    FROM revenue_per_order
    GROUP BY
        is_large,
        manufacturer,
        seat_class;
        """
        cur.execute(query)
        sql_data = cur.fetchall()
        df_1 = pd.DataFrame(sql_data)
    return df_1

def report_2():
    with db_cur(dictionary=True) as cur:
        query ="""WITH RECURSIVE
bounds AS (
	SELECT
        DATE_FORMAT(MIN(departure_time), '%Y-%m-01') AS start_month,
        DATE_FORMAT(MAX(departure_time), '%Y-%m-01') AS end_month
	FROM flights
),
months AS (
	SELECT CAST(start_month AS DATE) AS month_start
	FROM bounds
	UNION ALL
	SELECT DATE_ADD(month_start, INTERVAL 1 MONTH)
	FROM months
	JOIN bounds ON 1=1
	WHERE month_start < CAST(end_month AS DATE)
),
flight_base AS (
	SELECT
    	f.airplane_id,
        DATE_FORMAT(f.departure_time, '%Y-%m-01') AS month_start,
    	f.status,
    	f.origin_airport_name,
    	f.dest_airport_name
	FROM flights f
),
monthly_counts AS (
	SELECT
    	airplane_id,
    	month_start,
    	SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS flights_completed,
    	SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS flights_cancelled
	FROM flight_base
	GROUP BY airplane_id, month_start
),
route_counts AS (
	SELECT
    	airplane_id,
    	month_start,
    	origin_airport_name,
    	dest_airport_name,
    	ROW_NUMBER() OVER (
        	PARTITION BY airplane_id, month_start
        	ORDER BY COUNT(*) DESC, origin_airport_name ASC, dest_airport_name ASC
    	) AS rn
	FROM flight_base
	GROUP BY airplane_id, month_start, origin_airport_name, dest_airport_name
)
SELECT
	a.airplane_id,
	DATE_FORMAT(m.month_start, '%Y-%m') AS flight_month,
	COALESCE(mc.flights_completed, 0) AS flights_completed,
	COALESCE(mc.flights_cancelled, 0) AS flights_cancelled,
	ROUND(100.0 * COALESCE(mc.flights_completed, 0) / 30, 2) AS utilization_percent_assuming_30_days,
	rc.origin_airport_name AS dominant_origin,
	rc.dest_airport_name   AS dominant_destination
FROM airplanes a
CROSS JOIN months m
LEFT JOIN monthly_counts mc
	ON mc.airplane_id = a.airplane_id
   AND mc.month_start = DATE_FORMAT(m.month_start, '%Y-%m-01')
LEFT JOIN route_counts rc
	ON rc.airplane_id = a.airplane_id
   AND rc.month_start = DATE_FORMAT(m.month_start, '%Y-%m-01')
   AND rc.rn = 1
ORDER BY m.month_start, a.airplane_id;
"""
        cur.execute(query)
        sql_data = cur.fetchall()
        df_2 = pd.DataFrame(sql_data)
    return df_2

def get_revenue_chart_image():
    # getting our data from the sql we turned into dataframe
    df = report_1()

    if df.empty:
        return None

    # changing our database name to more appeearing names
    df['total_revenue'] = df['total_revenue'].astype(float)
    df['is_large'] = df['is_large'].map({1: 'Large Aircraft', 0: 'Small Aircraft'})

    navy_blue = "#002147"
    dark_green = "#B8405E"
    bg_color = "#E8EEF4"

    sns.set_theme(style="whitegrid", font="serif", rc={
        "axes.facecolor": bg_color,
        "figure.facecolor": bg_color,
        "grid.color": "#ffffff",
        "grid.linewidth": 1.2
    })

    custom_palette = {"Business": navy_blue, "Economy": dark_green}

    g = sns.catplot(
        data=df, kind="bar", x="manufacturer", y="total_revenue",
        hue="seat_class", col="is_large", palette=custom_palette,
        height=5, aspect=0.9, edgecolor=None, linewidth=0
    )

    g.fig.set_facecolor(bg_color)
    g.fig.subplots_adjust(top=0.82)
    g.fig.suptitle('Revenue Analysis', fontsize=18, fontweight='bold', fontname='serif')

    for ax in g.axes.flat:
        ax.yaxis.set_major_formatter('${x:,.0f}')


    img = io.BytesIO()

    plt.savefig(img, format='png', bbox_inches='tight')

    plt.close()

    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return f"data:image/png;base64,{plot_url}"


def get_utilization_heatmap_image():
    df = report_2()

    if df.empty:
        return None

    df['utilization_percent_assuming_30_days'] = df['utilization_percent_assuming_30_days'].astype(float)

    pivot_df = df.pivot_table(
        index='airplane_id',
        columns='flight_month',
        values='utilization_percent_assuming_30_days',
        fill_value=0
    )

    bg_color = "#E8EEF4"
    navy_blue = "#002147"

    cmap = LinearSegmentedColormap.from_list("CustomNavy", ["white", navy_blue])

    sns.set_theme(style="white", font="serif", rc={
        "axes.facecolor": bg_color,
        "figure.facecolor": bg_color
    })

    plt.figure(figsize=(10, len(pivot_df) * 0.8 + 2))

    ax = sns.heatmap(
        pivot_df,
        annot=True,
        fmt=".1f",
        cmap=cmap,
        linewidths=1,
        linecolor=bg_color,
        cbar_kws={'label': 'Utilization %'}
    )

    plt.title('Monthly Fleet Utilization (%)', fontsize=16, fontweight='bold', color=navy_blue, pad=20)
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Airplane ID', fontsize=12, fontweight='bold')

    for t in ax.texts:
        t.set_text(t.get_text() + "%")

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', facecolor=bg_color)
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return f"data:image/png;base64,{plot_url}"

def get_cancellation_rate_chart_image():
    with db_cur(dictionary=True) as cur:
        query = """
        WITH
        order_creation AS (
            SELECT
                booking_code,
                MIN(event_time) AS creation_time
            FROM bookinghistory
            GROUP BY booking_code
        ),
        last_event AS (
            SELECT bh.booking_code, bh.status
            FROM bookinghistory bh
            JOIN (
                SELECT booking_code, MAX(event_time) AS max_time
                FROM bookinghistory
                GROUP BY booking_code
            ) x
              ON x.booking_code = bh.booking_code
             AND x.max_time = bh.event_time
        ),
        orders_with_month AS (
            SELECT
                oc.booking_code,
                DATE_FORMAT(oc.creation_time, '%Y-%m') AS order_month,
                le.status
            FROM order_creation oc
            JOIN last_event le
              ON le.booking_code = oc.booking_code
        )
        SELECT
            order_month,
            SUM(CASE WHEN status = 'cancelcustomer' THEN 1 ELSE 0 END) / COUNT(*) AS cancellation_rate
        FROM orders_with_month
        GROUP BY order_month
        ORDER BY order_month;
        """
        cur.execute(query)
        data = cur.fetchall()

    df = pd.DataFrame(data)

    df["order_month_dt"] = pd.to_datetime(df["order_month"], format="%Y-%m")
    df = df.sort_values("order_month_dt")
    df["cancellation_rate_pct"] = df["cancellation_rate"] * 100

    plt.figure(figsize=(9, 5))
    ax = sns.lineplot(
        data=df,
        x="order_month_dt",
        y="cancellation_rate_pct",
        marker="o"
    )

    ax.set_title("Cancellation Rate by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Cancellation Rate (%)")

    ax.set_xticks(df["order_month_dt"])
    ax.set_xticklabels(df["order_month"], rotation=45, ha="right")

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return image_base64
