import requests
import sqlite3


def create():
    con = sqlite3.connect("lucky.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE results(numbers, number_of_winners, game_date, location)")
    cur.commit()


def parse():
    response = requests.get("https://loteriascaixa-api.herokuapp.com/api/mega-sena")
    data = response.json()
    con = sqlite3.connect("lucky.db")
    cur = con.cursor()
    for item in data:
        if item['premiacoes'][0]['vencedores'] > 0:
            numbers = str(item['dezenas'])
            game_date = str(item['data'])
            location = item['local'] if item['local'] != '' else 'Localização não disponível'
            number_of_winners = str(item['premiacoes'][0]['vencedores'])

            print(numbers)
            print(game_date)
            print(location)
            print(number_of_winners)

            query = """INSERT INTO results
                          (numbers, number_of_winners, game_date, location) 
                           VALUES 
                          (?, ?, ?, ?)"""
            cur.execute(query, (numbers, number_of_winners, game_date, location))
            print('-----------------------------------------------')
    con.commit()


if __name__ == '__main__':
    parse()
