import matplotlib.pyplot as plt
import datetime
import pandas as pd

from collections import defaultdict

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

def plot_schedule_changes(json_data):
    """
    Plot the schedule changes over time from the provided JSON data.

    Parameters
    ----------
    json_data : list of dict
        List of dictionaries containing the schedule change data.
    """
    # Extract dates and metrics
    dates = [datetime.datetime.strptime(entry['dataDate'], '%Y-%m-%dT%H:%M:%S') for entry in json_data]
    
    metrics = json_data[0]['metrics'].keys()
    
    # Initialize a dictionary to hold lists of metric values
    metric_values = {metric: [] for metric in metrics}
    
    # Populate the metric values dictionary
    for entry in json_data:
        for metric in metrics:
            metric_values[metric].append(entry['metrics'][metric])

    # Define colors and linestyles for each metric
    color_linestyle_dict = {
        "CriticalChanges": {"color": 'red', "marker": 'o'},
        "NearCriticalChanges": {"color": 'goldenrod', "marker": 'd'},
        "ActivityChanges": {"color": 'seagreen', "marker": 's'},
        "LogicChanges": {"color": 'blue', "marker": '^'},
        "CalendarChanges": {"color": 'dodgerblue', "marker": 'v'},
        "DurationChanges": {"color": 'steelblue', "marker": 'o'},
        "DelayedActivityChanges": {"color": 'firebrick', "marker": 'd'},
    }

    plt.figure(figsize=(14, 10))
    ms = 4  # marker size
    lw = 2  # linewidth
    
    for metric, style in color_linestyle_dict.items():
        plt.plot(dates, metric_values[metric], label=metric, marker=style["marker"], markersize=ms, linewidth=lw, color=style["color"])
    
    plt.title('Schedule Changes Over Time')

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
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def plot_activity_distribution_by_month(json_data, scenario_details):
    """
    Plot the activity start and finish dates by month from the provided JSON data.

    Parameters
    ----------
    json_data : list of dict
        List of dictionaries containing the activity data.
    """
    # Data date
    data_date = datetime.datetime.strptime(scenario_details["dataDate"], "%Y-%m-%d")

    # Initialize a dictionary to hold counts for each month and category
    counts = defaultdict(lambda: defaultdict(int))

    # Extract and count the relevant dates
    for entry in json_data:
        dates = {
            'Baseline Starts': entry['baseline'].get('startDate'),
            'Baseline Finishes': entry['baseline'].get('finishDate')
        }
        # Start Dates
        if pd.to_datetime(entry['actualStartDate']):
            dates['Current Starts (Actual)'] = entry['actualStartDate']
        
        if pd.to_datetime(entry['startDate']) is not None and pd.to_datetime(entry['startDate']) >= data_date:
            dates['Current Starts (Planned)'] = entry['startDate']

        # Finish Dates
        if pd.to_datetime(entry['actualFinishDate']):
            dates['Current Finishes (Actual)'] = entry['actualFinishDate']
        elif pd.to_datetime(entry['finishDate']) is not None:
            dates['Current Finishes (Planned)'] = entry['finishDate']
        
        for date_type, date_str in dates.items():
            if date_str:
                date_obj = pd.to_datetime(date_str)
                month_year = (date_obj).strftime('%Y-%m')
                counts[month_year][date_type] += 1

    # Convert the counts dictionary to a DataFrame for easier plotting
    df_counts = pd.DataFrame(counts).fillna(0).T
    df_counts.index = pd.to_datetime(df_counts.index)

    # Define colors for each date type
    colors = {
        'Current Starts (Actual)': 'lightsteelblue',
        'Current Finishes (Actual)': 'cornflowerblue',
        'Current Starts (Planned)': 'lightgreen',
        'Current Finishes (Planned)': 'darkgreen',
        'Baseline Starts': 'lightgrey',
        'Baseline Finishes': 'darkgrey'
    }

    # Plotting
    _, ax = plt.subplots(figsize=(14, 8))
    width = 3  # width of the bars

    # Plot bars for each date type
    for i, date_type in enumerate(df_counts.columns):
        offset = (i - (len(df_counts.columns) - 1) / 2) * width  # center the bars around the first of the month
        ax.bar(df_counts.index + pd.DateOffset(months=-1, days=offset), df_counts[date_type], width=width, label=date_type, color=colors[date_type])

    # Customize x-axis to show the first of every month with the format "mm/yyyy"
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b-%y'))
    ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())

    # Rotate the x-axis labels by -30 degrees and align them to the right
    plt.xticks(rotation=-30, ha='right')
    
    # Remove top, right, and left spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Draw a vertical line for the current date and add the current date text
    ax.axvline(x=data_date + pd.DateOffset(months=-1), color='black', linestyle='--', linewidth=1)
    max_height = df_counts.max().max()
    ax.text(data_date + pd.DateOffset(months=-1, days=1), max_height, f"Data Date: {data_date.strftime('%d %b-%y')}", rotation=-90, verticalalignment='top', horizontalalignment='left')

    # Place the legend below the x-axis with no box around it on one line
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=6, frameon=False)
    plt.grid(True, axis='y')

    plt.title('Monthly Activity Start & Finish Distribution')
    plt.tight_layout()
    plt.show()

    return df_counts.sort_index()