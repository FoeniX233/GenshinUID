import asyncio
import json
from pathlib import Path

import httpx

R_PATH = Path(__file__).parents[0]
MAP_PATH = R_PATH / 'map'
DATA_PATH = R_PATH / 'data'

version = '2.7.0'
version_old = '2.6.0'

avatarName2Element_fileName = f'avatarName2Element_mapping_{version}.json'
weaponHash2Name_fileName = f'weaponHash2Name_mapping_{version}.json'
weaponHash2Type_fileName = f'weaponHash2Type_mapping_{version}.json'
skillId2Name_fileName = f'skillId2Name_mapping_{version}.json'
talentId2Name_fileName = f'talentId2Name_mapping_{version}.json'
avatarId2Name_fileName = f'avatarId2Name_mapping_{version}.json'

artifact2attr_fileName = f'artifact2attr_mapping_{version_old}.json'
icon2Name_fileName = f'icon2Name_mapping_{version_old}.json'

with open(DATA_PATH / 'textMap.json', "r", encoding='UTF-8') as f:
    raw_data = json.load(f)


async def avatarId2NameJson() -> None:
    with open(DATA_PATH / 'AvatarExcelConfigData.json', "r", encoding='UTF-8') as f:
        avatar_data = json.load(f)

    temp = {}
    for i in avatar_data:
        temp[str(i['id'])] = raw_data[str(i['nameTextMapHash'])]

    with open(MAP_PATH / avatarId2Name_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp, file, ensure_ascii=False)


async def avatarName2ElementJson() -> None:
    with open(MAP_PATH / avatarId2Name_fileName, "r", encoding='UTF-8') as f:
        avatarId2Name = json.load(f)

    temp = {}
    elementMap = {'风': 'Anemo', '岩': 'Geo', '草': 'Dendro', '火': 'Pyro', '水': 'Hydro', '冰': 'Cryo', '雷': 'Electro'}
    for i in list(avatarId2Name.values()):
        data = json.loads(httpx.get('https://info.minigg.cn/characters?query={}'.format(i)).text)
        if 'errcode' in data:
            pass
        else:
            temp[i] = elementMap[data['element']]

    with open(MAP_PATH / avatarName2Element_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp, file, ensure_ascii=False)


async def weaponHash2NameJson() -> None:
    with open(DATA_PATH / 'WeaponExcelConfigData.json', "r", encoding='UTF-8') as f:
        weapon_data = json.load(f)

    temp = {}
    for i in weapon_data:
        temp[str(i['nameTextMapHash'])] = raw_data[str(i['nameTextMapHash'])]

    with open(MAP_PATH / weaponHash2Name_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp, file, ensure_ascii=False)


async def weaponHash2TypeJson() -> None:
    with open(DATA_PATH / 'WeaponExcelConfigData.json', "r", encoding='UTF-8') as f:
        weapon_data = json.load(f)

    temp = {}
    for i in weapon_data:
        if i['weaponType'] == 'WEAPON_POLE':
            weaponType = "长柄武器"
        elif i['weaponType'] == 'WEAPON_BOW':
            weaponType = "弓"
        elif i['weaponType'] == 'WEAPON_SWORD_ONE_HAND':
            weaponType = "单手剑"
        elif i['weaponType'] == 'WEAPON_CLAYMORE':
            weaponType = "双手剑"
        elif i['weaponType'] == 'WEAPON_CATALYST':
            weaponType = "法器"
        else:
            weaponType = ""
        temp[str(i['nameTextMapHash'])] = weaponType

    with open(MAP_PATH / weaponHash2Type_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp, file, ensure_ascii=False)


async def skillId2NameJson() -> None:
    with open(DATA_PATH / 'AvatarSkillExcelConfigData.json', "r", encoding='UTF-8') as f:
        skill_data = json.load(f)

    temp = {'Name': {}, 'Icon': {}}
    for i in skill_data:
        temp['Name'][str(i['id'])] = raw_data[str(i['nameTextMapHash'])]
        temp['Icon'][str(i['id'])] = i['skillIcon']

    with open(MAP_PATH / skillId2Name_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp, file, ensure_ascii=False)


async def talentId2NameJson() -> None:
    with open(DATA_PATH / 'AvatarTalentExcelConfigData.json', "r", encoding='UTF-8') as f:
        talent_data = json.load(f)

    temp = {'Name': {}, 'Icon': {}}
    for i in talent_data:
        temp['Name'][str(i['talentId'])] = raw_data[str(i['nameTextMapHash'])]
        temp['Icon'][str(i['talentId'])] = i['icon']

    with open(MAP_PATH / talentId2Name_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp, file, ensure_ascii=False)

async def artifact2attrJson() -> None:
    with open(DATA_PATH / 'ReliquaryExcelConfigData.json', "r", encoding='UTF-8') as f:
        reliquary_data = json.load(f)
    
    with open(DATA_PATH / 'DisplayItemExcelConfigData.json', "r", encoding='UTF-8') as f:
        Display_data = json.load(f)

    temp = {}
    for i in reliquary_data:
        temp[str(i['icon'])] = raw_data[str(i['nameTextMapHash'])]

    with open(MAP_PATH / icon2Name_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp, file, ensure_ascii=False)
    
    temp2 = {}
    for i in Display_data:
        if i['icon'].startswith('UI_RelicIcon'):
            temp2[raw_data[str(i['nameTextMapHash'])]] = '_'.join(i['icon'].split('_')[:-1])

    temp3 = {}
    for i in temp:
        for k in temp2:
            if i.startswith(temp2[k]):
                temp3[temp[i]] = k

    with open(MAP_PATH / artifact2attr_fileName, 'w', encoding='UTF-8') as file:
        json.dump(temp3, file, ensure_ascii=False)

async def main():
    await avatarId2NameJson()
    await avatarName2ElementJson()
    await weaponHash2NameJson()
    await skillId2NameJson()
    await talentId2NameJson()
    await weaponHash2TypeJson()
    await artifact2attrJson()

asyncio.run(main())
