"""
Zer-ru — это модуль zer на русском! Для сокращения и автоматизации кода.

Версия модуля: 0.0.5 alpha.
Издатель: ZerProg studio.
"""

import os as oss
import datetime
import sys
from tqdm import tqdm
import random as randam

class DateTime:
    '''Класс DateTime работает с информацией о дате и времени.'''
    def date(separator='-',null=True):
        if null==True:
            Date = ['','']
            if datetime.date.today().day<=9:
                Date[0]='0'
            if datetime.date.today().month<=9:
                Date[1]='0'
            return f'{Date[0]}{datetime.date.today().day}{separator}{Date[1]}{datetime.date.today().month}{separator}{datetime.date.today().year}'
        return f'{datetime.date.today().day}{separator}{datetime.date.today().month}{separator}{datetime.date.today().year}'
    def day(null=True):
        if null==True:
            if datetime.date.today().day<=9:
                return f'0{datetime.date.today().day}'
        return datetime.date.today().day
    def month(null=True):
        if null==True:
            if datetime.date.today().month<=9:
                return f'0{datetime.date.today().month}'
        return datetime.date.today().month
    def year():
        return datetime.date.today().year
    def time(separator='-', null=True):
        if null==True:
            Time = ['','','']
            if datetime.datetime.now().hour<=9:
                Time[0]='0'
            if datetime.datetime.now().minute<=9:
                Time[1]='0'
            if datetime.datetime.now().second<=9:
                Time[2]='0'
            return f'{Time[0]}{datetime.datetime.now().hour}{separator}{Time[1]}{datetime.datetime.now().minute}{separator}{Time[2]}{datetime.datetime.now().second}'
        return f'{datetime.datetime.now().hour}{separator}{datetime.datetime.now().minute}{separator}{datetime.datetime.now().second}'
    def second(null=True):
        if null==True:
            if datetime.datetime.now().second<=9:
                return f'0{datetime.datetime.now().second}'
        return datetime.datetime.now().second
    def minute(null=True):
        if null==True:
            if datetime.datetime.now().minute<=9:
                return f'0{datetime.datetime.now().minute}'
        return datetime.datetime.now().minute
    def hour(null=True):
        if null==True:
            if datetime.datetime.now().hour<=9:
                return f'0{datetime.datetime.now().hour}'
        return datetime.datetime.now().hour
 
class os:
    '''
    Класс os работает с информацией об операционной системе.
    '''
    def nameuser():
        '''Получение имени пользователя.'''
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = oss.environ.get(name)
            if user:
                return user
    def name():
        '''
        Получение названия операционной системы.
        '''
        return oss.uname().sysname
    def namepc():
        '''
        Получение имени компьютера.
        '''
        return oss.uname().nodename
    def version():
        '''
        Получение версии операционной системы.
        '''
        return oss.uname().version

class email:
    '''
    Класс email работает с электронной почтой.
    '''
    def send_gmail(Sender,Password,To,Theme,Text,Info=True):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        '''
        Отправка электронного письма. Поддерживается только Gmail.

        Sender: Email отправителя.
        Pass: Пароль от Email отправителя.
        To: Email получателя.
        Theme: Тема Email.
        Text: Текст Email.
        Info: Если True то выводит в консоль информацию по типу 'отправка...' и 'Письмо было успешно отправлено.'. Ошибки выводятся всегда.
        '''
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(Sender, Password)

            msg = MIMEMultipart()

            msg["Sender"] = Sender
            msg["To"] = To
            msg["Subject"] = Theme

            content = f'{Text}'
            msg.attach(MIMEText(content, "plain"))

            if Info==True:
                print("Отправка...")
            server.sendmail(Sender, To, msg.as_string())

            if Info==True:
                print("Письмо было успешно отправлено.")
            return
        except Exception as error:
            if error.errno==-2:
                print('\033[31mОшибка: не удалось связатся с сервером или указано неверно имя.\033[0;0m')
                return [1,'Ошибка: не удалось связатся с сервером или указано неверно имя.']
            else:
                print(f'\033[31mОшибка: {error}\033[0;0m')
                return [0,f'Ошибка: {error}']

    def send_gmail_files(Sender, Password,To,Theme,text=None, Html=None,Pathfile=None, Info=True):
        '''
        Отправка электронного письма с вложеным HTML и другими файлами. Поддерживается только Gmail.
        
        Sender: Email отправителя.
        Pass: Пароль от Email отправителя.
        To: Email получателя.
        Theme: Тема Email.
        Text: Текст Email.
        Html: Путь к файлу HTML.
        Pathfile: Путь к папке(без папок внутри) с файлами. Поддержка файлов text, image, audio, application...
        Info: Если True то выводит в консоль информацию по типу 'отправка...' и 'Письмо было успешно отправлено.'. Ошибки выводятся всегда.
        '''
        import smtplib
        import mimetypes
        from email import encoders
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.image import MIMEImage
        from email.mime.audio import MIMEAudio
        from email.mime.application import MIMEApplication
        from email.mime.base import MIMEBase

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(Sender, Password)
            msg = MIMEMultipart()
            msg["Sender"] = Sender
            msg["To"] = To
            msg["Subject"] = Theme

            if text:
                msg.attach(MIMEText(text))

            if Html:
                try:
                    with open(Html) as file:
                        Html = file.read()
                except IOError:
                    Html = None
                msg.attach(MIMEText(Html, "html"))

            if Pathfile:
                if Info==True:
                    print("Загрузка файлов...")
                if Pathfile[len(Pathfile)-1]!='/' or Pathfile[len(Pathfile)-1]!='\\':
                    Pathfile+='/'
                for file in tqdm(os.listdir(Pathfile)):
                    try:
                        filename = os.path.basename(file)
                        ftype, encoding = mimetypes.guess_type(file)
                        file_type, subtype = ftype.split("/")
                    except:
                        print('Ошибка распознания файлов.')

                    if file_type == "text":
                        with open(f"{Pathfile}{file}") as f:
                            file = MIMEText(f.read())
                    elif file_type == "image":
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEImage(f.read(), subtype)
                    elif file_type == "audio":
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEAudio(f.read(), subtype)
                    elif file_type == "application":
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEApplication(f.read(), subtype)
                    else:
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEBase(file_type, subtype)
                            file.set_payload(f.read())
                            encoders.encode_base64(file)

                    file.add_header('content-disposition', 'attachment', filename=filename)
                    msg.attach(file)

            if Info==True:
                print("Отправка...")
            server.sendmail(Sender, To, msg.as_string())

            if Info==True:
                print("Письмо было успешно отправлено.")
        except Exception as error:
            if error.errno==-2:
                print('\033[31mОшибка: не удалось связатся с сервером или указано неверно имя.\033[0;0m')
                return [1,'Ошибка: не удалось связатся с сервером или указано неверно имя.']
            else:
                print(f'\033[31mОшибка: {error}\033[0;0m')
                return [0,f'Ошибка: {error}']

    def send_mailru(Sender,Password,To,Theme,Text,Info=True):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        '''
        Отправка электронного письма. Поддерживается только Gmail.

        Sender: Email отправителя.
        Pass: Пароль от Email отправителя.
        To: Email получателя.
        Theme: Тема Email.
        Text: Текст Email.
        Info: Если True то выводит в консоль информацию по типу 'отправка...' и 'Письмо было успешно отправлено.'. Ошибки выводятся всегда.
        '''
        try:
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(Sender, Password)

            msg = MIMEMultipart()

            msg["Sender"] = Sender
            msg["To"] = To
            msg["Subject"] = Theme

            content = f'{Text}'
            msg.attach(MIMEText(content, "plain"))

            if Info==True:
                print("Отправка...")
            server.sendmail(Sender, To, msg.as_string())

            if Info==True:
                print("Письмо было успешно отправлено.")
            return
        except Exception as error:
            if error.errno==-2:
                print('\033[31mОшибка: не удалось связатся с сервером или указано неверно имя.\033[0;0m')
                return [1,'Ошибка: не удалось связатся с сервером или указано неверно имя.']
            else:
                print(f'\033[31mОшибка: {error}\033[0;0m')
                return [0,f'Ошибка: {error}']

    def send_mailru_files(Sender, Password,To,Theme,text=None, Html=None,Pathfile=None, Info=True):
        '''
        Отправка электронного письма с вложеным HTML и другими файлами. Поддерживается только Gmail.
        
        Sender: Email отправителя.
        Pass: Пароль от Email отправителя.
        To: Email получателя.
        Theme: Тема Email.
        Text: Текст Email.
        Html: Путь к файлу HTML.
        Pathfile: Путь к папке(без папок внутри) с файлами. Поддержка файлов text, image, audio, application...
        Info: Если True то выводит в консоль информацию по типу 'отправка...' и 'Письмо было успешно отправлено.'. Ошибки выводятся всегда.
        '''
        import smtplib
        import mimetypes
        from email import encoders
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.image import MIMEImage
        from email.mime.audio import MIMEAudio
        from email.mime.application import MIMEApplication
        from email.mime.base import MIMEBase

        try:
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(Sender, Password)
            msg = MIMEMultipart()
            msg["Sender"] = Sender
            msg["To"] = To
            msg["Subject"] = Theme

            if text:
                msg.attach(MIMEText(text))

            if Html:
                try:
                    with open(Html) as file:
                        Html = file.read()
                except IOError:
                    Html = None
                msg.attach(MIMEText(Html, "html"))

            if Pathfile:
                if Info==True:
                    print("Загрузка файлов...")
                if Pathfile[len(Pathfile)-1]!='/' or Pathfile[len(Pathfile)-1]!='\\':
                    Pathfile+='/'
                for file in tqdm(os.listdir(Pathfile)):
                    try:
                        filename = os.path.basename(file)
                        ftype, encoding = mimetypes.guess_type(file)
                        file_type, subtype = ftype.split("/")
                    except:
                        print('Ошибка распознания файлов.')

                    if file_type == "text":
                        with open(f"{Pathfile}{file}") as f:
                            file = MIMEText(f.read())
                    elif file_type == "image":
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEImage(f.read(), subtype)
                    elif file_type == "audio":
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEAudio(f.read(), subtype)
                    elif file_type == "application":
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEApplication(f.read(), subtype)
                    else:
                        with open(f"{Pathfile}{file}", "rb") as f:
                            file = MIMEBase(file_type, subtype)
                            file.set_payload(f.read())
                            encoders.encode_base64(file)

                    file.add_header('content-disposition', 'attachment', filename=filename)
                    msg.attach(file)

            if Info==True:
                print("Отправка...")
            server.sendmail(Sender, To, msg.as_string())

            if Info==True:
                print("Письмо было успешно отправлено.")
        except Exception as error:
            if error.errno==-2:
                print('\033[31mОшибка: не удалось связатся с сервером или указано неверно имя.\033[0;0m')
                return [1,'Ошибка: не удалось связатся с сервером или указано неверно имя.']
            else:
                print(f'\033[31mОшибка: {error}\033[0;0m')
                return [0,f'Ошибка: {error}']

class random:
    def length(quantity):
        '''
        Генерация случайного числа.

        quantity: количество символов в случайном числе. Максимальное значение 150 символов.
        '''
        if quantity>150:
            return 'Ошибка превышено возможное количество генерируемых чисел.'
        numbers = ''
        coll1 = f'{randam.random()}'
        numbers+= coll1[2:12]
        coll2 = f'{randam.random()}'
        numbers+= coll2[2:12]
        coll3 = f'{randam.random()}'
        numbers+= coll3[2:12]
        if quantity>=31:
            coll4 = f'{randam.random()}'
            numbers+= coll4[2:12]
            coll5 = f'{randam.random()}'
            numbers+= coll5[2:12]
            coll6 = f'{randam.random()}'
            numbers+= coll6[2:12]
        if quantity>=61:
            coll7 = f'{randam.random()}'
            numbers+= coll7[2:12]
            coll8 = f'{randam.random()}'
            numbers+= coll8[2:12]
            coll9 = f'{randam.random()}'
            numbers+= coll9[2:12]
            coll10= f'{randam.random()}'
            numbers+= coll10[2:12]
        if quantity>=101:
            coll11 = f'{randam.random()}'
            numbers+= coll11[2:12]
            coll12 = f'{randam.random()}'
            numbers+= coll12[2:12]
            coll13 = f'{randam.random()}'
            numbers+= coll13[2:12]
            coll14= f'{randam.random()}'
            numbers+= coll14[2:12]
            coll15 = f'{randam.random()}'
            numbers+= coll15[2:12]
        return numbers[0:quantity]

    def from_to(min, max):
        '''
        Генерация случайного числа от минимального значения до максимального.
        
        min: Минимальное число.
        max: Максимальное число.
        '''
        return randam.randint(min, max)

def survey(text, yes, no):
    """
    Вывод вопроса в консоль.

    text: Текст который будет выведен.
    yes: Вариант положительного ответа.
    no: Вариант отрицательного ответа.
    """
    while True:
        inp = input(text)
        inp = inp.strip()
        inp = inp.lower()
        if inp==yes:
            return 'yes'
        if inp==no:
            return 'no'

def opensite(url):
    '''
    Открытие сайта в браузере.
    '''
    strar = url[:5]
    if strar!='https' and strar!='http:':
        temp=url
        url=f'http:/{temp}'
    if oss.name=='posix' or os.name=='Linux':
        oss.system(f"open '{url}'")
    if oss.name=='nt' or os.name=='Windows':
        oss.system(f"start '{url}'")
