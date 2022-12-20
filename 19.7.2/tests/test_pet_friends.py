import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_None_email(email="", password=valid_password):
    """Проверяем что запрос api-key возращает статус 403 при пустом поле с email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_api_key_for_None_password(email=valid_email, password=""):
    """Проверяем что запрос api-key возращает статус 403 ппри пустом поле с password"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_api_key_for_not_exist_email(email='0@maeil.ru', password=valid_password):
    """Проверяем что запрос api-key возращает статус 403 при несуществующем email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_api_key_for_wrong_password(email=valid_email, password="wrong_password"):
    """Проверяем что запрос api-key возращает статус 403 при неправильном пароле"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_list_of_pets_wrong_filter(filter='Wrong_Filter'):
    """Проверяем, что при запросе всех питомцев с неправильным фильтром сервер выдаст ошибку 500
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем status code.
    Возможные значения неправильного фильтра: любые, кроме 'my_pets' и '' (пустого значения)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status == 500


def test_get_list_of_pets_wrong_api_key(api_key='Wrong_Api_Key', filter=''):
    """Проверяем, что при запросе всех питомцев с неправильным api_key сервер выдаст ошибку 403
    Для этого мы сразу пытаемся получить список питомцев, предварительно вставив неправильный api-key.
    Возможные значения api_key - любые, кроме правильного
    Возможные значения фильтра: любые"""

    status, _ = pf.get_list_of_pets({'key': api_key}, filter)

    assert status == 403


def test_add_new_pet_not_numbers_age(name='Барбоскин', animal_type='двортерьер',
                                     age='asd', pet_photo='images/cat1.jpg'):
    """Проверяем, что мы не можем создать питомца с возрастом, состоящим не из цифр.
    Мы ожидаем получить status code 400
    Итог - мы можем добавить питомца с возрастом не из цифр, если мы не будем проверять это до отправки запроса на сервер,
    То есть если мы это будем проверять в API"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_without_photo(name='Барбоскин', animal_type='двортерьер', age='12'):
    """Здесь мы проверяем, что мы можем добавить нового питомца без фотографии.
    Мы ожидаем получить status code 200 и что имя в возвращенном json будет совпадать с данным именем."""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца без фотографии
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_wrong_api_key(api_key='Wrong_Api_Key', name='Барбоскин', animal_type='двортерьер', age='12'):
    """Ожидаем, что при попытке добавления питомца без фотографии и подаче неправильного api-key мы получим ошибку 403
    и список питомцев остается тем же, что и до добавления.
    Возможные значения api_key - любые, кроме правильного"""

    # Получаем правильный api-key и список питомцев до попытки добавления
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets_before = pf.get_list_of_pets(auth_key, "my_pets")

    # Пытаемся добавить питомца без фотографии
    status, _ = pf.add_new_pet({'key': api_key}, name, animal_type, age)

    # Получаем список питомцев после попытки добавления
    _, my_pets_after = pf.get_list_of_pets(auth_key, "my_pets")

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert my_pets_before == my_pets_after


def test_delete_pet_wrong_api_key(api_key='Wrong_Api_Key'):
    """Ожидаем, что при попытке удаления питомца и подаче неправильного api-key мы получим ошибку 403 и питомец остается в списке питомцев
    Возможные значения api_key - любые, кроме правильного"""

    # Получаем правильный api-key и список питомцев до попытки удаления
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев до попытки удаления
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление с неправильным api-key
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet({'key': api_key}, pet_id)

    # Получаем список питомцев после попытки удаления
    _, my_pets_after = pf.get_list_of_pets(auth_key, "my_pets")

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert my_pets == my_pets_after
