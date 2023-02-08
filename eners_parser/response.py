import requests

GROUP = 'ТРП-3-20'
WEEK_EOF = 20

HTTP_RESPONSES = ''.join(
    [requests.get(f'https://eners.kgeu.ru/apish2.php?group={GROUP}&week={i}&type=one').text for i in range(WEEK_EOF)]
)
