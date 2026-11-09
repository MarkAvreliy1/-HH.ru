import json
import requests


def open_inf():
    url = 'http://www.cbr.ru/dataservice'
    p_id = 33
    dsId = 128
    Params = {"y1": 2025, "y2": 2025, "datasetId": dsId, "publicationId": p_id}
    response_data = requests.get(f"{url}/data", params=Params)

    response = response_data.status_code
    if response != 200:
        print(f'Ошибка - {response}')

    if __name__ == '__main__':
        with open("Data_course.json", "w", encoding="utf-8") as f:
            json.dump(response_data.json(), f, ensure_ascii=False, indent=2)

    return response_data.json()

#print(open_inf())

class Data:
    def __init__(self):
        self.raw_data = open_inf()

class Cbr:
    def __init__(self):
        self.raw_data = open_inf()
        self.list_course = self.data_course()

    def data_cbr_csv(self):
        if __name__ == "__main__":
            import pandas as pd

            df = pd.json_normalize(self.raw_data)  # распаковывает вложенные словари
            df.to_csv("data_cbr_course.csv", index=False)

    def data_course(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        data_course =  {"101": None, "102": None}
        for el in self.raw_data["RawData"]:
            date_time = datetime.strptime(el['date'], "%Y-%m-%dT%H:%M:%S")
            time_difference = now - date_time
            if time_difference <= timedelta(days=40) and el["element_id"] != 103:
                if el['element_id'] == 101:
                    data_course['101'] = el['obs_val']
                else:
                    data_course["102"] = el['obs_val']

        return data_course

    def euro_course(self):
        return self.list_course["102"]

    def dollar_course(self):
        return self.list_course["101"]


c = Cbr()
print(Cbr().euro_course())
