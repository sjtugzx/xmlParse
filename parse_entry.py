import pandas as pd
import ParseInfo
import multiprocessing as mp


if __name__ == '__main__':

    csv_data = pd.read_csv("paperInfo.csv").values.tolist()
    # data_col=["id","pdfpath"]
    # csv_data.columns=data_col
    print(csv_data[0])

    with mp.Pool(80) as pool:
        pool.map(ParseInfo.parseInfo, csv_data)

