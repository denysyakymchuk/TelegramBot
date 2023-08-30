import logging
from xml.etree.ElementTree import Element, SubElement, tostring


class XMLFormatter(logging.Formatter):
    def format(self, record):
        log_entry = logging.Formatter.format(self, record)

        log_element = Element("log")

        time_element = SubElement(log_element, "time")
        time_element.text = self.formatTime(record)

        level_element = SubElement(log_element, "level")
        level_element.text = record.levelname

        message_element = SubElement(log_element, "message")
        message_element.text = log_entry

        return tostring(log_element, encoding="unicode")


def setup_logging():
    logger = logging.getLogger("xml_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("log.xml")
    file_handler.setLevel(logging.DEBUG)

    xml_formatter = XMLFormatter()
    file_handler.setFormatter(xml_formatter)

    logger.addHandler(file_handler)

    return logger
