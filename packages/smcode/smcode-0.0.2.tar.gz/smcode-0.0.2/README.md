# smcode

## Installaion (설치)

cmd창을 열어서 하단의 코드를 입력 후 실행.

```bash
pip install smcode
```

## Example (사용예시)
```py
from smcode.selenium import * # smcode의 selenium 모듈의 모든 것을 임포트

driver = load_driver()
```

or

```py
from smcode.selenium import load_driver # smcode의 selenium 모듈의 load_driver만 임포트

driver = load_driver()
```

or

```py
import smcode.selenium # smcode의 selenium 모듈을 임포트, 이 경우에는 하단처럼 전체 경로를 입력해야 함

driver = smcode.selenium.load_driver()
```

or

```py
import smcode # 이 경우에는 하단처럼 전체 경로를 입력해야 함

driver = smcode.selenium.load_driver()
```

### 시크릿모드

```py
from smcode.selenium import *

driver = load_driver(mode='secret') # 다른 import 방법들도 가능
```
