import os
import logging
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_ID = "deepseek-ai/DeepSeek-V3-0324"
client = InferenceClient(token=HF_API_TOKEN)

SYSTEM_PROMPT = (
    "Ты анализируешь текст запроса клиента на закупку промышленных труб. "
    "Твоя задача — извлечь из текста следующие параметры и вернуть результат строго в формате JSON со следующими ключами: "
    "\"type_of_pipe\", \"diameter_of_pipe\", \"pipe_wall_thickness\", \"volume_tons\", \"timeline\", \"interest_level\". "

    "Правила извлечения параметров: \n"
    "- \"type_of_pipe\": значение — \"Бесшовная\" или \"Сварная\" труба. Если тип трубы не указан, попробуй определить тип самостоятиельно из контекста (если указана цель для чего нужна труба), иначе укажи null.\n"
    "- \"diameter_of_pipe\": если указан диаметр трубы, классифицируй его как \"До 500 мм\" или \"От 500 мм\". Если не указан — null.\n"
    "- \"pipe_wall_thickness\": если указана толщина стенки, классифицируй её как \"До 15 мм\" или \"До 30 мм\". Если не указана — null.\n"
    "- \"volume_tons\": если указан объём, классифицируй как \"До 100 т.\" или \"От 100 т.\". Если не указан — null.\n"
    "- \"timeline\": если указан срок поставки, классифицируй как \"До месяца\" или \"От месяца\". Если не указан — null.\n"

    "- \"interest_level\": оценивай уровень интереса клиента по следующим правилам:\n"
    "  * Если объём \"До 100 т.\" и срок \"До месяца\" → \"HOT\"\n"
    "  * Если объём \"До 100 т.\" и срок \"От месяца\" → \"WARM\"\n"
    "  * Если объём \"От 100 т.\" и срок \"До месяца\" → \"WARM\"\n"
    "  * Если объём \"От 100 т.\" и срок \"От месяца\" → \"COLD\"\n"
    "Если невозможно определить уровень интереса из-за отсутствующих данных по объёму или сроку — укажи null.\n"

    "Верни результат в строго следующем формате:\n"
    "{\n"
    "  \"type_of_pipe\": значение,\n"
    "  \"diameter_of_pipe\": значение,\n"
    "  \"pipe_wall_thickness\": значение,\n"
    "  \"volume_tons\": значение,\n"
    "  \"timeline\": значение,\n"
    "  \"interest_level\": значение\n"
    "}"
)


SYSTEM_PROMPT_TYPE_OF_PIPE = (
    "Ты анализируешь текст запроса клиента на закупку промышленных труб. "
    "Извлеки параметр \"type_of_pipe\": значение — \"Бесшовная\" или \"Сварная\". Если тип трубы не указан, попробуй определить тип самостоятельно из контекста (если указана цель для чего нужна труба), иначе укажи null. "
    "Верни результат в формате JSON: {\"type_of_pipe\": значение}. "
    "Если в тексте не указан тип трубы, укажи null."
)

SYSTEM_PROMPT_DIAMETER_OF_PIPE = (
    "Ты анализируешь текст запроса клиента на закупку промышленных труб. "
    "Извлеки параметр diameter_of_pipe — диаметр трубы. "
    "Допустимые значения: 'До 500 мм' или 'От 500 мм'. "
    "Верни результат в формате JSON: {\"diameter_of_pipe\": значение}. "
    "Если в тексте не указан диаметр, укажи null."
)



SYSTEM_PROMPT_PIPE_WALL_THICKNESS = (
    "Ты анализируешь текст запроса клиента на закупку промышленных труб. "
    "Извлеки параметр pipe_wall_thickness — толщина стенки трубы. "
    "Допустимые значения: 'До 15 мм' или 'До 30 мм'. "
    "Верни результат в формате JSON: {\"pipe_wall_thickness\": значение}. "
    "Если в тексте не указана толщина стенки, укажи null."
)


SYSTEM_PROMPT_VOLUME_TONS = (
    "Ты анализируешь текст запроса клиента на закупку промышленных труб. "
    "Извлеки параметр volume_tons — объём поставки в тоннах. "
    "Допустимые значения: 'До 100 т.' или 'От 100 т.'. "
    "Верни результат в формате JSON: {\"volume_tons\": значение}. "
    "Если в тексте не указан объём, укажи null."
)


SYSTEM_PROMPT_TIMELINE = (
    "Ты анализируешь текст запроса клиента на закупку промышленных труб. "
    "Извлеки параметр timeline — срок поставки. "
    "Допустимые значения: 'До месяца' или 'От месяца'. "
    "Верни результат в формате JSON: {\"timeline\": значение}. "
    "Если в тексте не указан срок, укажи null."
)


#До 100т и до месяца - горячий клиент
#До 100т и больше месяца - тёплый 
#От 100т и до месяца - тёплый
#От 100т и больше месяца - холодный 

def analyze_text(text: str) -> dict:
    prompt = f"{SYSTEM_PROMPT}\nТекст: {text}\nОтвет:"
    logging.info(f"Отправка запроса к Hugging Face через huggingface_hub, модель: {MODEL_ID}")
    logging.info(f"Prompt: {prompt}")
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}]
        )
        logging.info(f"Ответ модели: {completion}")
        content = completion.choices[0].message.content
        logging.info(f"Контент ответа: {content}")

        import json, re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            logging.info(f"Извлечённый JSON: {match.group(0)}")
            parsed = json.loads(match.group(0))

            # Гарантируем наличие всех нужных ключей
            keys = ["type_of_pipe", "diameter_of_pipe", "pipe_wall_thickness", "volume_tons", "timeline", "interest_level"]
            return {key: parsed.get(key, None) for key in keys}
        else:
            logging.warning("JSON не найден в ответе модели.")
            return {
                "type_of_pipe": None,
                "diameter_of_pipe": None,
                "pipe_wall_thickness": None,
                "volume_tons": None,
                "timeline": None,
                "interest_level": None
            }
    except Exception as e:
        logging.error(f"Ошибка при запросе к Hugging Face: {e}")
        return {
            "type_of_pipe": None,
            "diameter_of_pipe": None,
            "pipe_wall_thickness": None,
            "volume_tons": None,
            "timeline": None,
            "interest_level": None
        }



def analyze_single_param(text: str, param_code: str) -> dict:
    PARAM_PROMPTS = {
        "type_of_pipe": SYSTEM_PROMPT_TYPE_OF_PIPE,
        "diameter_of_pipe": SYSTEM_PROMPT_DIAMETER_OF_PIPE,
        "pipe_wall_thickness": SYSTEM_PROMPT_PIPE_WALL_THICKNESS,
        "volume_tons": SYSTEM_PROMPT_VOLUME_TONS,
        "timeline": SYSTEM_PROMPT_TIMELINE
    }

    if param_code not in PARAM_PROMPTS:
        logging.error(f"Неизвестный параметр: {param_code}")
        return {param_code: None}

    prompt = f"{PARAM_PROMPTS[param_code]}\nТекст: {text}\nОтвет:"
    logging.info(f"Отправка запроса для параметра '{param_code}' к Hugging Face. Модель: {MODEL_ID}")
    logging.info(f"Prompt: {prompt}")

    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}]
        )
        content = completion.choices[0].message.content
        logging.info(f"Ответ модели: {content}")

        import json, re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            logging.info(f"Извлечённый JSON: {match.group(0)}")
            return json.loads(match.group(0))
        else:
            logging.warning(f"JSON не найден в ответе модели для параметра {param_code}.")
            return {param_code: None}
    except Exception as e:
        logging.error(f"Ошибка при извлечении параметра '{param_code}': {e}")
        return {param_code: None}
