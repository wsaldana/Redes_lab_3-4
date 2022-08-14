#-----------------------------------#
#|Universidad del Valle de Guatemala|
#|----------------------------------|
#| Redes - Sección 20 - 12/08/2022  |
#|----------------------------------|
#| PROYECTO 1: Apartado ADMIN TOOLS |
#|  Javier Alejandro Cotto Argueta  |
#-----------------------------------#

import sys
import aiodns
import asyncio
import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
import slixmpp
import base64, time
import threading

class Cliente(slixmpp.ClientXMPP):
    def __init__(self, usu, password):
        slixmpp.ClientXMPP.__init__(self, usu, password)
        self.usu = usu
        self.password = password
        self.add_event_handler("session_start", self.login)
        self.add_event_handler("register", self.registro)
        self.add_event_handler("message", self.mensaje)

    async def login(self, event):
        self.send_presence()

        def DM():
            to = input("Ingrese el contacto(ejemplo@alumchat.fun): ")
            msg = input("Ingrese mensaje:  ")
            self.send_message(mto = to, mbody = msg, mtype = "chat")
            print("0/100%")
            time.sleep(3)
            print("---25/100%")
            print("------50/100%")
            time.sleep(3)
            print("---------75/100%")
            print("------------100/100%")
            time.sleep(3)
            print("-----Enviado Exitosamente-----")
        
        def logout():
            self.disconnect()
            print("-----Sesión cerrada, Conectese Pronto:)-----")
        
        def AddContact():
            contacto = input("Ingrese usuario del contacto a agregar(ejemplo@alumchat.fun): ")
            self.send_presence_subscription(pto = contacto)
            print("0/100%")
            time.sleep(3)
            print("---33/100%")
            print("------66/100%")
            time.sleep(3)
            print("----------100/100%")
            print("-----Has añadido a " + str(contacto) + " exitosamente-----")

        def DeleteUser():
            self.register_plugin('xep_0030')    
            self.register_plugin('xep_0004') 
            self.register_plugin('xep_0077')
            self.register_plugin('xep_0199')
            self.register_plugin('xep_0066')

            delete = self.Iq()
            delete['type'] = 'set'
            delete['from'] = self.boundjid.user
            delete['register']['remove'] = True
            delete.send()

            self.disconnect()
            print("-----Espero crees otra cuenta, ya te extrañamos:(-----")


op = ""

print("----------------------------")
print("|     MENU DE OPCIONES     |")
print("----------------------------")
print("|1. Registrar Cuenta       |")
print("|2. Iniciar Sesión         |")
print("|3. Eliminar Cuenta        |")
print("----------------------------")
op = input("Ingrese opción:\t")

if op == "1":
    #crear cuenta
    print("crear cuenta")

elif op == "2":
    usu = input("Ingrese usuario(usuario@alumchat.fun): ")
    password = getpass("Ingrese contraseña: ")

