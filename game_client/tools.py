from socket import socket, AF_INET, SOCK_DGRAM
from map import Map
import json

class GameClient:

    def __init__(self):
        
        self.SEND_PORT = 34255
        self.RECIEVE_PORT = 34253
        self.ADDRESS = "127.0.0.1" # 自分に送信
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.objects = {
                "character_id": "",
                "terrain": Map(),
                "characters": {},
                "items": {},
            }
        self.should_terrain_redraw = False
        self.should_objects_redraw = False

    # ポートを設定
    def set_port(self, send_port, recieve_port):

        self.SEND_PORT = send_port
        self.RECIEVE_PORT = recieve_port
        
        pass

    # アドレスを設定
    def set_address(self, address):

        self.ADDRESS = address

        pass


    # キー入力の状態を送信
    def send_key_message(self, SALT, character_id ,button_name, keystatus, optional):

        input_key_message = {
                    "salt": SALT,
                    "character_id": character_id, # キャラクターID
                    "button_name": button_name, # どのボタンが押されているか
                    "status": keystatus, # キーが押されていればTrue, 離されていればFalse
                    "optional": optional, # オプション情報
                }
    
        self.s.sendto(json.dumps(input_key_message).encode(), (self.ADDRESS, self.SEND_PORT))


    # udpで受け取った値を返す
    def recieve(self, address_check=False):

        msg, address = self.s.recvfrom(self.RECIEVE_PORT)
        address

        game_data = json.loads(msg.decode('utf-8'))

        if "character_id" in game_data.keys():
            self.objects["character_id"] = game_data["character_id"]
        if "characters" in game_data.keys():
            self.should_objects_redraw = True
            for character in game_data["characters"]:
                self.objects["characters"][character["character_id"]] = character
        if "terrain" in game_data.keys() and game_data["terrain"]:
            terrain = game_data["terrain"]
            width = terrain["width"]
            height = terrain["height"]
            self.ox = terrain["origin"]["x"]
            self.oy = terrain["origin"]["y"]
            data = terrain["data"]
            if width != self.objects["terrain"].width or height != self.objects["terrain"].height:
                print("Overwrite terrain")
                self.objects["terrain"] = Map(width=width, height=height, data=data)
                self.should_terrain_redraw = True
            else:
                pass
        if "items" in game_data.keys():
            self.should_objects_redraw = True
            for item in game_data["items"]:
                self.objects["items"][item["item_id"]] = item

    # soketを閉じる
    def game_client_close(self):
        self.s.close()
        pass