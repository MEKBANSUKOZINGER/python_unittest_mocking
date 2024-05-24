import random
import time
import unittest
from unittest.mock import patch

class character() :
    winning = 0
    def __init__(self, name, hp, attackRate) :
        self.name = name
        self.hp = hp
        self.attackRate = attackRate

    def getName(self) :
        return self.name
    
    def getHP(self) :
        return self.hp
    
    def getAttackRate(self) :
        return self.attackRate
    
    def attack(self, target) :
        print("공격")
 
    def getAttack(self, damage) :
        self.hp -= damage

    def __gt__(self, other) :
        if self.hp > other.hp :
            return "당신이 이기고 있습니다!"
        elif self.hp < other.hp :
            return "AI가 이기고 있습니다!"
        else :
            return "비기고 있습니다!"
        
    @classmethod
    def setWinning(cls) :
        cls.winning += 1


class player(character) :

    def attack(self, target) :
        skill = int(input("발동하실 스킬 이름을 입력해주세요! 1 : 기본 공격 | 2 : 랜덤 공격"))
        if skill == 1 :
            print(f"{self.name}의 기본 공격!")    
            target.getAttack(self.attackRate)  # 이 부분 주석처리 했다가 getAttack 짠 후에 다시 돌아와서 짜기
        elif skill == 2:
            randomAttackRate = random.randint(0,20)
            print(f"{self.name}의 랜덤 공격!")
            target.getAttack(randomAttackRate) # 이 부분 주석처리 했다가 getAttack 짠 후에 다시 돌아와서 짜기
        else :
            print(f"{self.name}은 순간 눈 앞이 흐려져 공격을 하지 못했다!")

    def getAttack(self, damage):
        super().getAttack(damage)
        print(f"{self.name}은 {damage}의 피해를 입었다!")

class AI(character) :
    
    def attack(self, target) :
        skill = random.randint(1,2)
        if skill == 1:
            print(f"{self.name}의 기본 공격!")
            target.getAttack(self.attackRate)
        elif skill == 2 :
            randomAttackRate = random.randint(0,21)
            print(f"{self.name}의 랜덤 공격!")
            target.getAttack(randomAttackRate)

    def getAttack(self, damage):
        super().getAttack(damage)
        print(f"{self.name}은 {damage}의 피해를 입었다!")

#----- TEST CASE (USING UNITTEST, MOCKING) -----
class TestGame(unittest.TestCase):

    @patch('builtins.input', side_effect = [1, 2, 'N'])
    @patch('random.randint', side_effect = [20, 1,2,20])
    def test_game_flow(self, mock_randint, mock_input):
        # 플레이어와 AI 생성
        user = player("Tester", 200, 10)
        ai = AI("AI_Test", 200, 10)
        
        # 플레이어의 공격 테스트
        user.attack(ai)
        self.assertEqual(ai.getHP(), 190)  # 기본 공격

        user.attack(ai)
        self.assertEqual(ai.getHP(), 170)  # 랜덤 공격 (random.randint가 10을 반환하도록 목업됨)

        # AI의 공격 테스트
        ai.attack(user)
        self.assertEqual(user.getHP(), 190)  # 기본 공격 (random.randint가 1을 반환하도록 목업됨)

        ai.attack(user)
        self.assertEqual(user.getHP(), 170)  # 랜덤 공격 (random.randint가 10을 반환하도록 목업됨)
    
    @patch('builtins.input', side_effect=['1', 'N'])
    def test_player_victory(self, mock_input):
        user = player("Tester", 200, 10)
        ai = AI("AI_100", 10, 10)
        
        user.attack(ai)
        print(ai.getHP())
        self.assertTrue(ai.getHP() <= 0)

    @patch('builtins.input', side_effect = ['N'])
    @patch('random.randint', side_effect = [1])
    def test_ai_victory(self, mock_randint, mock_input):
        user = player("Tester", 10, 10)
        ai = AI("AI_100", 200, 10)
        
        ai.attack(user)
        self.assertTrue(user.getHP() <= 0)
#----- TEST LOGIC ENABLED -----
#----- DOING TEST -----
if __name__ == '__main__':
    unittest.main()
#----- TEST COMPLETED -----

while True :
    userName = input("게임에 오신 것을 환영합니다! 사용자의 이름을 입력해주세요.")
    AIname = str(random.randint(1,10000)) + "호"
    user = player(userName, 200, 10)
    ai = AI(AIname, 200, 10)
    print(f"\n현재 {player.winning}번의 승리와 {AI.winning}번의 패배 기록중")
    print(f"그럼 지금부터 {user.getName()}과 {ai.getName()}의 경기가 시작됩니다!")
    while True :
        print(f"\n{user.getName()}의 차례!")
        user.attack(ai)
        if (ai.getHP() <= 0) :
            print(f"{user.getName()}가 {ai.getName()}를 꺾고 승리했습니다!")
            user.setWinning()
            break
        print(f"{ai.getName()}의 차례!")
        ai.attack(user)
        if (user.getHP() <= 0) :
            print(f"{ai.getName()}가 {user.getName()}를 꺾고 승리했습니다!")
            ai.setWinning()
            break
        print(user > ai)
    over = input("게임이 종료되었습니다. 다시 진행하시겠습니까? Y|N")
    if over == "N" :
        print("게임이 종료됩니다...")
        break
    else :
        print("게임이 다시 시작됩니다! 잠시만 기다려주세요...\n")
        time.sleep(3)


