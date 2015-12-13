__author__ = 'tmkasun'
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import statsmodels.api as sm


def load_data(file_number=1):
    data_collection = {
        1: "data/ta_feng_dataset/D01",
        2: "data/ta_feng_dataset/D02",
        3: "data/ta_feng_dataset/D11",
        4: "data/ta_feng_dataset/D12",
    }
    loaded_data = open(data_collection[file_number])
    return loaded_data


def read_data(data_file):
    print("Pandas version:{}\nNumpy version:{}\n".format(pd.__version__, np.__version__))
    data_lines = data_file.readlines()
    data_length = len(data_lines)
    print("Number of data: {}".format(data_length))
    head_lines = "\n".join(data_lines[:3])
    print("First three lines of the data set\n{}".format(head_lines))
    tail_line = data_lines[-1]
    print("Last line of the data set\n{}".format(tail_line))
    return data_lines


def get_series(data_file):
    separated_lines = csv.reader(data_file, delimiter=";")
    relevant_data = []
    density = {}
    print("Processing data.......")
    for line in separated_lines:

        tx_date = line[0].split(' ')[0]  # Remove empty timestamp
        customer_id = int(line[1])
        if tx_date in density:
            density[tx_date] += 1
        else:
            density[tx_date] = 1
        relevant_data.append([tx_date, customer_id])

    relevant_data = np.array(relevant_data)
    # print(relevant_data.shape)
    starting_month = relevant_data[0][0]
    ending_month = relevant_data[-1][0]
    dates = pd.date_range(starting_month, ending_month, freq='D')
    # print(dates.shape)

    monthly_data = pd.Series(density.values(), index=dates)
    return monthly_data
    # monthly_data_F = monthly_data.cumsum()
    # monthly_data.plot(kind='line')
    # monthly_data_F.plot()
    # details = monthly_data.describe()
    # print(details)

    # m = details['mean']
    # y = mx +
    # plt.show()
    # print("DONE")


def main():
    all_months = []
    for file_number in range(1, 5):
        print("Reading :{}".format(file_number))
        data_file = load_data(file_number)
        read_data(data_file)
        data_file.seek(0)  # Resenting pointer to beginning of the file TODO dam inefficient change this
        monthly_series = get_series(data_file)

        # res = sm.tsa.seasonal_decompose(monthly_series.values,freq=7)
        # res.plot()

        all_months.append(monthly_series)

        # monthly_series.plot(kind='line', linestyle='dashed')
        # a = monthly_series.resample("1D", fill_method="ffill")
        # b = pd.rolling_mean(a, window=10, min_periods=1)
        # b.plot(kind='line')

    combined_series = pd.concat(all_months)
    combined_series.plot(kind='line', linestyle='dashed')

    combined_series_description = combined_series.describe()
    print(combined_series_description)
    a = combined_series.resample("1D", fill_method="ffill")
    b = pd.rolling_mean(a, window=10, min_periods=1)
    b.plot(kind='line')
    plt.show()


if __name__ == '__main__':
    main()