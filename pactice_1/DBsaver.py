temp_bd = [
{
    "id": 1,
    "race": "director",
    "name": "Мартынов Дмитрий",
    "level": 12,
    "profession": {
        "id": 1,
        "title": "Влиятельный человек",
        "description": "Эксперт по всем вопросам"
    },
    "skills":
        [{
            "id": 1,
            "name": "Купле-продажа компрессоров",
            "description": ""

        },
        {
            "id": 2,
            "name": "Оценка имущества",
            "description": ""

        }]
},
{
    "id": 2,
    "race": "worker",
    "name": "Андрей Косякин",
    "level": 12,
    "profession": {
        "id": 1,
        "title": "Дельфист-гребец",
        "description": "Уважаемый сотрудник"
    },
    "skills": []
},
]

import datetime

project_db = [
    {
        "id": 1,
        "username": 'User 1',
        "doing": [
            {
                "id": 1,
                "time_spent": 10,
                "case": {
                    "id": 1,
                    "name": "Case 1",
                    "description": "Simple case with two subcases",
                    "priority": 'super_high',
                    "subcases": [
                        {
                            "id": 1,
                            "what_to_do": "first step of instruction",
                            "comment": "",
                            "deadline": datetime.datetime(year=2024, month=2, day=24, hour=8),
                            "messages": [
                                {
                                    "id": 1,
                                    "seemed": False,
                                }
                            ]
                        },
                        {
                            "id": 2,
                            "what_to_do": "second step of instruction",
                            "comment": "it is as simple as first",
                            "deadline": datetime.datetime(year=2024, month=3, day=1, hour=8),
                            "messages": []
                        }
                    ]
                }
            },
            {
                "id": 2,
                "time_spent": 11,
                "case": {
                    "id": 2,
                    "name": "Case 2",
                    "description": "Also simple case with one subcase",
                    "priority": 'high',
                    "subcases": [
                        {
                            "id": 3,
                            "what_to_do": "the only one step of instruction",
                            "comment": "",
                            "deadline": datetime.datetime(year=2024, month=3, day=13, hour=12),
                            "messages": [
                            ]
                        }
                    ]
                }
            }
        ]
    }
]






