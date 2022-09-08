#-----------------------------------#
#|Universidad del Valle de Guatemala|
#|----------------------------------|
#| Redes - Sección 20 - 01/09/2022  |
#|----------------------------------|
#|        LAB 3 Y 4: Routing        |
#-----------------------------------#

import sys
import select
import asyncio
import logging
from getpass import getpass
import slixmpp

from src.routing import Router
from src.models import Message, Node


if sys.platform == 'win32' and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Cliente(slixmpp.ClientXMPP):
    def __init__(
        self, usu, password, node: str = 'A', router: str = 'flooding'
    ):
        slixmpp.ClientXMPP.__init__(self, usu, password)
        self.usu = usu
        self.password = password
        self.router = Router(router)
        self.node = Node(node, usu)


        self.add_event_handler("message", self.receive_msg)
        self.add_event_handler("session_start", self.start)

    def receive_msg(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("\n >> MENSAJE RECIBIDO:")
            print(msg['body'], "\n")

    def DM(self):
        de = input("Ingrese el nombre del nodo que envia: ")
        para = input("Ingrese el nombre del nodo que recibe: ")
        msg = input("Ingrese mensaje:  ")

        json_msg = Message(
            msg,
            de,
            para
        )
        # receiver = self.router.get_next().name

        self.send_message(
            mto=self.router.table[para],
            mbody=json_msg.serialize(),
            mtype="chat"
        )

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        menu = True

        while (menu):
            await self.get_roster()
            print("-----------------------------")
            print("|     MENU DE FUNCIONES     |")
            print("-----------------------------")
            print("|1.  Mensaje Directo        |")
            print("|2.  Obtener ruta           |")
            print("|3.  Salir                  |")
            print("-----------------------------")
            # op = input("Ingrese opción:\t")
            op_std, x, y = select.select([sys.stdin], [], [], 5)
            if op_std:
                op = sys.stdin.readline().strip()
                if (op == "1"):
                    self.DM()

                elif (op == "2"):
                    sender = input("Nodo inicial: ").upper()
                    receiver = input("Nodo receptor: ").upper()

                    print(
                        self.router.get_route(sender, receiver)
                    )

                elif(op == "3"):
                    menu = False
                    self.disconnect()

                else:
                    pass


if __name__ == "__main__":
    # ----------------------------
    # |   Inicio del Programa    |
    # ----------------------------
    logging.basicConfig(level=logging.ERROR, format=None)
    op = ""
    print("----------------------------")
    print("|     MENU DE OPCIONES     |")
    print("----------------------------")
    print("|1. Iniciar Sesión         |")
    print("|2. Salir                  |")
    print("----------------------------")
    op = input("Ingrese opción:\t")

    if op == "1":
        # Login
        usu = input("Ingrese usuario(usuario@alumchat.fun): ")
        password = getpass("Ingrese contraseña: ")
        print(" 1) Flooding")
        print(" 2) Distance Vector")
        print(" 3) Dijkstra")
        alg = input("Ingrese algoritmo: ")
        if alg == "1":
            xmpp = Cliente(usu, password, router='flooding')
        elif alg == "2":
            xmpp = Cliente(usu, password, router='distance')
        else:
            xmpp = Cliente(usu, password, router='dijkstra')
        xmpp.register_plugin('xep_0030')
        xmpp.register_plugin('xep_0199')
        xmpp.register_plugin('xep_0045')
        xmpp.register_plugin('xep_0096')
        xmpp.connect(disable_starttls=True)
        xmpp.process(forever=False)

    elif op == "2":
        exit()
