# mixpanel을 init하기 위한 file
# 다른파일들에서 맨 아래서 생성한 mp를 가지고 mixpanel쪽과 통신할 수 있다.

from __future__ import absolute_import
from mixpanel import Mixpanel

PROJECT_TOKEN = "5f98afd11a1344fec4d92abbd375ff51"

mp = Mixpanel(PROJECT_TOKEN)