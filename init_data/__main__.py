import csv
import json
import requests


def create_document_request(
        text: str, rubrics: list, created_date: str
) -> requests.Response:
    url = "http://127.0.0.1:8000/v1/documents"

    payload = json.dumps({
        'rubrics': rubrics,
        'text': text,
        'created_date': created_date
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def str_to_rubric_list(string: str) -> list[str]:
    return [
        string.strip("'")
        for string in string.lstrip('[').rstrip(']').split(', ')
    ]


def csv_loader() -> None:
    with open('./init_data/posts.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for line in reader:
            create_document_request(
                text=line[0],
                created_date=line[1],
                rubrics=str_to_rubric_list(line[2])
            )


if __name__ == '__main__':
    csv_loader()
