"""
Este es el módulo de Base de Datos
"""
import os
from libretronic import archivos
from tqdm import tqdm, trange
import time
import psycopg2, psycopg2.extras

def consulta_de_archivo_v3(servidor,base,usuario,passe,rutaDeScript,nombreConsulta):
    """Esta función consulta desde un archivo.sql a un servidor específico"""
    print('Consultando '+nombreConsulta+'.sql')
    archivoConsulta = os.path.join(rutaDeScript,nombreConsulta)
    Cadena='export PGPASSWORD="'+passe+'"; '+' psql -h '+servidor+' -U '+usuario+' -d '+base+' -A -F"|" -f '+'\"'+archivoConsulta+'.sql" > "'+archivoConsulta+'.csv"'      
    os.system(Cadena)


def consulta_de_archivo(servidor,base,usuario,passe,rutaDeScript,nombreConsulta):
    """Esta función consulta desde un archivo.sql a un servidor específico"""
    print('Consultando '+nombreConsulta+'.sql')
    archivoConsulta = os.path.join(rutaDeScript,nombreConsulta)
    Cadena='export PGPASSWORD="'+passe+'"; '+'psql -h '+servidor+' -U '+usuario+' -d '+base+' -A -F"|" -f '+'\"'+archivoConsulta+'.sql" > "'+archivoConsulta+'.csv"'      
    os.system(Cadena)
    #archivos.csv_to_xlsx(rutaDeScript+'\\',nombreConsulta+'.csv',nombreConsulta)

def consulta_de_archivo_v2(servidor,base,usuario,passe,rutaDeScript,nombreConsulta):
    """Esta función consulta desde un archivo.sql a un servidor específico"""    
    archivoConsulta = os.path.join(rutaDeScript,nombreConsulta)
    Cadena='psql -h '+servidor+' -p '+passe+' -U '+usuario+' -d '+base+' -A -F"|" -f '+'\"'+archivoConsulta+'.sql" > "'+archivoConsulta+'.csv"'      
    os.system(Cadena) 

def consulta_de_archivo_v1(servidor,base,usuario,passe,rutaDeScript,nombreConsulta):
    """Esta función consulta desde un archivo.sql a un servidor específico"""    
    archivoConsulta = os.path.join(rutaDeScript,nombreConsulta)
    Cadena='export PGPASSWORD="'+passe+'"; '+'psql -h '+servidor+' -U '+usuario+' -d '+base+' -A -F"|" -f '+'\"'+archivoConsulta+'.sql" > "'+archivoConsulta+'.csv"'      
    os.system(Cadena)        
    #archivos.csv_to_xlsx(rutaDeScript+'\\',nombreConsulta+'.csv',nombreConsulta)

def consulta_de_lista_v3(servidor,base,usuario,passe,rutaDeScript,listadeConsultas):
    """Esta función realiza consultas a partir de un archivo.dat
    que a su ves contiene  una lista de consultas
    """
    print("Barriendo ",listadeConsultas)
    
    #archivoConsulta=rutaDeScript+'\\'+listadeConsultas
    archivoConsulta=os.path.join(rutaDeScript,listadeConsultas)
    infile = open(archivoConsulta,'r')
    Consultas = infile.readlines()
    infile.close()
    for nombreConsulta in Consultas:
        nombreConsulta=nombreConsulta.rstrip('\n')
        consulta_de_archivo_v3(servidor,base,usuario,passe,rutaDeScript,nombreConsulta) 


def consulta_de_lista(servidor,base,usuario,passe,rutaDeScript,listadeConsultas):
    """Esta función realiza consultas a partir de un archivo.dat
    que a su ves contiene  una lista de consultas
    """
    print("Barriendo ",listadeConsultas)
    
    #archivoConsulta=rutaDeScript+'\\'+listadeConsultas
    archivoConsulta=os.path.join(rutaDeScript,listadeConsultas)
    infile = open(archivoConsulta,'r')
    Consultas = infile.readlines()
    infile.close()
    for nombreConsulta in Consultas:
        nombreConsulta=nombreConsulta.rstrip('\n')
        consulta_de_archivo(servidor,base,usuario,passe,rutaDeScript,nombreConsulta)         

def consulta_de_lista_v1(servidor,base,usuario,passe,rutaDeScript,listadeConsultas):
    """Esta función realiza consultas a partir de un archivo.dat
    que a su ves contiene  una lista de consultas
    """     
     
    archivoConsulta=os.path.join(rutaDeScript,listadeConsultas)
    infile = open(archivoConsulta,'r')
    Consultas = infile.readlines()
    infile.close()
    barra = tqdm(Consultas) 
    for nombreConsulta in barra:        
        nombreConsulta=nombreConsulta.rstrip('\n')
        barra.set_description("Consultando %s" % nombreConsulta)
        consulta_de_archivo_v1(servidor,base,usuario,rutaDeScript,nombreConsulta)   
def consulta_de_lista_v2(servidor,base,usuario,passe,rutaDeScript,listadeConsultas):
    """Esta función realiza consultas a partir de un archivo.dat
    que a su ves contiene  una lista de consultas
    """     
     
    archivoConsulta=os.path.join(rutaDeScript,listadeConsultas)
    infile = open(archivoConsulta,'r')
    Consultas = infile.readlines()
    infile.close()
    barra = tqdm(Consultas) 
    for nombreConsulta in barra:        
        nombreConsulta=nombreConsulta.rstrip('\n')
        barra.set_description("Consultando %s" % nombreConsulta)
        consulta_de_archivo_v2(servidor,base,usuario,passe,rutaDeScript,nombreConsulta)               

def consultatoMem(consulta,base,servidor,usuario,passe):
    """
    Ejecuta una consulta y regresa los datos solicitados en un cursor
    """
    try:
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        connect_str = 'dbname='+base+' user='+usuario+' host='+servidor+' password='+passe
        conn = psycopg2.connect(connect_str)
        conn.set_client_encoding('ISO 8859-1')        
        cur=conn.cursor (cursor_factory=psycopg2.extras.DictCursor)         
        cur.execute(consulta)
        res = cur.fetchall()
        return res        
    except Exception as e:                
        print(e) 
def consultaArchivotoMem(servidor,base,usuario,passe,rutaDeScript,fileconsulta):
    """
    Consulta un Archivo
    """
    archivoc = os.path.join(rutaDeScript,fileconsulta)    
    archivo = open(archivoc, 'r')
    CadDatos = archivo.read()
    archivo.close()   
    MemDatos = consultatoMem(CadDatos,base,servidor,usuario,passe)     
    return MemDatos          