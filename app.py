from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId  #Binario hacer busquedas reapidas desde mongo

import pymongo


MONGO_URI = "mongodb+srv://jessi:NBHD@clustercrud.h9cgmbg.mongodb.net/?retryWrites=true&w=majority"
MONGO_BD = "escuela"
MONGO_COLECCION = "alumnos"

cliente=pymongo.MongoClient(MONGO_URI)
#Conexion a la BD
BD = cliente[MONGO_BD]
#Acceder a la conexion que esta en la BD
coleccion = BD[MONGO_COLECCION]

ID_ALUMNO = ""

#FUNCION MOSTRAR DATOS EN LA TABLA DESDE LA BD
def mostarDatos():
    try:
        #mostrar todos los registros 
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        #Obtener los documentos
        for documento in coleccion.find():
            #Mostrar datos dentro de la tabla
            tabla.insert('',0,text = documento["_id"], values = documento["nombre"])

    #Para la conexion y muestre el mensaje por consola 
        #cliente.server_info()
        #print ('Conexion Exitosa')

    except pymongo.errors.ConnectionFailure as errorConexion:
        print ('Conexio Erronea '+errorConexion)
        


#FUNCION CREAR REGISTRO ->BOTON CREAR
def crearRegistro():
    #Se comprueba si estan esos datos tienen texto
    if len(nombre.get())!=0 and len(sexo.get())!=0 and len(calificacion.get())!=0 :
        try:
            documento = {"nombre":nombre.get(), "sexo":sexo.get(), "calificacion":calificacion.get()}
            #Se va insertar el documento dentro de la coleccion
            coleccion.insert_one(documento)
            messagebox.showinfo(message="Insertado") 

            #limpiar campos
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print ('Error unu '+error)
    else:
        messagebox.showerror(message="Inserte datos >:v ")

    mostarDatos()


#FUNCION EDITAR REGISTRO ->BOTON EDITAR
def editarRegistro():
    global ID_ALUMNO
    if len(nombre.get())!=0 and len(sexo.get())!=0 and len(calificacion.get())!=0 :
        try:
            #Diccionario
            idBuscar = {"_id":ObjectId(ID_ALUMNO)}
            newvalores = {"nombre":nombre.get(),"sexo":sexo.get(), "calificacion":calificacion.get()}
            #Aqui se hace la actualizacion de los datos editados
            coleccion.find_one_and_update(idBuscar, newvalores)
            #messagebox.showinfo(message="Actualizado") 
            #limpiar campos
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)

        except pymongo.errors.ConnectionFailure as error:
            print ('Error '+error)
        
            #Desabilitar botones
    crear["state"] = "normal"
    editar["state"] = "disabled"




#*************************************#
#FUNCION dobleClickTabla
def dobleClickTabla(event):
    #Al dar click en la tabla se va obtener el id
    global ID_ALUMNO
    ID_ALUMNO = str(tabla.item(tabla.selection())["text"])
    #Se busca el documento que tenga ese id
    #print(ID_ALUMNO)
    documento = coleccion.find({"_id":ObjectId(ID_ALUMNO)})[0]
    
    #Que se coloquen los datos en sus recuadros
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    sexo.delete(0,END)
    sexo.insert(0,documento["sexo"])
    calificacion.delete(0,END)
    calificacion.insert(0,documento["calificacion"])
    #Desabilitar botones
    crear["state"] = "disabled"
    editar["state"] = "normal"

#Ventana de TKinter 
ventana = Tk()
tabla = ttk.Treeview(ventana, columns=1)
tabla.grid(row=1, column=0, columnspan=1)
tabla.heading("#0", text="ID")
tabla.heading("#1", text="NOMBRE")

#A la tabla se le agrega el evento de EDITAR
#El metodo bind es como view de ver 
tabla.bind("<Double-Button-1>",dobleClickTabla) #Recibe un doble click

#LABEL
#Nombre
Label(ventana,text="Nombre").grid(row=2, column=0)
nombre = Entry(ventana)
nombre.grid(row=2, column=1)

#Sexo
Label(ventana,text="Sexo").grid(row=3, column=0)
sexo = Entry(ventana)
sexo.grid(row=3, column=1)

#Califi
Label(ventana,text="Calificacion").grid(row=4, column=0)
calificacion = Entry(ventana)
calificacion.grid(row=4, column=1)

#Boton CREAR
crear = Button(ventana, text="Crear Alumno", command=crearRegistro, bg="#93bd9a", fg="black")
crear.grid(row=5, columnspan=2) #Abarca 2 columnas


#Boton Editar
editar = Button(ventana, text="Editar Alumno", command=editarRegistro, bg="#e7c049", fg="black")
editar.grid(row=6, columnspan=2) #Abarca 2 columnas
editar["state"] = "disabled"


mostarDatos()
ventana.mainloop()

