"""
Parse cube configuration file and create cube parser object which
can be passed to the MdxEngine.
"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os
from collections import OrderedDict

import yaml

from .models import Cube, Dimension, Facts


class ConfigParser:
    """Parse olapy config excel file.

    Config file used if you want to show only some measures, dimensions,
    columns... in excel

    Config file should be under '~/olapy-data/cubes/cubes-config.xml'

    Assuming we have two tables as follows under 'labster' folder

    table 1: stats_line (which is the facts table)

    +----------------+---------+--------------------+----------------------+
    | departement_id | amount  |    monthly_salary  |  total monthly cost  |
    +----------------+---------+--------------------+----------------------+
    |  111           |  1000   |      2000          |    3000              |
    +----------------+---------+--------------------+----------------------+
    | bla  bla bla   |         |                    |                      |
    +----------------+---------+--------------------+----------------------+

    table 2: orgunit (which is a dimension)

    +------+---------------+-----------+------------------+------------------+
    | id   | type          |  name     |  acronym         | other colums.....|
    +------+---------------+-----------+------------------+------------------+
    |  111 | humanitarian  |  humania  | for better life  |                  |
    +------+---------------+-----------+------------------+------------------+
    | bla  | bla   bla     |           |                  |                  |
    +------+---------------+-----------+------------------+------------------+


    Excel Config file Structure example::

        <?xml version="1.0" encoding="UTF-8"?>
        <cubes>
            <!-- if you want to set an authentication mechanism for excel to access cube,
                user must set a token with login url like 'http://127.0.0.1/admin  -->
            <!-- default password = admin -->

            <!-- enable/disable xmla authentication -->
            <xmla_authentication>False</xmla_authentication>

            <cube>
                <!-- cube name => csv folder name or database name -->
                <name>labster</name>

                <!-- source : csv | postgres | mysql | oracle | mssql -->
                <source>csv</source>

                <!-- start building customized star schema -->
                <facts>
                    <!-- facts table name -->
                    <table_name>stats_line</table_name>

                    <keys>
                        <!--
                        <column_name ref="[target_table_name].[target_column_name]">[Facts_column_name]</column_name>
                        -->
                        <column_name ref="orgunit.id">departement_id</column_name>
                    </keys>

                    <!-- specify measures explicitly -->
                    <measures>
                        <!-- by default, all number type columns in facts table, or you can specify them here -->
                        <name>montant</name>
                        <name>salaire_brut_mensuel</name>
                        <name>cout_total_mensuel</name>
                    </measures>
                </facts>
                <!-- end building customized star schema -->

                <!-- star building customized dimensions display in excel from the star schema -->
                <dimensions>
                    <dimension>
                        <!-- if you want to keep the same name for excel display, just use the
                             same name in name and displayName -->
                        <name>orgunit</name>
                        <displayName>Organisation</displayName>

                        <columns>
                            <!-- IMPORTANT !!!!  COLUMNS ORDER MATTER -->
                            <name>type</name>
                            <name>nom</name>
                            <name>sigle</name>
                        </columns>
                    </dimension>
                </dimensions>
                <!-- end building customized dimensions display in excel from the star schema -->
            </cube>
        </cubes>
    """

    def __init__(self, cube_config_file=None):
        """

        :param cube_path: path to cube (csv folders) where config file is located by default
        :param file_name: config file name (DEFAULT = cubes-config.xml)
        :param web_config_file_name: web config file name (DEFAULT = web_cube_config.xml)
        """

        if cube_config_file:
            self.cube_config_file = cube_config_file
        else:
            self.cube_config_file = self._get_cube_path()

    def _get_cube_path(self):
        if 'OLAPY_PATH' in os.environ:
            home_directory = os.environ['OLAPY_PATH']
        else:
            from os.path import expanduser
            home_directory = expanduser("~")

        return os.path.join(home_directory, 'olapy-data', 'cubes', 'cubes-config.yml')

    def config_file_exists(self):
        # type: () -> bool
        """
        Check whether the config file exists or not.
        """
        return os.path.isfile(self.cube_config_file)

    def get_cube_config(self, conf_file=None):
        """
        Construct parser cube obj (which can ben passed to MdxEngine) for excel

        :return: Cube obj
        """

        if conf_file:
            file_path = conf_file
        else:
            file_path = self.cube_config_file

        # try:
        with open(file_path) as config_file:
            config = yaml.load(config_file)

            facts = [
                Facts(
                    table_name=config['facts']['table_name'],
                    keys=dict(zip(config['facts']['keys']['columns_names'],
                                  config['facts']['keys']['refs'])
                              ),
                    measures=config['facts']['measures']
                )
            ]

            dimensions = [
                Dimension(
                    name=dimension['dimension']['name'],
                    displayName=dimension['dimension']['displayName'],
                    columns=OrderedDict(
                        (
                            column['name'],
                            column['name'] if 'column_new_name' not in column else
                            column['column_new_name'],
                        ) for column in dimension['dimension']['columns']
                    ) if 'columns' in dimension['dimension'] else {}
                ) for dimension in config['dimensions']
            ]

        # only one cube right now
        return Cube(
            xmla_authentication=bool(config['xmla_authentication']),
            name=config['name'],
            source=config['source'],
            facts=facts,
            dimensions=dimensions,
        )
        # except BaseException:
        #     raise ValueError('Bad configuration in the configuration file')
