import os
import tkinter
import tkinter.scrolledtext as st
from tkinter import *
from tkinter import messagebox as m
from tkinter import ttk

from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk
from PIL import ImageTk, Image

import steno.hover as ho
import steno.text as txt
import steno.audio as aud
import steno.database as db
import steno.image as image_

buttonColor = '#0762f5'
buttonfgColor = '#ffffff'
whiteBg = '#ffffff'
blackBg = '#000000'
blueColor = '#4681f4'
redColor = '#bf222a'

def text_steno():
    """The text steganography function this includes both encoding and decoding"""
    win = Toplevel(master=root, bg=whiteBg)
    win.title('Text Steno')
    win.geometry('480x410')
    win.wm_iconbitmap('images/l2.ico')
    

    win_label = Label(win, text='Text -Steganography', font=cas_big, bg=whiteBg, fg=blackBg)
    win_label.place(x=5, y=4)

    optionLabel = Label(win, text='Would you like to Encode or Decode? ', font=cas_big, bg=whiteBg, fg=blackBg)
    optionLabel.place(x=5, y=300)
    def encode():
        """encoding function for text files"""
        global choice_button, infile_loc
        outfile_loc, m_or_f = '', ''

        size_label = Label(win, text='Select File:', font=cas, bg=whiteBg, fg=blackBg)
        size_label.place(x=5, y=45)
        es = Entry(win, width=50, font=cas)
        es.place(x=7, y=65)

        def browse():
            """Opens a prompt for selecting files"""
            global infile_loc
            infile_loc = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File to DECODE',
                                         filetypes=[('Text files', '.txt')], defaultextension='.txt')
            es.delete(0, END)
            es.insert(0, infile_loc)
            size_label.config(text='Selected File:')

        se_bu = Button(win, text='Browse', bg=blueColor, fg=whiteBg, font=cas, command=browse, relief='ridge')
        se_bu.place(x=411, y=61)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        # TODO add a widget where user will be able to see contents of their chosen file

        ch_lb = Label(win, text='Select what you want to hide', bg=whiteBg, fg=blackBg, font=cas)
        ch_lb.place(x=5, y=85)
        select = StringVar(win)
        style = ttk.Style()
        style.configure('C.TRadiobutton', font=cas, background=whiteBg, foreground=blackBg)

        message_ch = ttk.Radiobutton(win, text='Hide a Message', value="1", variable=select, style='C.TRadiobutton')
        message_ch.place(x=5, y=105)

        choice_file = ttk.Radiobutton(win, text='Hide a File', value="2", variable=select, style='C.TRadiobutton')
        choice_file.place(x=5, y=130)

        password_ = Entry(win, width=20, show='*', font=cas, state=DISABLED)
        password_.place(x=10, y=185)

        def choice():
            """Here the user's choice is evaluated & accordingly work is done"""
            global choice_button
            if select.get() == "1":
                """If the user chooses to enter a message a text prompt is opened"""
                message = Toplevel(master=win)
                message.title('Enter Message')
                message.resizable(False, False)
                message.wm_iconbitmap('images/l2.ico')
                lm = Label(message, text='Enter your message that you want to hide:', bg='yellow', font=cas)
                lm.pack(side=TOP, fill=BOTH)
                ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
                t = st.ScrolledText(message)
                t.config(font=cas)
                t.pack()

                def click(event=None):
                    """Here we collect whatever message the user entered"""
                    global m_or_f
                    message.withdraw()
                    m_or_f = t.get("1.0", "end-1c")
                    # after getting message we allow the user to enter password
                    password_.config(state=NORMAL)
                    password_.focus()

                bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg=blueColor, font=cas)
                bm.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
                message.bind('<Control-b>', click)
                choice_button.config(state=DISABLED)
                refresh.config(state=NORMAL)

            elif select.get() == "2":
                """If user chooses to encode a file then select file prompt opens up"""
                global m_or_f
                m.showinfo('Procedure', 'Select the file which contains\nthe data you want to encode.')
                m_or_f = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File',
                                         filetypes=[('Text files', '.txt')], defaultextension='.txt')
                choice_button.config(state=DISABLED)
                refresh.config(state=NORMAL)
                password_.config(state=NORMAL)
                password_.focus()

        choice_button = Button(win, text='Select', command=choice, bg=blueColor, font=cas, relief='ridge')
        choice_button.place(x=152, y=122)
        ho.CreateToolTip(choice_button, 'Opens a prompt according\nto your chosen option.')

        def process():
            """Here the password's eyes show & hide functions are carried out"""
            if password_["state"] == ACTIVE or password_['state'] == NORMAL:
                if password_["show"] == '*':
                    password_.config(show="")
                    pass_button.config(image=img2)
                elif password_["show"] == "":
                    password_.config(show='*')
                    pass_button.config(image=img)

        pass_label = Label(win, text='Set password:', font=cas, bg=whiteBg, fg='#1046b3')
        pass_label.place(x=10, y=155)

        pass_button = Button(win, image=img, relief='ridge', bg=whiteBg, command=process)
        pass_button.place(x=195, y=180)
        ho.CreateToolTip(pass_button, 'Show/ Hide password')
        success = Label(win, bg='#c0ed98', font=cas, fg='red')
        success.place(x=20, y=280)

        def execute():
            """Main function which checks the requirements and encodes data accordingly"""
            global outfile_loc, m_or_f
            m.showinfo('Procedure', 'It will be embeded and saved in the same file provided!!')
            outfile_loc = infile_loc
            if password_.get() != '' and infile_loc != '' and outfile_loc != '' and m_or_f != '' and es.get() != '':
                if select.get() == '1':
                    try:
                        txt.encode(passwd=password_.get(), infile=es.get(), outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password_.get(), infile=infile_loc, outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                elif select.get() == '2':
                    try:
                        txt.encode(passwd=password_.get(), infile=es.get(), outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file\n{} in\n{}'.format(m_or_f, outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password_.get(), infile=infile_loc, outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file\n{} in\n{}'.format(m_or_f, outfile_loc))
            else:
                m.showerror('ERROR', 'Something went wrong\ntry again.')

        main = Button(win, text='Hide Data', command=execute, bg=blueColor, relief='ridge', font=cas)
        main.place(x=20, y=250)
        ho.CreateToolTip(main, 'Checks everything\nthen encodes the data')

        # TODO show contents of file after encoding[optional]

        def refresh():
            """If the user wants to again choose the options"""
            if choice_button['state'] == DISABLED:
                choice_button.config(state=NORMAL)

        refresh = Button(win, text='Refresh', command=refresh, state=DISABLED, relief='ridge', font=cas, bg=blueColor, fg=whiteBg)
        refresh.place(x=360, y=122)
        ho.CreateToolTip(refresh, 'Refreshes Page')

    def decode():
        """Decoding function for text files"""
        global file_loc
        dec = Toplevel(master=root, bg=whiteBg)
        dec.title('Text Steno Decode File')
        dec.geometry('800x250')
        dec.wm_iconbitmap('images/l2.ico')
        dec_label = Label(dec, text='Text -Steganography (Decode the file for the message)', font=cas_big, bg=whiteBg, fg=blackBg)
        dec_label.place(x=5, y=4)
        info_label = Label(dec, text='Select File:', font=cas, bg=whiteBg, fg=blackBg)
        info_label.place(x=5, y=60)
        file_ent = Entry(master=dec, width=50, font=cas)
        file_ent.place(x=7, y=85)

        def browse():
            """Opens a prompt for selecting files"""
            global file_loc
            file_loc = askopenfilename(parent=dec, initialdir=os.getcwd(), title='Select File to DECODE',
                                       filetypes=[('Text files', '.txt')], defaultextension='.txt')
            file_ent.delete(0, END)
            file_ent.insert(0, file_loc)
            info_label.config(text='Selected File:')

        se_bu = Button(dec, text='Browse', bg=blueColor, fg=whiteBg, font=cas, command=browse, relief='ridge')
        se_bu.place(x=410, y=82)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        pass_lb = Label(dec, text='Enter password:', bg=whiteBg, fg=blackBg, font=cas)
        pass_lb.place(x=5, y=110)
        pass_ent = Entry(dec, width=20, font=cas, show='*')
        pass_ent.place(x=7, y=135)
        pass_ent.focus()

        def show():
            """Here the password's eyes show & hide functions are carried out"""
            if pass_ent["state"] == ACTIVE or pass_ent['state'] == NORMAL:
                if pass_ent["show"] == '*':
                    pass_ent.config(show="")
                    pass_bu.config(image=img2)
                elif pass_ent["show"] == "":
                    pass_ent.config(show='*')
                    pass_bu.config(image=img)

        pass_bu = Button(dec, image=img, command=show, bg=blueColor, fg=whiteBg, relief='ridge')
        pass_bu.place(x=190, y=130)
        ho.CreateToolTip(pass_bu, 'Show/ Hide password')

        def work(event=None):
            """Here after collecting the requirements decoding is carried out"""
            global data
            try:
                data = txt.decode(passwd=pass_ent.get(), file=file_ent.get())
            except FileNotFoundError:
                data = txt.decode(passwd=pass_ent.get(), file=file_loc)
            finally:
                text_win = Toplevel(dec)
                text_win.title('Decoded Message')
                text_win.resizable(False, False)
                text_win.wm_iconbitmap('images/l2.ico')
                show_lb = Label(text_win, text='The message hidden in the selected file:',
                                bg=whiteBg, fg='red', font=cas)
                show_lb.pack(side=TOP, fill=BOTH)
                ho.CreateToolTip(show_lb, "Can't understand what's decoded\nthen your password is WRONG")
                show_text = st.ScrolledText(text_win)
                show_text.pack()
                show_text.tag_configure('beauty', font=cas)
                show_text.insert(INSERT, data, 'beauty')
                show_text.config(state=DISABLED)
                show_bu = Button(text_win, text='Exit', bg=blueColor, fg='red',
                                 command=text_win.destroy, font=cas)
                show_bu.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(show_bu, 'Closes the window')

        def forgotten():
            global path
            foo = Toplevel(dec, bg=whiteBg)
            foo.title('Forgot Password')
            foo.geometry('420x300')
            foo.wm_iconbitmap('images/l2.ico')
            f_lb = Label(foo, text='Forgot Password Recovery', font=cas_big, fg=blackBg, bg=whiteBg)
            f_lb.place(x=5, y=5)
            uname_lb = Label(foo, text='Enter Admin username:', fg=blackBg, bg=whiteBg, font=cas).place(x=5, y=50)
            uname_ent = Entry(foo, font=cas, width=20)
            uname_ent.place(x=180, y=50)
            pwd_lb = Label(foo, text='Enter Admin Password:', fg=blackBg, bg=whiteBg, font=cas).place(x=5, y=80)
            pwd_ent = Entry(foo, font=cas, width=20, show='*')
            pwd_ent.place(x=180, y=80)
            file2 = Label(foo, text='Enter file Path:', fg=blackBg, bg=whiteBg, font=cas).place(x=5, y=110)
            file_new = Entry(foo, font=cas, width=51)
            file_new.place(x=5, y=140)

            def browse_txt():
                """Opens a prompt for selecting files"""
                global path
                path = askopenfilename(parent=foo, initialdir=os.getcwd(), title='Select File to DECODE',
                                       filetypes=[('Text files', '.txt')], defaultextension='.txt')
                file_new.delete(0, END)
                file_new.insert(0, path)

            def check(event=None):
                dt = db.main_work(uname_ent.get(), pwd_ent.get(), path)
                if len(dt) < 2:
                    show_label.config(text=dt[0], font=cas_big)
                else:
                    dt1, dt2 = dt
                    state = 'Hi {} the password for the\nchosen file is:- {}'.format(dt1, dt2[0])
                    show_label.config(text=state, font=cas)

            def show_txt():
                """Here the password's eyes show & hide functions are carried out"""
                if pwd_ent["state"] == ACTIVE or pwd_ent['state'] == NORMAL:
                    if pwd_ent["show"] == '*':
                        pwd_ent.config(show="")
                        pass_bu2.config(image=img2)
                    elif pwd_ent["show"] == "":
                        pwd_ent.config(show='*')
                        pass_bu2.config(image=img)

            pass_bu2 = Button(foo, image=img, command=show_txt, bg=blueColor, fg=whiteBg, relief='ridge')
            pass_bu2.place(x=350, y=70)
            ho.CreateToolTip(pass_bu, 'Show/ Hide password')

            fo_br = Button(foo, text='Browse', font=cas, bg=blueColor, fg=whiteBg, command=browse_txt, relief='flat')
            fo_br.place(x=354, y=161)
            ho.CreateToolTip(fo_br, 'Browse & select files')
            check2 = Button(foo, text='Check & Retrieve', font=cas, bg=blueColor, fg=whiteBg, command=check)
            check2.place(x=25, y=200)
            ho.CreateToolTip(check2, 'Checks everything & gives password')
            show_label = Label(foo, text='', bg=whiteBg, fg=blackBg, font=cas_big)
            show_label.place(x=10, y=230)
            foo.bind('<Return>', check)

        decode_main = Button(dec, text='Decode', relief='ridge', bg=blueColor, fg=whiteBg, font=cas, command=work)
        decode_main.place(x=10, y=190)
        ho.CreateToolTip(decode_main, 'Checks the requirements then\nshows the decoded data.')
        forgot = Button(dec, text='Forgot Password', relief='ridge', bg=blueColor, fg=whiteBg, font=cas, command=forgotten)
        forgot.place(x=150, y=200)
        ho.CreateToolTip(forgot, 'This helps you retrieve\nforgotten if you have admin account.')
        exit_dec = Button(dec, text='Exit', bg=redColor, fg=whiteBg, font=cas, relief='ridge',
                          command=dec.destroy)
        exit_dec.place(x=360, y=200)
        ho.CreateToolTip(exit_dec, 'Closes the window')
        dec.bind('<Return>', work)

    encoding = Button(win, text='Encode data', command=encode, relief='ridge', font=cas, bg=blueColor, fg=whiteBg)
    encoding.place(x=40, y=360)
    ho.CreateToolTip(encoding, 'Encoding data function')
    decoding = Button(win, text="Decode data", command=decode, relief='ridge', font=cas, bg=blueColor, fg=whiteBg)
    decoding.place(x=180, y=360)
    ho.CreateToolTip(decoding, "Decoding data function")
    exit_win = Button(win, text='Exit', font=cas, relief='ridge', command=win.destroy, bg=redColor, fg=whiteBg)
    exit_win.place(x=360, y=360)
    ho.CreateToolTip(exit_win, 'Closes the window')


def image_steno():
    """Image steganography function"""
    img_win = Toplevel(master=root, bg='#ffffff')
    img_win.title('Image steno')
    img_win.geometry('515x260')
    img_win.wm_iconbitmap('images/l2.ico')
    im_lb = Label(img_win, text='Image Steganography', bg='#ffffff', fg='#000000', font=cas_big)
    im_lb.place(x=10, y=10)

    def em_img():
        """Image steganography functions"""
        global file, mess
        select_lb = Label(img_win, text='Select File:', font=cas, bg=whiteBg, fg=blackBg)
        select_lb.place(x=5, y=50)
        file_im = Entry(img_win, width=55, font=cas, relief='ridge', bg=whiteBg,fg=blackBg)
        file_im.place(x=7, y=75)
        file_im.place(x=7, y=75)
        file_im.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global file
            file = askopenfilename(parent=img_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                   filetypes=[('Image files', '.png')], defaultextension='.png')
            file_im.delete(0, END)
            file_im.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(img_win, text='Browse', bg=blueColor, font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def pan():
            """Opens message prompt to enter message"""
            global mess
            message = Toplevel(img_win)
            message.title('Enter Message')
            message.resizable(False, False)
            message.wm_iconbitmap('images/l2.ico')
            lm = Label(message, text='Enter your message that you want to hide:', bg=whiteBg, font=cas, fg=blackBg)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=cas, bg=whiteBg, fg=blackBg)
            t.pack()

            def click(event=None):
                """Collects the message entered by user"""
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg=blueColor, font=cas, fg=blackBg)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(img_win, command=pan, text='Enter Message', font=cas, bg=whiteBg, fg=blackBg)
        b.place(x=10, y=100)
        ho.CreateToolTip(b, 'Opens a prompt where you can enter message')
        success = Label(img_win, bg='#edaa82', font=cas)
        success.place(x=10, y=170)

        def done():
            """Main function which asks for saving file location and then embeds the data in image file"""
            global file, mess
            m.showinfo('Procedure', 'Message will be embedded in the chosen image itself and saved in the same location!!!')
            out = file #asksaveasfilename(title='Save your embedded file as', filetypes=[('Image files', '.png')], defaultextension='.png', initialdir=os.getcwd(), parent=img_win)
            if mess != '' and file != '' and file_im.get() != '' and out != '':
                try:
                    image_.encrypt_image(img_path=file, message=mess, new_path=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
                except FileNotFoundError:
                    image_.encrypt_image(img_path=file_im.get(), message=mess, new_path=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(img_win, text='Embed Message', bg='#3a89de', font=cas, command=done)
        main_bu.place(x=10, y=130)
        ho.CreateToolTip(main_bu, 'Checks everything and embeds your data')

    def ex_img():
        """Data extracting function of image steno"""
        global ex_file
        ex_win = Toplevel(root, bg=whiteBg)
        ex_win.title('Image Steno-EXTRACT')
        ex_win.geometry('800x410')
        ex_win.wm_iconbitmap('images/l2.ico')
        ex_lb = Label(ex_win, text='Image -Steganography ( Extract Message from Image)', bg=whiteBg, fg=blackBg, font=cas_big)
        ex_lb.place(x=10, y=10)
        file_lb = Label(ex_win, text='Select File:', font=cas, bg=whiteBg, fg=whiteBg)
        file_lb.place(x=5, y=50)
        file_ex = Entry(ex_win, width=55, font=cas, relief='ridge', bg=whiteBg, fg=blackBg)
        file_ex.place(x=7, y=75)
        file_ex.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global ex_file
            ex_file = askopenfilename(parent=ex_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                      filetypes=[('Image files', '.png')], defaultextension='.png')
            file_ex.delete(0, END)
            file_ex.insert(0, ex_file)
            file_lb.config(text='Selected File:')

        se_bu = Button(ex_win, text='Browse', bg=blueColor, fg=whiteBg, font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def extract_data(event=None):
            """Extracts data from the audio file and shows it in a text box"""
            dat = image_.decrypt_image(img_path=ex_file)
            suc_lb = Label(ex_win, text='Hidden message is:', font=cas, fg=blackBg, bg=whiteBg).place(x=6, y=130)
            sh = st.ScrolledText(ex_win, width=60, height=7, font=cas)
            sh.place(x=8, y=155)
            sh.insert(INSERT, dat)
            sh.config(state=DISABLED)

        ex_bu = Button(ex_win, text='Extract Message', font=cas, command=extract_data, padx=5, pady=5, bg=blueColor, fg=whiteBg)
        ex_bu.place(x=10, y=100)
        ho.CreateToolTip(ex_bu, 'Extracts the hidden \ndata & displays it')
        ex_win.bind('<Return>', extract_data)

        qu_bu = Button(ex_win, text='Exit', font=cas, command=ex_win.destroy, padx=5, pady=5, width=70, bg=redColor, fg=whiteBg)
        qu_bu.place(x=400, y=360, width=50)
        ho.CreateToolTip(qu_bu, 'Exits window')

    bu_en = Button(img_win, text='Embed', font=cas, bg=buttonColor, fg=buttonfgColor, command=em_img, padx=5, pady=5, width = 10)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Embeds data in image file')
    bu_ex = Button(img_win, text='Extract', font=cas, bg=buttonColor, fg=buttonfgColor, command=ex_img, padx=5, pady=5, width = 10)
    bu_ex.place(x=260, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from image file')
    qubu = Button(img_win, text='Exit', font=cas, bg=buttonColor, fg=buttonfgColor, command=img_win.destroy, padx=5, pady=5, width = 10)
    qubu.place(x=410, y=220)
    ho.CreateToolTip(qubu, 'Exits window')


def audio_steno():
    """Audio steganography functions"""
    aud_win = Toplevel(master=root, bg=whiteBg)
    aud_win.title('Audio Steno')
    aud_win.geometry('515x260')
    aud_win.wm_iconbitmap('images/l2.ico')
    au_lb = Label(aud_win, text='Audio -Steganography', bg=whiteBg, fg=blackBg, font=cas_big)
    au_lb.place(x=10, y=10)

    def em_aud():
        """Audio steno's embedding function"""
        global file, mess
        select_lb = Label(aud_win, text='Select File:', font=cas, bg=whiteBg, fg=blackBg)
        select_lb.place(x=5, y=50)
        file_au = Entry(aud_win, width=55, font=cas, relief='ridge')
        file_au.place(x=7, y=75)
        file_au.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global file
            file = askopenfilename(parent=aud_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                   filetypes=[('Audio files', '.wav')], defaultextension='.wav')
            file_au.delete(0, END)
            file_au.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(aud_win, text='Browse', bg=blueColor, fg=whiteBg, font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def pan():
            """Opens message prompt to enter message"""
            global mess
            message = Toplevel(aud_win, bg=blueColor)
            message.title('Enter Message')
            message.resizable(False, False)
            message.wm_iconbitmap('images/l2.ico')
            lm = Label(message, text='Enter your message that you want to hide:', bg=whiteBg, fg=blackBg, font=cas)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=cas, bg=whiteBg, fg=blackBg)
            t.pack()

            def click(event=None):
                """Collects the message entered by user"""
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg=blueColor, fg=whiteBg, font=cas)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(aud_win, command=pan, text='Enter Message', font=cas, bg=blueColor, fg=whiteBg)
        b.place(x=10, y=100)
        ho.CreateToolTip(b, 'Opens a prompt where you can enter message')
        success = Label(aud_win, bg=whiteBg, font=cas)
        success.place(x=10, y=170)

        def done():
            """Main function which asks for saving file location and then embeds the data in audio file"""
            global file, mess
            m.showinfo('Procedure', ' Embeding the message in the same audio file provided!! ')
            out = file #asksaveasfilename(title='Save your embedded file as', filetypes=[('Audio File', '.wav')],defaultextension='.wav', initialdir=os.getcwd(), parent=aud_win)
            if mess != '' and file != '' and file_au.get() != '' and out != '':
                try:
                    aud.embed(infile=file, message=mess, outfile=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
                except FileNotFoundError:
                    aud.embed(infile=file_au.get(), message=mess, outfile=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(aud_win, text='Embed Message', bg=blueColor, fg=whiteBg, font=cas, command=done)
        main_bu.place(x=10, y=130)
        ho.CreateToolTip(main_bu, 'Checks everything and embeds your data')

    def ex_aud():
        """Data extracting function of audio steno"""
        global ex_file
        ex_win = Toplevel(root, bg=whiteBg)
        ex_win.title('Audio Steno-EXTRACT')
        ex_win.geometry('515x310')
        ex_win.wm_iconbitmap('images/l2.ico')
        ex_lb = Label(ex_win, text='Audio -Steganography (Extract hidden message from audio)', bg=whiteBg, fg=blackBg, font=cas_big)
        ex_lb.place(x=10, y=10)
        file_lb = Label(ex_win, text='Select File:', font=cas, bg=whiteBg, fg=blackBg)
        file_lb.place(x=5, y=50)
        file_ex = Entry(ex_win, width=55, font=cas, relief='ridge')
        file_ex.place(x=7, y=75)
        file_ex.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global ex_file
            ex_file = askopenfilename(parent=ex_win, initialdir=os.getcwd(), title='Select a wav File to EMBED',
                                      filetypes=[('Audio files', '.wav')], defaultextension='.wav')
            file_ex.delete(0, END)
            file_ex.insert(0, ex_file)
            file_lb.config(text='Selected File:')

        se_bu = Button(ex_win, text='Browse', bg=blueColor, fg=whiteBg, font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def extract_data(event=None):
            """Extracts data from the audio file and shows it in a text box"""
            dat = aud.extract(ex_file)
            suc_lb = Label(ex_win, text='Hidden message is:', font=cas, fg=blackBg, bg=whiteBg).place(x=6, y=130)
            sh = st.ScrolledText(ex_win, width=60, height=7, font=cas)
            sh.place(x=8, y=155)
            sh.insert(INSERT, dat)
            sh.config(state=DISABLED)

        ex_bu = Button(ex_win, text='Extract Message', fg=whiteBg, bg=blueColor, font=cas, command=extract_data)
        ex_bu.place(x=10, y=100)
        ho.CreateToolTip(ex_bu, 'Extracts the hidden \ndata & displays it')
        ex_win.bind('<Return>', extract_data)

        qu_bu = Button(ex_win, text='Exit', font=cas, fg=whiteBg, bg=blueColor, command=ex_win.destroy)
        qu_bu.place(x=467, y=278)
        ho.CreateToolTip(qu_bu, 'Exits window')

    bu_en = Button(aud_win, text='Embed', font=cas, fg=whiteBg, bg=blueColor, command=em_aud)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Embeds data in audio file')
    bu_ex = Button(aud_win, text='Extract', font=cas, fg=whiteBg, bg=blueColor, command=ex_aud)
    bu_ex.place(x=230, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from audio file')
    qubu = Button(aud_win, text='Exit', font=cas, fg=whiteBg, bg=blueColor, command=aud_win.destroy)
    qubu.place(x=410, y=220)
    ho.CreateToolTip(qubu, 'Exits window')


def password():
    ps = Toplevel(root, bg=whiteBg)
    ps.geometry('400x300+800+200')
    ps.wm_iconbitmap('images/l2.ico')
    ps_lb = Label(ps, text='User Login[backup]', font=cas_big, bg=whiteBg, fg=whiteBg)
    ps_lb.place(x=5, y=5)
    ps_name_lb = Label(ps, text='Enter name:', bg=whiteBg, fg=blackBg, font=cas).place(x=5, y=50)
    ps_name_entry = Entry(ps, width=30, font=cas)
    ps_name_entry.place(x=100, y=50)
    ps_username_lb = Label(ps, text='Enter\nusername:', bg=whiteBg, fg=blackBg, font=cas).place(x=9, y=80)
    ps_username_entry = Entry(ps, width=30, font=cas)
    ps_username_entry.place(x=100, y=100)
    ps_pass = Label(ps, text='Enter\npassword:', bg=whiteBg, fg=blackBg, font=cas).place(x=9, y=130)
    ps_pass_entry = Entry(ps, width=25, font=cas, show='*')
    ps_pass_entry.place(x=100, y=150)

    def ok_done(event=None):
        db.new(ps_name_entry.get(), ps_username_entry.get(), ps_pass_entry.get())
        suc_lb.config(text='Done!!')

    ps_button = Button(ps, text='Done', font=cas, command=ok_done, fg=whiteBg, bg=blueColor)
    ps_button.place(x=350, y=250)
    suc_lb = Label(ps, text='', font=cas_big, bg=whiteBg, fg=blackBg)
    suc_lb.place(x=150, y=200)

    def show():
        """Here the password's eyes show & hide functions are carried out"""
        if ps_pass_entry["show"] == '*':
            ps_pass_entry.config(show="")
            pass_bu.config(image=img2)
        elif ps_pass_entry["show"] == "":
            ps_pass_entry.config(show='*')
            pass_bu.config(image=img)

    pass_bu = Button(ps, image=img, command=show, bg='#36f5eb', relief='ridge')
    pass_bu.place(x=310, y=140)
    ho.CreateToolTip(pass_bu, 'Show/ Hide password')
    ho.CreateToolTip(ps_button, 'Sets up your admin account')
    ps.bind('<Return>', ok_done)

root = Tk()

# setting attribute
#root.attributes('-toolwindow', True)
root.title('Stegnography')

root.config(bg=blackBg)
root.resizable(True, False)

icon_filename = 'images/l2'

if "nt" == os.name:
    icon_filename = f"{icon_filename}.ico"
else:
    icon_filename = f"@{icon_filename}.xbm"

root.wm_iconbitmap(icon_filename)

# centering the main window


root_h, root_w = 300, 400
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
x_coor = int((s_w / 2) - (root_w / 2))
y_coor = int((s_h / 2) - (root_h / 2))
root.geometry("{}x{}+{}+{}".format(s_w, s_h, 0, 0))
#root.geometry('350x200')

# defining the fonts used and images
cas = ('Segoe Ui', 10)
cas_big = ('Segoe Ui', 20)
img = PhotoImage(file="images/noshow.png").subsample(4, 4)
img2 = PhotoImage(file="images/show.png").subsample(4, 4)
img3 = PhotoImage(file="images/down.png").subsample(3, 3)

# Create an object of tkinter ImageTk
bgimg = ImageTk.PhotoImage(Image.open("images/mainBg.jpg").resize((s_w, s_h)))
# Create a Label Widget to display the text or Image
label = Label(root, image = bgimg)
label.pack()

lb = Label(root, text="Steganography", font=cas_big, bg=blackBg, fg='#ffffff')
lb.place(x=550, y=100)

lb = Label(root, text="Click on any of these to perform an action:", font=('Seoui UI', 15), bg=blackBg, fg='#ffffff')
lb.place(x=475, y=350)
#y-cordinate for the button
buttony=400

image = Button(root, text='Image Steganography',  bg='#0762f5', command=image_steno, font=cas, padx=5, pady=5, fg=whiteBg)
image.place(x=475, y=buttony)
ho.CreateToolTip(image, 'Click here\nto hide your\ndata in an image file')

audio = Button(root, text='Audio Steganography',  bg='#0762f5', command=audio_steno,font=cas, padx=5, pady=5, fg=whiteBg)
#audio = Button(root, text='Audio\nSteganography', command=audio_steno)
audio.place(x=628, y=buttony)
ho.CreateToolTip(audio, 'Click here\nto hide data in\n an audio file.')

text = Button(root, text='Text Steganography ',bg='#0762f5', command=text_steno, font=cas, padx=5, pady=5, fg=whiteBg)
text.place(x=780, y=buttony)
ho.CreateToolTip(text, 'Click here\nto hide your\ndata in a text file')

uni = Button(root, image=img3, command=password, bg='#00000f', width=20, height=10)
uni.place(x=740, y=120)
ho.CreateToolTip(uni, 'Here you can create\nadmin account to\nretrieve forgotten passwords later.')


root.mainloop()
db.close()
