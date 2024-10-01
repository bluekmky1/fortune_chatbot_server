class ResponseTemplates:
    def __init__(self, version: str = "2.0"):
        self.version = version

    def simple_text(self, text: str):
        return {
            "version": self.version,
            "template": {
                "outputs": [
                    {
                        "textCard": {
                            "title": text,
                            "buttons": [
                                {
                                    "action": "block",
                                    "label": "운세 보고 할일 추천받기",
                                    "blockId": "66f91a98ef21cb53dd05b5a9"
                                }
                            ]
                        }
                    }
                ],

            }
        }

    def quickReplies(self, text: str, nextBlockId: str, quickReplies: list):
        return {
            "version": self.version,
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": text
                        }
                    },
                ],
                "quickReplies": [
                    {
                        "messageText": reply,
                        "action": "block",
                        "blockId": nextBlockId,
                        "label": reply
                    } for reply in quickReplies
                ]
            }
        }

    def simple_image(self, image_url: str, alt_text: str):
        return {
            "version": self.version,
            "template": {
                "outputs": [
                    {
                        "simpleImage": {
                            "imageUrl": image_url,
                            "altText": alt_text
                        }
                    }
                ]
            }
        }

    def fortune_and_tasks(self, fortune_and_tasks: dict):
        print(fortune_and_tasks)
        return {
            "version": self.version,
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"""오늘의 운세: {fortune_and_tasks['todayFortune']}


1. {fortune_and_tasks['todoDesc'][0]['todo']}
{fortune_and_tasks['todoDesc'][0]['desc']}

2. {fortune_and_tasks['todoDesc'][1]['todo']}
{fortune_and_tasks['todoDesc'][1]['desc']}

3. {fortune_and_tasks['todoDesc'][2]['todo']}
{fortune_and_tasks['todoDesc'][2]['desc']}""",

                        }
                    }
                ]
            }
        }

    def error(self, message: str = "에러가 발생했습니다."):
        return {
            "version": self.version,
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": message
                        }
                    }
                ]
            }
        }
