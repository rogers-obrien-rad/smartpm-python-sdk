import matplotlib.pyplot as plt
import datetime

def plot_percent_complete_curve(json_data):
    """
    Plot the progress curve from scenario data.
    Reproduces this figure from SmartPM: https://help.smartpmtech.com/the-progress-curve

    Parameters
    ----------
    json_data : dict
        Dictionary containing percent complete types and scenario data with progress information.
    """
    percent_complete_types = json_data['percentCompleteTypes']
    scenario_data = json_data['data']

    # Extract dates and values for each type of progress
    dates = [datetime.datetime.strptime(point['DATE'], '%Y-%m-%d') for point in scenario_data]

    # Extract data points for each type based on percentCompleteTypes
    data_series = {key: [point.get(key, None) for point in scenario_data] for key in percent_complete_types.keys()}

    # Define colors and linestyles for each type
    colors = {
        "ACTUAL": "steelblue",
        "SCHEDULED": "seagreen",
        "PLANNED": "seagreen",
        "PREDICTIVE": "steelblue",
        "LATE_DATE_PLANNED": "firebrick",
    }
    markers = {
        "ACTUAL": "s",
        "SCHEDULED": "^",
        "PLANNED": "o",
        "PREDICTIVE": "v",
        "LATE_DATE_PLANNED": "d",
    }

    linestyles = {
        "ACTUAL": "-",
        "SCHEDULED": "--",
        "PLANNED": "-",
        "PREDICTIVE": "--",
        "LATE_DATE_PLANNED": "-",
    }

    plt.figure(figsize=(14, 6))
    ms = 4  # marker size
    lw = 2  # linewidth

    # Plot each data series
    for key, label in percent_complete_types.items():
        if any(data_series[key]):
            plt.plot(dates, data_series[key], label=label.split(" (")[0], marker=markers.get(key, 'o'), markersize=ms, linestyle=linestyles.get(key, '-'), linewidth=lw, color=colors.get(key, 'dodgerblue'))

    # Shade the region between early date planned and late date planned lines if available
    if 'PLANNED' in data_series and 'LATE_DATE_PLANNED' in data_series:
        plt.fill_between(dates, data_series['PLANNED'], data_series.get('LATE_DATE_PLANNED', [None]*len(dates)), color='gray', alpha=0.3)

    plt.title('Planned VS Actual Percent Complete')

    # Customize x-axis to show the first of every month with the format "mm/dd/yy"
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%d/%y'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(bymonthday=1, interval=2))

    # Rotate the x-axis labels by -30 degrees and align them to the left
    plt.xticks(rotation=-30, ha='left')

    # Customize y-axis to show 0, 25, 50, 75, 100
    plt.yticks([0, 25, 50, 75, 100])

    # Remove top, right, and left spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Draw a vertical line for the current date if it is before the last date in predictive completion
    current_date = datetime.datetime.now()
    if current_date < max(dates):
        plt.axvline(x=current_date, color='black', linestyle='-', linewidth=lw + 1, label='Current Date')

    # Place the legend below the x-axis with no box around it on one line
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=7, frameon=False)
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def plot_earned_schedule_curve(json_data):
    """
    Plot the earned days curve from the provided JSON data.
    Reproduces this figure: https://help.smartpmtech.com/earned-baseline-days

    Parameters
    ----------
    json_data : dict
        Dictionary containing the date and days data.
    """
    data = json_data['data']

    # Extract dates and values for each type of days
    dates = [datetime.datetime.strptime(point['date'], '%Y-%m-%d') for point in data]
    earned_days = [point['earnedDays'] for point in data]
    planned_days = [point['plannedDays'] for point in data]
    predictive_days = [point['predictiveDays'] if point['predictiveDays'] is not None else None for point in data]

    plt.figure(figsize=(14, 6))
    ms = 4  # marker size
    lw = 2  # linewidth

    plt.plot(dates, earned_days, label='Earned Days', marker='o', markersize=ms, linestyle='-', linewidth=lw, color="seagreen")
    plt.plot(dates, planned_days, label='Planned Days', marker='d', markersize=ms, linestyle='-', linewidth=lw, color="firebrick")
    if any(predictive_days):
        plt.plot(dates, predictive_days, label='Predictive Days', marker='s', markersize=ms, linestyle='-', linewidth=lw, color="goldenrod")

    plt.title('Earned Baseline Days')

    # Customize x-axis to show the first of every month with the format "mm/dd/yy"
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%d/%y'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(bymonthday=1, interval=2))

    # Rotate the x-axis labels by -30 degrees and align them to the left
    plt.xticks(rotation=-30, ha='left')

    # Remove top, right, and left spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Draw a vertical line for the current date if it is before the last date in data
    current_date = datetime.datetime.now()
    if current_date < max(dates):
        plt.axvline(x=current_date, color='black', linestyle='-', linewidth=lw + 1, label='Current Date')

    # Place the legend below the x-axis with no box around it on one line
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=7, frameon=False)
    plt.grid(True)

    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import datetime

def plot_schedule_delay(json_data):
    """
    Plot the schedule delay curve from the provided JSON data.

    Parameters
    ----------
    json_data : dict
        Dictionary containing the schedule variance data.
    """
    data = json_data

    # Extract dates and values for each type of variance
    dates = [datetime.datetime.strptime(point['dataDate'], '%Y-%m-%dT%H:%M:%S') for point in data]
    end_date_variance = [point['endDateVariance']['cumulative'] for point in data]
    critical_path_delay = [point['criticalPathDelay']['cumulative'] for point in data]
    acceleration = [point['delayRecovery']['cumulative']*-1 for point in data] # values are inverse in response

    plt.figure(figsize=(14, 6))
    ms = 4  # marker size
    lw = 2  # linewidth

    plt.plot(dates, end_date_variance, label='End Date Variance', marker='o', markersize=ms, linestyle='-', linewidth=lw, color="goldenrod")
    plt.plot(dates, critical_path_delay, label='Critical Path Delay', marker='d', markersize=ms, linestyle='-', linewidth=lw, color="firebrick")
    plt.plot(dates, acceleration, label='Acceleration', marker='s', markersize=ms, linestyle='-', linewidth=lw, color="seagreen")

    # Shade the area between each curve and the x-axis
    plt.fill_between(dates, end_date_variance, color="goldenrod", alpha=0.7)
    plt.fill_between(dates, critical_path_delay, color="firebrick", alpha=0.7)
    plt.fill_between(dates, acceleration, color="seagreen", alpha=0.7)

    plt.title('Schedule Delay Over Time')

    # Customize x-axis to show the first of every month with the format "mm/dd/yy"
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%d/%y'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(bymonthday=1, interval=2))

    # Rotate the x-axis labels by -30 degrees and align them to the left
    plt.xticks(rotation=-30, ha='left')

    # Remove top, right, and left spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Draw a vertical line for the current date if it is before the last date in data
    current_date = datetime.datetime.now()
    if current_date < max(dates):
        plt.axvline(x=current_date, color='black', linestyle='-', linewidth=lw + 1, label='Current Date')

    # Place the legend below the x-axis with no box around it on one line
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=7, frameon=False)
    plt.grid(True)

    plt.tight_layout()
    plt.show()
