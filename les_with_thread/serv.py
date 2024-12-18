import threading
import time
import socket
import pickle

class CityGameServer:
    def __init__(self):
        self.rooms = {}
        self.lock = threading.Lock()
        self.banned_players = set()

    def handle_client(self, conn, addr):
        print(f"Подключен {addr}")
        time.sleep(1)
        conn.send(pickle.dumps("Введите ваше имя: "))
        player_name = pickle.loads(conn.recv(1024)).strip()
        conn.send(pickle.dumps(f"Добро пожаловать в игру, {player_name}! Введите команду (create, join, exit, change, ban): "))

        while True:
            try:
                command = pickle.loads(conn.recv(1024)).strip()

                if self.is_in_game(conn) and command.lower() not in ["exit", "ban", "change"]:
                    self.handle_game_input(conn, command)
                else:
                    self.handle_command(conn, command)
            except Exception as e:
                print(f"Ошибка при обработке команды: {e}")
                break

    def handle_command(self, conn, command):
        if command.lower() == "create":
            self.create_room(conn)
        elif command.lower() == "join":
            self.join_room(conn)
        elif command.lower() == "exit":
            self.exit_room(conn)
            conn.send(pickle.dumps("Вы покинули комнату. Введите команду (create, join, exit, change, ban): "))
        elif command.lower() == "change":
            self.change_room(conn)
        elif command.lower() == "ban":
            self.ban_player(conn)
        else:
            conn.send(pickle.dumps("Неизвестная команда. Попробуйте еще раз.\n"))

    def create_room(self, conn):
        with self.lock:
            conn.send(pickle.dumps("Введите имя комнаты: "))
            room_name = pickle.loads(conn.recv(1024)).strip()
            if room_name in self.rooms:
                conn.send(pickle.dumps("Комната с таким именем уже существует. Попробуйте другое имя.\n"))
            else:
                self.rooms[room_name] = {'players': [conn], 'cities': set(), 'current_city': "", 'player_turn': 0, 'game_started': False}
                conn.send(pickle.dumps("Комната создана. Ожидание второго игрока...\n"))

    def join_room(self, conn):
        with self.lock:
            conn.send(pickle.dumps("Введите имя комнаты для входа: "))
            room_name = pickle.loads(conn.recv(1024)).strip()
            if room_name not in self.rooms:
                conn.send(pickle.dumps("Комната не существует. Попробуйте другую комнату.\n"))
            else:
                room = self.rooms[room_name]
                if len(room['players']) < 2:
                    room['players'].append(conn)
                    conn.send(pickle.dumps("Вы присоединились к комнате.\n"))
                    if len(room['players']) == 2:
                        self.start_game(room_name)
                else:
                    conn.send(pickle.dumps("Комната заполнена. Попробуйте другую комнату.\n"))

    def exit_room(self, conn):
        with self.lock:
            for room_name, room in self.rooms.items():
                if conn in room['players']:
                    room['players'].remove(conn)
                    if len(room['players']) == 0:
                        del self.rooms[room_name]
                    break

    def change_room(self, conn):
        with self.lock:
            self.exit_room(conn)
            self.join_room(conn)

    def ban_player(self, conn):
        with self.lock:
            conn.send(pickle.dumps("Введите имя игрока для бана: "))
            player_name = pickle.loads(conn.recv(1024)).strip()
            if player_name in self.banned_players:
                conn.send(pickle.dumps(f"Игрок {player_name} уже забанен.\n"))
            else:
                self.banned_players.add(player_name)
                conn.send(pickle.dumps(f"Игрок {player_name} забанен.\n"))
                for room in self.rooms.values():
                    for player in room['players']:
                        if player_name == player.getpeername()[0]:
                            player.send(pickle.dumps(f"Игрок {player_name} забанен.\n"))
                            player.close()
                            room['players'].remove(player)

    def start_game(self, room_name):
        room = self.rooms[room_name]
        if len(room['players']) == 2:
            room['game_started'] = True
            for player in room['players']:
                player.send(pickle.dumps("Игра началась!\n"))
            threading.Thread(target=self.play_game, args=(room_name,), daemon=True).start()
        else:
            for player in room['players']:
                player.send(pickle.dumps("Ожидание второго игрока...\n"))

    def is_in_game(self, conn):
        for room in self.rooms.values():
            if conn in room['players'] and room['game_started']:
                return True
        return False

    def handle_game_input(self, conn, city_name):
        room_name = None
        for room in self.rooms.values():
            if conn in room['players']:
                room_name = room
                break

        if room_name:
            current_player = room_name['players'][room_name['player_turn']]
            if current_player == conn:
                if not room_name['current_city'] or city_name[0].lower() == room_name['current_city'][-1].lower():
                    if city_name.lower() not in room_name['cities']:
                        room_name['cities'].add(city_name.lower())
                        room_name['current_city'] = city_name
                        room_name['player_turn'] = 1 - room_name['player_turn']
                        for player in room_name['players']:
                            if player != current_player:
                                player.send(pickle.dumps(f"Город соперника: {city_name}\n"))
                    else:
                        current_player.send(pickle.dumps("Город уже был назван. Попробуй еще раз.\n"))
                else:
                    current_player.send(pickle.dumps("Город не начинается с правильной буквы. Попробуй еще раз.\n"))

    def play_game(self, room_name):
        room = self.rooms[room_name]
        while room['game_started']:
            current_player = room['players'][room['player_turn']]
            current_player.send(pickle.dumps("Введите город: "))
            data = pickle.loads(current_player.recv(1024)).strip()

            if data.lower() == "exit":
                for player in room['players']:
                    player.send(pickle.dumps("Игрок сдался\n"))
                room['game_started'] = False
                break
            elif not room['current_city'] or data[0].lower() == room['current_city'][-1].lower():
                if data.lower() not in room['cities']:
                    room['cities'].add(data.lower())
                    room['current_city'] = data
                    room['player_turn'] = 1 - room['player_turn']
                    for player in room['players']:
                        if player != current_player:
                            player.send(pickle.dumps(
                                f"Город соперника: {data}\n"))
                else:
                    current_player.send(pickle.dumps("Город уже был назван. Попробуй еще раз.\n"))
            else:
                current_player.send(pickle.dumps("Город не начинается с правильной буквы. Попробуй еще раз.\n"))

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12357))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)
        print("Сервер запущен. Ожидание игроков...")

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server = CityGameServer()
    server.start_server()
