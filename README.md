#### Подготовка/запуск
```
$ python3 -m venv .venv
$ # activate
$ pip install -r requirements.txt
$ mkdir -p dest
$ python3 app_main.py im peer:<id собеседника>
```
id можно получить так: если открыть чат, ссылка имеет вид `https://vk.com/im?sel=<ID>`

#### Результат
Фотографии и их список `im_photos.json` в директории `dest` 

#### Важно
На данный момент QtWebEngine крашится при завершении основного процесса.
Однако это не влияет на результат работы - после появления в консоли
сообщения `"MainApplication: all files saved"` все фото уже на диске.
