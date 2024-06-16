from pathlib import Path
import requests
import os
import json
from colorama import Fore , init
import shutil
import ast
import os
from bs4 import BeautifulSoup
import platform
sistema_operativo = platform.system()
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pymongo
from pymongo import MongoClient
#import dns.resolver
import time
import sys
sys.setrecursionlimit(1500)
import aiohttp
import asyncio
import aiohttp_socks
from aiohttp import FormData,MultipartWriter
import aiohttp.client

#dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
#dns.resolver.default_resolver.nameservers = ['1.1.1.1']

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}

if sistema_operativo == "Windows":
    cmd = "cls"
elif sistema_operativo == "Linux":
    cmd = "clear"

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def progress(filename,index,total):
    ifmt = sizeof_fmt(index)
    tfmt = sizeof_fmt(total)
    printl(f'{filename} {ifmt}/{tfmt}')
    pass

def printl(text):
    init()
    print(Fore.GREEN + text,end='\r')

async def make_session(type,id):
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        #session.cookie_jar.update_cookies(cookies)
        if type=="rcc":
            us = "cubaflix"
            ps = "Cubaflix1234*"
            host = "https://rcc.cujae.edu.cu/index.php/rcc/"
            async with session.get(host+"login",headers=headers) as resp:
                html = await resp.text()
            soup = BeautifulSoup(html,"html.parser")
            csrfToken = soup.find("input",attrs={"name":"csrfToken"})['value']
            payload = {}
            payload["csrfToken"] = csrfToken
            payload["source"] = ""
            payload["username"] = us
            payload["password"] = ps
            payload["remember"] = "1"
            async with session.post(host+"login/signIn", data=payload,headers=headers) as resp:
                pass
        else:
            resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":type,"id":id},headers={'Content-Type':'application/json'})
            data = json.loads(resp.text)
            session.cookie_jar.update_cookies(data)
        return session

async def wait_download(url,ichunk=0,index=0,file=None,session=None):
    init()
    printl(Fore.RED + 'Iniciando sesion...')
    dl = url
    if "api.download.cu" in dl:
        data = dl.split("api.download.cu/")[1].split("/")
        total_size = int(data[0])
        ids = data[1]
        filename = data[2].split("?")[-1]
        values = data[2].split("?"+filename)[0].split("?")
        type = "rcc"
        id = ""
        host = f"https://rcc.cujae.edu.cu/index.php/rcc/$$$call$$$/api/file/file-api/download-file?submissionFileId=*&submissionId={ids}&stageId=1"
    else:
        url = dl.split("{")[0]+".file"
        filename = dl.split("/")[-1]
        id = dl.split("{")[1].split("}")[0]
        total_size = int(dl.split("}/")[1].split("/")[0])
        type = "uo"

    if not session:
        session = await make_session(type,id)
    if session:
        init()
        os.system(cmd)
        printl(Fore.BLUE + 'Sesion Iniciada ... !!!')
    else:
        init()
        os.system(cmd)
        printl(Fore.RED + 'Error al iniciar sesion ... !!!')
    state = 'ok'
    i = ichunk
    l = 1
    j = str(l)
    chunk_por = index
    filet = 'Downloading: ' + filename
    if os.path.exists(filename):
        os.unlink(filename)
    if len(filet) > 30:
        filet = 'Downloading ... '
    f = open(filename,"wb") 
    os.system(cmd)
    fnl = []
    totals = total_size
    parte = 0
    if "api.download.cu" in dl:
        for v in values:
            url = host.replace("*",v)
            async with session.get(url,headers=headers) as resp:
                async for chunk in resp.content.iter_chunked(8192):
                    chunk_por += len(chunk)
                    f.write(chunk)
                    progress(f'{filet} ',chunk_por,total_size)
    else:
        while total_size > chunk_por:
            async with session.get(url,headers=headers) as resp:
                async for chunk in resp.content.iter_chunked(8192):
                chunk_por += len(chunk)
                f.write(chunk)
                progress(f'{filet} ',chunk_por,total_size)
            l+=1
            i+=1
            if parte==totals:
                total_size = chunk_por
    f.close()
    if os.path.exists('Cubaflix_Max/' + filename):
        os.unlink('Cubaflix_Max/' + filename)
    shutil.move(filename,'Cubaflix_Max/'+filename)
        
    os.system(cmd)
    printl('Descarga Finalizada !!! Archivos Guardados en ./Downloads. Envie 0 y luego Enter para salir o pulse solo Enter para continuar')
    state = 'finish'
    a = input()
    if a == '0':
        if state == 'finish':
            return False,i,chunk_por,file,session
    else:
        return True,i,chunk_por,file,session

async def initi():
    while (True):
        ichunk = 0
        index = 0
        file = None
        session = None
        init()
        print(Fore.YELLOW + '> Bienvenido a CubaflixMax <')
        print(Fore.YELLOW + 'Ingrese su enlace')
        url = input()
        if os.path.exists('Cubaflix_Max/'):
            pass
        else:
            os.mkdir('Cubaflix_Max/')
        wait,ichunk,index,file,session = await wait_download(url,ichunk,index,file,session)
        if not wait:
            break
                

loop = asyncio.get_event_loop()
loop.run_until_complete(initi())

#https://nube.uo.edu.cu/remote.php/dav/uploads/E88DF8CD-154A-4B85-A255-B162C8632F3A/web-file-upload-de3v9ttpv4azdp5gkkbeupn3ifj2z1zl-2531925677/{1}/1806431279/SITERESRSEVid.mp4