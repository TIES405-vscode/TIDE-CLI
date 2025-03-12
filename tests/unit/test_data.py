validate_token_response = {
    "active": True,
    "client_id": "oauth2_tide",
    "token_type": "Bearer",
    "username": "test_user",
    "scope": "profile user_tasks user_courses",
    "aud": "oauth2_tide",
    "exp": 864000,
    "iat": 1713772959,
}

get_profile_test_response = {
    "id": 11111111,
    "emails": [{"email": "test@test.fi", "verified": True}],
    "last_name": "Test",
    "given_name": "Test",
    "real_name": "Test Test",
    "username": "test_user",
}

get_ide_courses_test_response = [
    {
        "name": "Testikurssi",
        "id": 111111,
        "path": "kurssit/testi/test/",
        "tasks": [
            {
                "name": "Demo1",
                "path": "kurssit/testi/test/demot/Demo1",
                "doc_id": 1111111,
            },
            {
                "name": "Demo2",
                "path": "kurssit/testi/test/demot/Demo2",
                "doc_id": 2222222,
            },
        ],
    }
]

get_tasks_by_doc_test_response = [
    {
        "task_files": [
            {
                "task_id_ext": "111.test.test",
                "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
                'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
                "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
                "ohjelman toiminta */\n\n  return 0;\n}",
                "file_name": "test.c",
                "user_input": "3 4 2.5",
                "user_args": "",
            }
        ],
        "path": "kurssit/testi/test/demot/Demo1",
        "header": None,
        "stem": None,
        "type": "cc/input/comtest",
        "task_id": "testi",
        "doc_id": 1,
        "par_id": "asd",
        "ide_task_id": "t1",
    },
    {
        "task_files": [
            {
                "task_id_ext": "222.test.test",
                "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
                'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
                "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
                "ohjelman toiminta */\n\n  return 0;\n}",
                "file_name": "test.c",
                "user_input": "3 4 2.5",
                "user_args": "",
            }
        ],
        "path": "kurssit/testi/test/demot/Demo1",
        "header": None,
        "stem": None,
        "type": "cc/input/comtest",
        "task_id": "testi",
        "doc_id": 2,
        "par_id": "asd",
        "ide_task_id": "t2",
    },
]

get_task_by_ide_task_id_test_response = {
    "task_files": [
        {
            "task_id_ext": "333.test.test",
            "content": '#include <stdio.h>\n\nvoid ohjeet(void)\n{\n  printf("Ohjelma laskee huoneen '
            'pinta-alan ja tilavuuden annettujen tietojen perusteella.");\n\n}\n\n/* Kirjoita '
            "tarvittavat aliohjelmat */\n\nint main(void)\n{\n  ohjeet();\n\n  /* Täydennä "
            "ohjelman toiminta */\n\n  return 0;\n}",
            "file_name": "test.c",
            "user_input": "3 4 2.5",
            "user_args": "",
        }
    ],
    "path": "kurssit/testi/test/demot/Demo1",
    "header": None,
    "stem": None,
    "type": "cc/input/comtest",
    "task_id": "test",
    "doc_id": 3,
    "par_id": "asd",
    "ide_task_id": "t3",
}

get_tasks_by_course_test_response = [
    [
        [
            {
                "task_files": [
                    {
                        "task_id_ext": "75.CSharpHelloWorld.glG1Cy5mfAiQ",
                        "content": 'public class HelloWorld\n{\n    public static void Main()\n    {\n// --- Write your code below this line. ---\n        System.Console.WriteLine("Hello World");\n// --- Write your code above this line. ---\n    }\n}\n',
                        "file_name": "hello.cs",
                        "task_directory": None,
                        "task_type": "cs",
                        "user_input": "",
                        "user_args": "",
                    }
                ],
                "supplementary_files": [
                    {
                        "content": '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup>\n    <OutputType>Exe</OutputType>\n    <TargetFramework>net$(NETCoreAppMaximumVersion)</TargetFramework>\n  </PropertyGroup>\n</Project>\n',
                        "file_name": "t1.csproj",
                        "source": None,
                        "task_directory": None,
                    }
                ],
                "path": "kurssit/tie/ohj2/2025k/demot/demo1",
                "task_directory": None,
                "task_type": None,
                "header": None,
                "stem": None,
                "max_points": 2,
                "type": "cs",
                "task_id": "CSharpHelloWorld",
                "doc_id": 75,
                "par_id": "glG1Cy5mfAiQ",
                "ide_task_id": "t1",
            },
            {
                "task_files": [
                    {
                        "task_id_ext": "75.PythonHelloWorld.zDLesD5M3Qqg",
                        "content": 'print("kissa istuu")\n# --- Write your code below this line. ---\nprint("koira haukkuu")\n# --- Write your code above this line. ---\nprint("hevonen nauraa")\n',
                        "file_name": "animals.py",
                        "task_directory": None,
                        "task_type": "py",
                        "user_input": "",
                        "user_args": "",
                    }
                ],
                "supplementary_files": [
                    {
                        "content": "istuu\nja\nnaukuu\n",
                        "file_name": "kissa.txt",
                        "source": None,
                        "task_directory": None,
                    },
                    {
                        "content": "seisoo ja haukkuu",
                        "file_name": "koira.dat",
                        "source": None,
                        "task_directory": None,
                    },
                ],
                "path": "kurssit/tie/ohj2/2025k/demot/demo1",
                "task_directory": None,
                "task_type": None,
                "header": None,
                "stem": None,
                "max_points": None,
                "type": "py",
                "task_id": "PythonHelloWorld",
                "doc_id": 75,
                "par_id": "zDLesD5M3Qqg",
                "ide_task_id": "t2",
            },
            {
                "task_files": [
                    {
                        "task_id_ext": "75.CSharpHelloWorld2.0FimvtLFFJYM",
                        "content": 'public class HelloWorld\n{\n    public static void Main()\n    {\n// --- Write your code below this line. ---\n        System.Console.WriteLine("Hello World");\n// --- Write your code above this line. ---\n    }\n}',
                        "file_name": "hello.cs",
                        "task_directory": None,
                        "task_type": "csharp",
                        "user_input": "",
                        "user_args": "",
                    }
                ],
                "supplementary_files": [
                    {
                        "content": '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup>\n    <OutputType>Exe</OutputType>\n    <TargetFramework>net$(NETCoreAppMaximumVersion)</TargetFramework>\n  </PropertyGroup>\n</Project>\n',
                        "file_name": "t3.csproj",
                        "source": None,
                        "task_directory": None,
                    }
                ],
                "path": "kurssit/tie/ohj2/2025k/demot/demo1",
                "task_directory": None,
                "task_type": None,
                "header": None,
                "stem": None,
                "max_points": None,
                "type": "csharp",
                "task_id": "CSharpHelloWorld2",
                "doc_id": 75,
                "par_id": "0FimvtLFFJYM",
                "ide_task_id": "t3",
            },
        ]
    ],
    [
        [
            {
                "task_files": [
                    {
                        "task_id_ext": "76.CSharpHelloWorld.KVncYJwq6GpS",
                        "content": 'public class HelloWorld\n{\n    public static void Main()\n    {\n// --- Write your code below this line. ---\n        System.Console.WriteLine("Hello World");\n// --- Write your code above this line. ---\n    }\n}',
                        "file_name": "hello.cs",
                        "task_directory": None,
                        "task_type": "cs",
                        "user_input": "",
                        "user_args": "",
                    }
                ],
                "supplementary_files": [
                    {
                        "content": '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup>\n    <OutputType>Exe</OutputType>\n    <TargetFramework>net$(NETCoreAppMaximumVersion)</TargetFramework>\n  </PropertyGroup>\n</Project>\n',
                        "file_name": "33232123.csproj",
                        "source": None,
                        "task_directory": None,
                    }
                ],
                "path": "kurssit/tie/ohj2/2025k/demot/demo2",
                "task_directory": None,
                "task_type": None,
                "header": None,
                "stem": None,
                "max_points": None,
                "type": "cs",
                "task_id": "CSharpHelloWorld",
                "doc_id": 76,
                "par_id": "KVncYJwq6GpS",
                "ide_task_id": "33232123",
            }
        ]
    ],
    [
        [
            {
                "task_files": [
                    {
                        "task_id_ext": "77.CSharpHelloWorld.glG1Cy5mfAiQ",
                        "content": 'public class HelloWorld\n{\n    public static void Main()\n    {\n// --- Write your code below this line. ---\n        System.Console.WriteLine("Hei maailma");\n// --- Write your code above this line. ---\n    }\n}',
                        "file_name": "hello.cs",
                        "task_directory": None,
                        "task_type": "cs",
                        "user_input": "",
                        "user_args": "",
                    }
                ],
                "supplementary_files": [
                    {
                        "content": '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup>\n    <OutputType>Exe</OutputType>\n    <TargetFramework>net$(NETCoreAppMaximumVersion)</TargetFramework>\n  </PropertyGroup>\n</Project>\n',
                        "file_name": "t1.csproj",
                        "source": None,
                        "task_directory": None,
                    }
                ],
                "path": "kurssit/tie/ohj2/2025k/demot/demo3",
                "task_directory": None,
                "task_type": None,
                "header": None,
                "stem": None,
                "max_points": None,
                "type": "cs",
                "task_id": "CSharpHelloWorld",
                "doc_id": 77,
                "par_id": "glG1Cy5mfAiQ",
                "ide_task_id": "t1",
            },
            {
                "task_files": [
                    {
                        "task_id_ext": "77.PythonHelloWorld.zDLesD5M3Qqg",
                        "content": 'print("marsu maiskuttaa")\n',
                        "file_name": "hello.py",
                        "task_directory": None,
                        "task_type": "py",
                        "user_input": "",
                        "user_args": "",
                    }
                ],
                "supplementary_files": [],
                "path": "kurssit/tie/ohj2/2025k/demot/demo3",
                "task_directory": None,
                "task_type": None,
                "header": None,
                "stem": None,
                "max_points": None,
                "type": "py",
                "task_id": "PythonHelloWorld",
                "doc_id": 77,
                "par_id": "zDLesD5M3Qqg",
                "ide_task_id": "t2",
            },
            {
                "task_files": [
                    {
                        "task_id_ext": "77.CSharpLaskuri.cKYZhd0vQk7t",
                        "content": 'public class Counter\n{\n    public static void Main()\n    {\n// --- Write your code below this line. ---\n        System.Console.WriteLine("2 + 2 = 5");\n// --- Write your code above this line. ---\n    }\n}',
                        "file_name": "laskuri.cs",
                        "task_directory": None,
                        "task_type": "cs",
                        "user_input": "",
                        "user_args": "",
                    }
                ],
                "supplementary_files": [
                    {
                        "content": '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup>\n    <OutputType>Exe</OutputType>\n    <TargetFramework>net$(NETCoreAppMaximumVersion)</TargetFramework>\n  </PropertyGroup>\n</Project>\n',
                        "file_name": "t4.csproj",
                        "source": None,
                        "task_directory": None,
                    }
                ],
                "path": "kurssit/tie/ohj2/2025k/demot/demo3",
                "task_directory": None,
                "task_type": None,
                "header": None,
                "stem": None,
                "max_points": None,
                "type": "cs",
                "task_id": "CSharpLaskuri",
                "doc_id": 77,
                "par_id": "cKYZhd0vQk7t",
                "ide_task_id": "t4",
            },
        ]
    ],
]

submit_task_by_id_test_submit = {
    "code_files": [
        {
            "task_id_ext": "1111.test.asd",
            "content": '#include <stdio.h>\n\nint main(void)\n{\n  printf("Hello, World!\\n");\n\n  return '
            "0;\n}",
            "file_name": "test.c",
            "source": "editor",
            "user_input": "",
            "user_args": "",
        }
    ],
    "code_language": "cc",
}

submit_task_by_id_tim_test_response = {
    "result": {
        "web": {
            "console": "Hello, World!\n",
            "error": "",
            "pwd": "",
            "language": None,
            "runtime": "0.883   0.872\nCompile time:\nreal\t0m0.105s\nuser\t0m0.039s\nsys\t0m0.022s\n\nRun "
            "time:\nreal\t0m0.001s\nuser\t0m0.001s\nsys\t0m0.000s\n",
        },
        "savedNew": 111111,
        "valid": True,
    },
    "plugin": None,
}

example_task_cs = """
using System;

namespace HelloWorld
{
    class Program
    {
   
        static void Main(string[] args)
        {
            // --- Write your code below this line. ---


            // Edit an output.
            Console.Writeline("Hello!");

            Console.Writeline("World!");

            // --- Write your code above this line. ---
        }
    }
}

"""

example_task_py = """
class Program:

    @staticmethod
    def main():
        # --- Write your code below this line. ---

        # Edit an output.
        print("Hello, World!")
        print("Hello University also!")
        # --- Write your code above this line. ---
if __name__ == "__main__":
    Program.main()

"""

example_task_metadata_cs = """
using System;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            // --- Write your code below this line. ---

            // Edit an output.
            Console.Writeline("Hello, World!");

            // --- Write your code above this line. ---
        }
    }
}

"""

example_task_metadata_py = """
class Program:
    @staticmethod
    def main():
        # --- Write your code below this line. ---

        # Edit an output.
        print("Hello, World!")

        # --- Write your code above this line. ---
if __name__ == "__main__":
    Program.main()

"""

example_task_broken_cs = """
using System;
using Jypeli;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            // --- Write your code below this line. ---


            // Edit an output.
            Console.Writeline("Hello!");

            Console.Writeline("World!");

            // --- Write your code above this line. ---
        }
    }
}

"""

example_task_none_py = """
class Program:

    @staticmethod
    def main():
        # Edit an output.
        print("Hello, World!")
        print("Hello University also!")

if __name__ == "__main__":
    Program.main()

"""
