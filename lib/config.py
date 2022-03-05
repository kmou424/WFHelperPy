import configparser as ConfigParser
import os.path
from pathlib import Path


class _CustomConfigParser(ConfigParser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


class ConfigManager:
    writable = None
    config_parser = _CustomConfigParser()

    def __init__(self, filename: str, writable=False):
        self.filename = filename
        self.writable = writable
        self.section = None
        self.__initConfigParser()

    def __initConfigParser(self):
        if not Path(os.path.dirname(self.filename)).exists():
            os.makedirs(os.path.dirname(self.filename))
        if not Path(self.filename).exists():
            self.config_parser.write(open(self.filename, 'w', encoding='utf-8'))
        else:
            self.config_parser.read(self.filename, encoding='utf-8')

    def addComment(self, section, comment):
        content = ''
        for line in open(self.filename, encoding='utf-8'):
            if ('[' + section + ']') in line:
                content += ';' + comment + '\n'
            content += line
        comment_writer = open(self.filename, 'w', encoding='utf-8')
        comment_writer.write(content)
        comment_writer.close()

    def addSection(self, section: str, select=False):
        if self.writable:
            self.config_parser.add_section(section)
        if select:
            return self.selectSection(section)

    def checkoutSection(self, section: str):
        if not self.config_parser.has_section(section):
            self.addSection(section, select=True)
        else:
            self.selectSection(section)
        return self

    def getBoolean(self, option: str, default=False):
        if not self.hasOption(option):
            self.setValue(option, default)
            return default
        return self.config_parser.getboolean(self.section, option)

    def getFloat(self, option: str, default=-1):
        if not self.hasOption(option):
            self.setValue(option, default)
            return default
        return self.config_parser.getfloat(self.section, option)

    def getInt(self, option: str, default=-1):
        if not self.hasOption(option):
            self.setValue(option, default)
            return default
        return self.config_parser.getint(self.section, option)

    def getString(self, option: str, default=''):
        if not self.hasOption(option):
            self.setValue(option, default)
            return default
        return self.config_parser.get(self.section, option)

    def hasOption(self, option: str):
        return self.config_parser.has_option(self.section, option)

    def save(self):
        if self.writable:
            self.config_parser.write(open(self.filename, 'w', encoding='utf-8'))

    def selectSection(self, section: str):
        self.section = section
        return self

    def setValue(self, option: str, value):
        if self.writable:
            self.config_parser.set(self.section, option, str(value))

    def setValueBySection(self, section: str, option: str, value):
        if self.writable:
            self.config_parser.set(section, option, value)

    def removeSection(self, section: str):
        if self.writable:
            self.config_parser.remove_section(section)

    def removeOption(self, option: str):
        if self.writable:
            self.config_parser.remove_option(self.section, option)
