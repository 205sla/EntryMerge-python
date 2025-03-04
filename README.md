# EntryMerge-python

## 소개
**ENT File Extractor**는 엔트리 작품 파일인 `.ent` 파일을 선택하여 압축 해제하고, 여러 개의 파일을 병합한 후 새로운 `.ent` 파일로 다시 압축할 수 있는 GUI 애플리케이션입니다. Python의 `Tkinter`를 사용하여 개발되었습니다.

이 프로젝트는 **100% 생성형 AI**를 활용하여 개발되었습니다.

## 기능
- `.ent` 파일 선택 및 추가 (최대 10개)
- `project.json` 병합 및 중복 데이터 처리
- 압축 해제 후 다시 `.ent` 파일로 압축
- 직관적인 GUI 및 예외 처리

## 실행 방법
### 1. EXE 파일 실행 (권장)
별도의 Python 환경 설정 없이 실행할 수 있는 **Windows 실행 파일**을 제공합니다.
1. [`dist/EntryMerge.exe` 다운로드](https://github.com/205sla/EntryMerge-python/tree/main/dist)
2. `EntryMerge.exe` 파일을 실행합니다.
3. GUI에서 `.ent` 파일을 추가하고 병합을 진행합니다.
4. 자세한 실행 방법은 [유튜브 영상](https://youtu.be/DBWdrvaxsok)을 참고하세요.

### 2. Python 코드 실행
#### 필수 라이브러리 설치
```bash
pip install -r requirements.txt
```
> `requirements.txt`가 없는 경우, 다음 라이브러리를 설치하세요:
```bash
pip install tk
```

#### 실행
```bash
python app.py
```

## 사용 방법
1. **저장 경로 지정**: 빈 폴더만 선택 가능
2. **ENT 파일 추가**: `.ent` 파일을 10개까지 추가 가능
3. **압축 해제**: 개별 `.ent` 파일의 압축을 해제
4. **압축**: 모든 파일이 해제된 후, 병합된 데이터를 새 `.ent` 파일로 저장

## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

