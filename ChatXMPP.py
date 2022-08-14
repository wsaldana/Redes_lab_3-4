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


if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Cliente(slixmpp.ClientXMPP):
    def __init__(self, usu, password):
        slixmpp.ClientXMPP.__init__(self, usu, password)
        self.usu = usu
        self.password = password
        self.add_event_handler("session_start", self.login)
        #self.add_event_handler("register", self.registro)
        #self.add_event_handler("message", self.mensaje)

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
        
        def Delete():
            self.send_presence()
            self.get_roster()

            delete = self.Iq()
            delete['type'] = 'set'
            delete['from'] = self.user
            fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
            delete.append(fragment)

            try:
                delete.send()
                print("Cuenta Borrada")
            except IqError as e:
            
                print("Error", e)
            except IqTimeout:

                print("timeout del server")
            except Exception as e:
        
                print(e)  

            self.disconnect()
        
        while True:
            print("-----------------------------")
            print("|     MENU DE FUNCIONES     |")
            print("-----------------------------")
            print("|1.  Mostrar Contactos      |")
            print("|2.  Agregar Contacto       |")
            print("|3.  Detalles Contacto      |")
            print("|4.  Mensaje Directo        |")
            print("|5.  Conversación Grupal    |")
            print("|6.  Mensaje de Presenca    |")
            print("|7.  Notificaciones         |")
            print("|8.  Archivos               |")
            print("|9.  Eliminar               |")
            print("|10. Salir                  |")
            print("-----------------------------")
            op = input("Ingrese opción:\t")
  
op = ""
print("----------------------------")
print("|     MENU DE OPCIONES     |")
print("----------------------------")
print("|1. Registrar Cuenta       |")
print("|2. Iniciar Sesión         |")
print("|3. Salir                  |")
print("----------------------------")
op = input("Ingrese opción:\t")

if op == "1":
    usu = input("Ingrese usuario(usuario@alumchat.fun): ")
    password = getpass("Ingrese contraseña: ")
    xmpp = Cliente(usu,password)
    xmpp.register_plugin('xep_0004') # Data forms
    xmpp.register_plugin('xep_0066') # Out-of-band Data
    xmpp.register_plugin('xep_0077')
    xmpp.register_plugin('xep_0085')
    xmpp['xep_0077'].force_registration = True
    xmpp.connect()
    xmpp.process()

elif op == "2":
    usu = input("Ingrese usuario(usuario@alumchat.fun): ")
    password = getpass("Ingrese contraseña: ")
    xmpp = Cliente(usu, password)
    xmpp.register_plugin('xep_0030') 
    xmpp.register_plugin('xep_0199') 
    xmpp.connect()
    xmpp.process(forever=False)
                
elif op == "3":
    exit()
