# ENERS_iCalendar

## О проекте

Данный демо-проект демонстрирует процесс интегрирования учебного расписания КГЭУ () в ваше приложение для календаря (не предназначен для личного пользования). 

Написанная программа собирает данные из сайта eners.kgeu.ru (без лишней нагрузки на сервер), и формирует файл iCalendar для дальнейшего импорта в различные календарные сервисы:
- Google Календарь
- Яндекс Календарь
- Microsoft Outlook и многие другие...

### Существующие сервисы расписания

Среди основных имеющихся сервисов существуют две основные платформы:
- веб-приложение - [eners.kgeu.ru](https://eners.kgeu.ru/)
- Мобильное приложение - КГЭУ ЭИОС __(Не доступно пользователям продукции Apple)__

### Webcal и чем он полезен
#### Webcal

Webcal - это схема унифицированного идентификатора ресурса (URI) для доступа к файлам iCalendar. WebCal позволяет создавать и поддерживать интерактивный календарь событий или систему планирования на веб-сайте или в приложении.

Схема webcal была разработана для использования в приложении Apple iCal и стала общим стандартом де-факто для доступа к файлам формата iCalendar через WebDAV, обычно с использованием метода GET. Это не официальная схема URI, такие как http и ftp, зарегистрированные в IANA. По состоянию на 23 сентября 2012 года схема webcal имеет временный статус в IANA. Префикс протокола Webcal используется для запуска внешнего обработчика протокола, которому передается URL-адрес файла .ics, а не загруженное содержимое файла, точно так же, как feed иногда используется для запуска внешних RSS-ридеров. Идея заключается в том, что с таким префиксом протокола целевой файл должен быть подписан, а не импортирован в приложение календаря, как это произошло бы при простой загрузке. (Источник: [wikipedia](https://en.wikipedia.org/wiki/Webcal))

#### Польза

Так как сервис [eners.kgeu.ru](https://eners.kgeu.ru/) не требует регистрации, то __webcal__ может принести гораздо больше пользы для пользователя (и для преподавателей), и для этого нет необходимости создавать отдельное приложение, а позволить пользователю работать с прекрасным инструментом планирования (да-да, я сейчас про календарь), который у него уже имеется

### Преимущества данной разработки перед уже существующими

- **Экосистема**. Нет необходимости создавать отдельной приложение. Пользователь может импортировать к себе в учетную запись данный календарь, и все события будут отображаться на всех устройствах с данной учетной записью (ПК, мобильные телефоны, умные-часы, умные-колонки)

- **Иммерсивность**: Расписание будет отображаться вместе с уже существующими событиями пользователя, создавая больший эффект присутствия для пользователя в своих событиях. Определение [иммерсивности](https://ru.wiktionary.org/wiki/%D0%B8%D0%BC%D0%BC%D0%B5%D1%80%D1%81%D0%B8%D0%B2%D0%BD%D0%BE%D1%81%D1%82%D1%8C)

- **Свобода** выбора приложения для клиента. Данная разработка ничем не ограничивает пользователя использовать то приложение, которое ему удобно, тем самым пользователю **предоставляется не приложение для просмотра расписания, а само расписание**

- **Удобный интерфейс**. Интерфейс любого календаря удобнее, нежели в уже существующих разработках

- **Уведомления**, которые пользователь может настраивать сам!!!

### Но все же не все так просто...

Единственной проблемой данного решения является то, что есть те, кому необходимо просто узнать состояние и описание одного события: кто сейчас будет вести пару в кабенете "X", где я могу найти преподавателя "X" и т.п. . В данном случае webcal будет излишней затеей, но он никак не будет мешать уже существующим сервисам, и другие сервисы ему мешать не будут.

## Установка

Установить необходимые библиотеки:
``` zsh
  $ cd ENERS_iCalendar
  $ pip install -r requirements.txt 
```

После этого можете увидеть список команд:
``` zsh
  $ python vical.py --help
```
