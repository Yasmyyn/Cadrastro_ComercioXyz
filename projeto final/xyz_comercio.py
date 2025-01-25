import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk



# conectar ou criar o banco 
def conectar():
    return sqlite3.connect('users1.db')



# criar tabela se ela não existir
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute(''' 
      CREATE TABLE IF NOT EXISTS users1(
             id INTEGER PRIMARY KEY,
             nome TEXT,
             idade INTEGER,
             telefone TEXT,
             email TEXT,
             endereco TEXT             
        )
    ''')
    conn.commit()
    conn.close()



# inserindo dados no banco de dados
def agregar_usuarios():
    nome = entry_nome.get()
    idade = entry_idade.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    endereco = entry_endereco.get()


    if nome and idade:
       conn = conectar()
       c = conn.cursor()
       c.execute('INSERT INTO users1 (nome, idade, telefone, email, endereco) VALUES(?, ?, ?, ?, ?)', (nome, idade, telefone, email, endereco))
       conn.commit()
       conn.close()
       messagebox.showinfo('Inseridos', 'Os dados estão no banco de dados') 
       mostrar_usuarios()
    else:
       messagebox.showerror('Erro', 'Ocorreu um erro, os dados não foram inseridos')



# mostrar dados 
def mostrar_usuarios():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * from users1')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], usuario[5]))
    conn.close()



# deletar dados 
def eliminar_usuario():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        conn = conectar() 
        c = conn.cursor()
        c.execute('DELETE FROM users1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Exito', 'DADOS DELETADOS')
        mostrar_usuarios()
    else:
        messagebox.showerror('Erro', 'Dados não deletados')



def atualizar_usuario():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        novo_nome = entry_nome.get()
        nova_idade = entry_idade.get()
        novo_telefone = entry_telefone.get()
        novo_email = entry_email.get()
        novo_endereco = entry_endereco.get()
        if novo_nome and nova_idade and novo_telefone and novo_email and novo_endereco:
            conn = conectar() 
            c = conn.cursor()
            c.execute('UPDATE users1 SET nome = ?, idade = ?, telefone = ?, email = ?, endereco = ? WHERE id = ?', 
                     (novo_nome, nova_idade, novo_telefone, novo_email, novo_endereco, user_id)) 
            conn.commit()
            conn.close()
            messagebox.showinfo('Exito', 'Dados alterados')
            mostrar_usuarios()
        else:
            messagebox.showerror('Erro', 'Dados não inseridos')
    else:
        messagebox.showwarning('Atenção', 'O dado não foi selecionado')



janela = tk.Tk()
janela.title('Cadrastros Clientes XYZ Comércio')
janela.configure(background='#FFC0CB')


label_nome = tk.Label(janela, text='NOME: ', fg= 'Pink')
label_nome.grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10)


label_idade = tk.Label(janela, text='IDADE: ', fg= 'Pink')
label_idade.grid(row=1, column=0, padx=10, pady=10)
entry_idade = tk.Entry(janela)
entry_idade.grid(row=1, column=1, padx=10, pady=10)


label_email = tk.Label(janela, text='E-MAIL: ', fg= 'Pink') 
label_email.grid(row=2, column=0, padx=10, pady=10)
entry_email = tk.Entry(janela)
entry_email.grid(row=2, column=1, padx=10, pady=10)


label_telefone = tk.Label(janela, text='TELEFONE: ', fg= 'Pink')
label_telefone.grid(row=3, column=0, padx=10, pady=10)
entry_telefone = tk.Entry(janela)
entry_telefone.grid(row=3, column=1, padx=10, pady=10)


label_endereco = tk.Label(janela, text='ENDEREÇO: ', fg= 'Pink')
label_endereco.grid(row=4, column=0, padx=10, pady=10)
entry_endereco = tk.Entry(janela)
entry_endereco.grid(row=4, column=1, padx=10, pady=10)



btn_agregar = tk.Button(janela, text='INSERIR DADOS', command=agregar_usuarios, bg='Lightgreen' , fg='White')
btn_agregar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


btn_atualizar = tk.Button(janela, text='ATUALIZAR DADOS', command=atualizar_usuario, bg='Orange', fg='White' )
btn_atualizar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


btn_deletar = tk.Button(janela, text='DELETAR DADOS', command=eliminar_usuario, bg='Red' ,fg='White')
btn_deletar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)


columns = ('ID', 'NOME', 'IDADE', 'E-MAIL', 'TELEFONE', 'ENDEREÇO')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=8, column=0, columnspan=5, padx=10, pady=10)



for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_usuarios()

janela.mainloop()