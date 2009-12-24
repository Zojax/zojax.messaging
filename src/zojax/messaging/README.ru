===============
zojax messaging
===============

Сервис персональных сообщений для zojax. Чтобы получить доступ к
сервису сообщений нам нужно получит адаптер IMessageStorage для
IPrincipal. IMessageStorage содержит все сообщения.

Создадим `principal`::

    >>> from zope import interface
    >>> from zope.security.interfaces import IPrincipal

    >>> class Principal(object):
    ...     interface.implements(IPrincipal)
    ...     def __init__(self, id):
    ...         self.id = id

    >>> principal = Principal('bob')

Теперь мы можем получить IMessageStorage::

    >>> from zojax.messaging import interfaces

    >>> storage = interfaces.IMessageStorage(principal)

Мы можем проверить колличество непрочитанных сообщений

    >>> storage.unread
    0

Список различных сервисов сообщений.

    >>> storage.getServiceIds()
    []

Чтобы использовать zojax.messaging нам нужно реализовать два
интерфейса. Во первых IMessageService, этот сервис отвечает за
создание и идентификацию сообщений. И реализацию сообщения.
Для примера мы создадим сервис для приватных сообщений.

Сначало создадим интерфейс и реализация для сообщения::

    >>> from zope import schema

    >>> class IPersonalMessage(interfaces.IMessage):
    ...     
    ...     title = schema.TextLine(
    ...         title = u'Subject',
    ...         default = u'',
    ...         required = True)
    ...     
    ...     text = schema.Text(
    ...         title = u'Cooked',
    ...         required = True)
    ...     
    ...     sender = schema.TextLine(
    ...         title = u'Sender',
    ...         required = True)
    ...     
    ...     replyto = schema.TextLine(
    ...         title = u'Reply to',
    ...         required = True)

    >>> from zojax.messaging import message
    >>> class PersonalMessage(message.Message):
    ...     interface.implements(IPersonalMessage)


Реализация для сервиса::

    >>> from zojax.messaging import service
    >>> class PersonalMessages(service.MessageService):
    ...     
    ...     title = u'Personal messages'
    ...     description = u''
    ...     priority = 1
    ...     
    ...     def create(self, **data):
    ...         message = PersonalMessage(data.get('title',u''))
    ...         message.text = data.get('text',u'')
    ...         message.sender = data.get('sender',u'')
    ...         message.replyTo = data.get('replyTo',u'')
    ...         return message

В этом коде главное метод `create`, zojax.messaging будет вызывать
этот метод для создания сообщения.

Мы должны зарегесрировать 'factory' для нашего сервиса::

    >>> from zope import component
    >>> component.provideUtility(
    ...     PersonalMessages,
    ...     interfaces.IMessageServiceFactory, name='personal-messages')

Теперь мы можем создать персональное сообщение.

    >>> msgId = storage.create(
    ...     u'personal-messages',
    ...     title='Тестовое сообщение.', text='Сообщение', sender='zope.manager')

Сообщение создано и хранится в MessageStorage. При этом создается `IMessageCreateEvent`:

    >>> from zope.component.eventtesting import getEvents
    >>> interfaces.IMessageCreatedEvent.providedBy(getEvents()[-1])
    True
    >>> getEvents()[-1]
    <zojax.messaging.interfaces.MessageCreatedEvent ...>

Мы можем получить сообщение по его `id`

    >>> message = storage.getMessage(msgId)
    >>> isinstance(message, PersonalMessage)
    True

    >>> message.title, message.text, message.sender
    ('\xd0\xa2\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb5 \xd1\x81\xd0\xbe\xd0\xbe\xd0\xb1\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5.', '\xd0\xa1\xd0\xbe\xd0\xbe\xd0\xb1\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5', 'zope.manager')

MessageStorage автоматически создает уникальный id для сообщения, и
устанавливает дату создания сообщения, дата так же используется для
сортировки сообщений.

    >>> message.__id__
    1

    >>> message.__date__
    datetime.datetime(...)


Message readStatus. Мы можем узнать состояния сообщения::

    >>> message.__status__
    True

    >>> storage.unread
    1

Изменения состояния сообщения::

    >>> message.__status__ = False
    >>> storage.unread
    0

Сообщения для каждого сервиса хранятся в отдельных
хранилищах. Название хранилище такое же как и название сервиса::

    >>> messages = storage.getService('personal-messages')
    >>> isinstance(messages, PersonalMessages)
    True

    >>> len(messages)
    1

    >>> message.__id__ in messages
    True

    >>> 99999 in messages
    False

    >>> message is messages.get(message.__id__)
    True

Мы можем удалить сообщение

    >>> storage.remove(message.__id__)

При этом создается `IMessageRemovedEvent`:

    >>> interfaces.IMessageRemovedEvent.providedBy(getEvents()[-1])
    True
    >>> getEvents()[-1]
    <zojax.messaging.interfaces.MessageRemovedEvent ...>


Полная реализация персональных сообщений находится в пакете `zojax.personal.messages`
