'''Работа с содержательной частью информационных пакетов запроса НСИ'''

import os
import uuid
import jinja2
import logging
import xml

from dars import datastructs as ds
from dars import (
        models,
        utils,
        xml as dxml,
        )

logger = logging.getLogger('dars')


def render(model: models.GetPublicDocsRequestModel) -> str:
    '''Сгенерировать тело запроса публичных документов

    Аргументы:
        model - модель параметров команды
    '''
    if model.base == ds.Base.FZ223:
        raise NotImplementedError
    path = os.path.join(os.path.dirname(__file__), 'templates')
    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=path))
    template = env.get_template('getpublicdocsrequest.xml.j2')
    template.globals['now'] = utils.isonow
    template.globals['uuid'] = uuid.uuid4
    return template.render(context=model)


def extract_archive_info(xmlstring: str,
                         base: ds.Base = ds.Base.FZ44
                         ) -> list[str]:
    '''Извлечь документы организаций

    Аргументы:
        xmlstring - xml-строка, содержащая пакет данных getPublicDocsRequest
    Результат:
        Список ссылок для скачивания
    '''
    if base == ds.Base.FZ223:
        raise NotImplementedError
    try:
        obj = dxml.XmlObject(xmlstring, root_tag='Body/getPublicDocsResponse')
    except (xml.etree.ElementTree.ParseError, ValueError) as e:
        logger.error('Произошла ошибка при извлечении файла')
        logger.error(e)
        logger.error(xmlstring)
        return []
    # ---
    info_path = 'dataInfo/orgzanizations44DocsInfo/orgzanization44DocsInfo'
    info = []
    for el in obj.values(info_path):
        urls = [url.text for url in obj.values('archiveUrl', root=el)]
        info.extend(urls)
    return info
