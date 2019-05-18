from django.test import TestCase
from .models import TodoList
from django.urls import reverse
# Create your tests here.

#새로운 TODO(제목과 내용))을 작성할 수 있다.
#TODO 목록을 볼 수 있다.
#TODO 항목의 제목과 내용을 수정할 수 있다.
#TODO 항목을 삭제할 수 있다.
#사용자의 선택에 의해 TODO에는 마감기한을 넣을 수 있다.
#TODO 항목의 우선순위를 설정 및 조절 할 수 있다.
#TODO 항목에 대한 완료처리를 할 수 있다.
#마감기한이 지난 TODO에 대해 알림을 노출 할 수 있다.

#TODO 이용시 발생하는 오류 사항을 최소화한다.
#오류 발생 시 사용자가 이해하기 쉽게 표시한다.
#다른 사람이 읽기 쉬운 코드를 작성한다.
#HTML/CSS에서 사용할 수 있는 최신 구조와 기술을 사용한다.

#직관적이고 의미 전달이 명확한 화면을 사용자에게 전달한다.