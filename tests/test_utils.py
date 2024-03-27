import os
import shutil
import unittest
from tidecli.utils import file_handler
from tidecli.models.TaskData import TaskData
from unittest_prettify.colorize import (
    colorize,
    GREEN,
    YELLOW,
    MAGENTA
)

# Testdata for creating filestructure
file_data = [
    {
        "code": "print('Hello World1')",
        "path": "main.py",
        "header": "Tehtävä 1"
    },
    {
        "code": "print('Hello Agora!')",
        "path": "new.py",
        "header": "Tehtävä 1"
    }
]

folder_data = [{'ide_files': {'code': "print('Hello world!')",
                              'path': 'main.py'},
                'task_info': {'header': 'Hello world!',
                              'stem': 'Kirjoita viesti maailmalle',
                              'answer_count': None,
                              'type': 'py'},
                'task_id': '60.pythontesti',
                'document_id': 60,
                'paragraph_id': 'Xelt2CQGvUwL',
                'ide_task_id': 'Tehtävä1'}]

course_data = [
    {
        "course_name": "Ohjelmointikurssi1",
        "course_id": 58,
        "course_path": "/view/courses/ohjelmointikurssi1/ohjelmointikurssi1",
        "demo_paths": [
            {
                "path": "courses/ohjelmointikurssi1/Demot/Demo10"
            },
            {
                "path": "courses/ohjelmointikurssi1/Demot/Demo1"
            }
        ]
    }
]

tasks_data_single = [
    {
        "ide_files": {
            "code": "print('Hello world!')",
            "path": "main.py"
        },
        "task_info": {
            "header": "Tehtävä 1",
            "stem": "Kirjoita viesti maailmalle",
            "answer_count": None,
            "type": "py"
        },
        "task_id": "60.pythontesti",
        "document_id": 60,
        "paragraph_id": "Xelt2CQGvUwL",
        "ide_task_id": "Tehtävä1"
    },
    {
        "ide_files": {
            "code": "print('Hello Joni!')\ndef kissa():\n    print(\"hello\")\n\nkissa()\n",
            "path": "main.py"
        },
        "task_info": {
            "header": "Tehtävä 2",
            "stem": None,
            "answer_count": None,
            "type": "py"
        },
        "task_id": "60.T2",
        "document_id": 60,
        "paragraph_id": "wAOLW5wrjrK4",
        "ide_task_id": "Tehtävä2"
    }
]

tasks_data_multi = [
    {
        "ide_files": [
            {
                "code": "#include <stdio.h>\n#include \"add.h\"\n\nint main() {\n  printf(\"%d\", add(1, 2));\n  return 0;\n}\n",
                "path": "main.cc"
            },
            {
                "code": "\nint add(int a, int b) {\n  return 0;\n}\n",
                "path": "add.cc"
            },
            {
                "code": "\nint add(int a, int b);",
                "path": "add.h"
            }
        ],
        "task_info": {
            "header": "Teht\u00e4v\u00e4 3",
            "stem": "md:\nKorjaa `add.cc`:ssa oleva `add`-funktio niin, ett\u00e4 se summaa\nluvut `a` ja `b`.\n\nKokeile ladata t\u00e4m\u00e4 teht\u00e4v\u00e4 TIMiin ja tutki, milt\u00e4 vastaukset n\u00e4ytt\u00e4v\u00e4t tietokannassa.\n",
            "answer_count": None,
            "type": "cc"
        },
        "task_id": "60.Tehtava3",
        "document_id": 60,
        "paragraph_id": "RDDZdgS1GwDR",
        "ide_task_id": "Teht\u00e4v\u00e419"
    },
    {
        "ide_files": {
            "code": "        System.Console.WriteLine(\"Hello World\");",
            "path": "main.cs"
        },
        "task_info": {
            "header": "Teht\u00e4v\u00e4 5",
            "stem": "HelloHello",
            "answer_count": None,
            "type": "cs"
        },
        "task_id": "60.tehtava5",
        "document_id": 60,
        "paragraph_id": "pukg3h0uynFa",
        "ide_task_id": "Teht\u00e4v\u00e45"
    }
]

metadata_single = [
    {
        "course_name": "Ohjelmointikurssi1",
        "course_id": 58,
        "course_path": "/view/courses/ohjelmointikurssi1/ohjelmointikurssi1",
        "demos": [
            {
                "path": "courses/ohjelmointikurssi1/Demot/Demo10",
                "tasks": []
            },
            {
                "path": "courses/ohjelmointikurssi1/Demot/Demo1",
                "tasks": tasks_data_single
            }
        ]
    }
]

validated_task_data = {
    "header": "Testitehtävä",
    "stem": "Testistemmi",
    "type": "py",
    "task_id": "60.Testitehtävä",
    "par_id": "XX",
    "doc_id": "60",
    "ide_task_id": "testi_tehtävä",
    "task_files": [{
        "content": "print(Hello!)",
        "path": "testi.py",
        "source": ""
    }]
}

# Creating the test files to user home dir
user_home = os.environ['HOME']
test_path = os.path.join(user_home, 'Desktop', 'Ohjelmointikurssi 1/Demo1/Tehtävä 1')


@colorize(color=GREEN)
class TestCreateFiles(unittest.TestCase):
    """Test the creation of multiple files to folder."""
    def test_create_files(self):
        """
        Create all files given in list to folder

        Add metadata files to folder
        """
        file_handler.create_files(
            files=file_data,
            folder_path=test_path,
            demo_path="courses/ohjelmointikurssi1/Demot/Demo1")

        assert os.path.exists(os.path.join(test_path, 'main.py'))
        assert os.path.exists(os.path.join(test_path, 'new.py'))

    def test_overwrite_files(self):
        """
        Overwrite all files given in list in folder.
        """
        changed_file_data = [{
            "code": "print('Changed!')",
            "path": "main.py",
            "header": "Tehtävä 1"
        },
            {
            "code": "print('Also changed!')",
            "path": "new.py",
            "header": "Tehtävä 1"
        }]

        file_handler.create_files(
            files=changed_file_data,
            folder_path=test_path,
            demo_path="courses/ohjelmointikurssi1/Demot/Demo1",
            overwrite=True)

        contents = ''
        with open(os.path.join(test_path, 'main.py'), 'r') as file:
            contents = file.read()
            file.close()
            self.assertEqual(contents, 'print(\'Changed!\')')

        with open(os.path.join(test_path, 'new.py'), 'r') as file:
            contents = file.read()
            file.close()
            self.assertEqual(contents, 'print(\'Also changed!\')')

    def test_single_create_files(self):
        """
        Create single file  to folder
        """
        single_file_data = {
            "code": "print('Single!')",
            "path": "single.py"
        }

        file_handler.create_files(
            files=single_file_data,
            folder_path=test_path,
            demo_path="courses/ohjelmointikurssi1/Demot/Demo1",
            overwrite=True)

        assert os.path.exists(os.path.join(test_path, 'single.py'))
        assert os.path.exists(os.path.join(test_path, 'main.py'))
        assert os.path.exists(os.path.join(test_path, 'new.py'))

    def tearDownClass():
        shutil.rmtree(os.path.join(
            user_home, 'Desktop', 'Ohjelmointikurssi 1'))


@colorize(color=GREEN)
class TestCreateMetadata(unittest.TestCase):
    def test_metadata_file(self):
        """
        Create metadata file to folder for single task
        """
        metadata_path = os.path.join(user_home, 'Desktop', 'Ohjelmointikurssi', 'Demo1', 'Testitehtävä')
        os.makedirs(metadata_path)
        file_handler.write_metadata(metadata_path, '#tehtävä', 'courses/ohjelmointikurssi1/Demot/Demo1', 60, '.py')

        with open(os.path.join(metadata_path, 'metadata.json'), 'r') as file:
            contents = file.read()
            self.assertEqual(
                contents, '{\n    "task_id": "#tehtävä",\n'
                '    "demo_path": "courses/ohjelmointikurssi1/Demot/Demo1",\n'
                '    "doc_id": 60,\n'
                '    "code_language": ".py"\n}')

        assert os.path.exists(os.path.join(metadata_path, 'metadata.json'))

    def tearDownClass():
        shutil.rmtree(os.path.join(user_home, 'Desktop', 'Ohjelmointikurssi'))


@colorize(color=MAGENTA)
class TestCreateDemoTask(unittest.TestCase):
    def test_create_demo_task(self):
        """
        Create a single demo task structure into folder
        """

        data = TaskData(**validated_task_data)
        file_handler.create_demo_task(data, 'Ohjelmointikurssi', 'courses/ohjelmointikurssi1/Demot/Demo1')
        assert os.path.exists(os.path.join(user_home, 'Desktop', 'Ohjelmointikurssi', 'Demo1', 'Testitehtävä', 'metadata.json'))

    def tearDownClass():
        shutil.rmtree(os.path.join(user_home, 'Desktop', 'Ohjelmointikurssi'))


@colorize(color=MAGENTA)
class TestCreateDemoTasks():
    def test_create_demo_tasks():
        """
        Create all demo tasks

        All tasks are created in specified folder under
        a excercise folder
        """
        course = {
            "name": "Ohjelmointikurssi Testi",
            "demo_paths": [
                "courses/ohjelmointikurssi1/Demot/Demo1"
            ]
        }

        file_handler.create_demo_tasks(course)
        assert os.path.exists(os.path.join(user_home, 'Desktop', 'Ohjelmointikurssi', 'Demo1', 'Testitehtävä', 'metadata.json'))

    def tearDownClass():
        shutil.rmtree(os.path.join(user_home, 'Desktop', 'Ohjelmointikurssi'))
