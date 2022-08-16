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
        self.add_event_handler("session_start", self.start)
        #self.add_event_handler("add_contact", self.AddContact)
        #self.add_event_handler("message", self.mensaje)

    def DM(self):
        para = input("Ingrese el contacto(ejemplo@alumchat.fun): ")
        self.Notification(para)
        msg = input("Ingrese mensaje:  ")
        self.send_message(mto = para, mbody = msg, mtype = "chat")
    
    def logout(self):
        self.disconnect()
        print("-----Sesión cerrada, Conectese Pronto:)-----")
    
    def sendMsg(self,to):
        message = input("Ingrese mensaje a enviar: ")
        self.send_message(mto=to,
                          mbody=message,
                          mtype='chat')

    def AddContact(self):
        contacto = input("Ingrese el contacto(ejemplo@alumchat.fun): ")
        try:
            self.send_presence_subscription(pto=contacto) 
            self.send_message(mto=contacto,
                          mbody="Hola, quieres ser mi amigo?",
                          mtype='chat')
        except IqTimeout:
            print("Conexión Perdida") 
        
        self.send_presence()
        self.get_roster()

    def ShowContacts(self):
        print('Contactos %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s)' % (name, jid))
                else:
                    print('\n',jid)

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])
                        print('-' * 72)

    def UserInfo(self):
        self.get_roster()
        usuario = input("Ingrese usuario del contacto del que quiere información(ejemplo@alumchat.fun): ")
        estado = self.client_roster.presence(usuario)
        subs = self.client_roster[usuario]['subscription']
        grupos = self.client_roster[usuario]['groups']

        print("--------INFORMACIÓN--------")
        print("Usuario: ", usuario)
        print("Subscripción: ", subs)
        print("Grupos", grupos)
        for res, pres in estado.items():
            print("Estado: ", estado[res]["status"])
            print("Prioridad: ", estado[res]["priority"])

    def GroupMSG(self):
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0199')

        room = input("Nombre del grupo (ejemplo@conference.alumchat.fun): ")
        nickname = input("Apodo/Alias ")
        message = input('Mensaje a enviar al grupo: ')
        self.plugin['xep_0045'].join_muc(room, nickname)
        self.send_message(mto=room, mbody=message, mtype='groupchat')

    def PresMSG(self):
        estado = input("Actualiza tu estado(Available, Not Available, Do not Disturb): ")
        info = input("Que información quiere mostrar en el perfil (chat, away, dnd): ")
        self.send_presence(pshow=info, pstatus=estado)
        print("--------Se ha actualizado el estado--------")
        
    def Notification(self, to):
        notification = self.Message()
        notification["chat_state"] = "composing"
        notification["to"] = to
        notification.send()

    def sendF(self):
        para = input("Indique el usuario al que quiere enviar: ") 
        archivo = input("Direccion del archivo: ")
        
        with open(archivo, 'rb') as img:
            file_ = base64.b64encode(img.read()).decode('utf-8')

        self.send_message(mto=para, mbody=file_, msubject='send_file', mtype='chat')

    def Delete(self):
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

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        menu = True
        logging.basicConfig(level=logging.DEBUG, format=None)

        while (menu):
            print("-----------------------------")
            print("|     MENU DE FUNCIONES     |")
            print("-----------------------------")
            print("|1.  Mostrar Contactos      |")
            print("|2.  Agregar Contacto       |")
            print("|3.  Detalles Contacto      |")
            print("|4.  Mensaje Directo        |")
            print("|5.  Conversación Grupal    |")
            print("|6.  Mensaje de Presencia   |")
            print("|7.  Archivos               |")
            print("|8.  Eliminar               |")
            print("|9.  Salir                  |")
            print("-----------------------------")
            op = input("Ingrese opción:\t")

            if (op == "1"):
                self.ShowContacts()

            elif (op == "2"):
                self.AddContact()
            
            elif(op == "3"):
                self.UserInfo()
            
            elif(op == "4"):
                self.DM()
            
            elif(op == "5"):
                self.GroupMSG()

            elif(op == "6"):
                self.PresMSG()

            elif(op == "7"):
                self.sendF()

            elif(op == "8"):
                self.Delete()

            elif(op == "9"):
                menu = False
                self.logout()
            
            self.send_presence()
            await self.get_roster()

logging.basicConfig(level=logging.DEBUG, format=None)
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
    #Registro pendiente NO SIRVE
    usu = input("Ingrese nuevo usuario: ")
    psd = getpass("Ingrese contraseña: ")

elif op == "2":
    usu = input("Ingrese usuario(usuario@alumchat.fun): ")
    password = getpass("Ingrese contraseña: ")
    xmpp = Cliente(usu, password)
    xmpp.register_plugin('xep_0030') 
    xmpp.register_plugin('xep_0199')
    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
    xmpp.register_plugin('xep_0096') # Jabber Search 
    xmpp.connect()
    xmpp.process(forever=False)
                
elif op == "3":
    exit()
