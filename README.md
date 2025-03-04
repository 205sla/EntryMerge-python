# ENT File Extractor

## 소개
**ENT File Extractor**는 `.ent` 파일을 선택하여 압축 해제하고, 여러 개의 `project.json` 파일을 병합한 후 새로운 `.ent` 파일로 다시 압축할 수 있는 GUI 애플리케이션입니다. Python의 `Tkinter`를 사용하여 개발되었습니다.

이 프로젝트는 **100% 생성형 AI**를 활용하여 개발되었습니다.

## 기능
- `.ent` 파일 선택 및 추가 (최대 10개)
- `project.json` 병합 및 중복 데이터 처리
- `scenes` ID 자동 변경 및 `objects` 내 관련 ID 수정
- 압축 해제 후 다시 `.ent` 파일로 압축
- 직관적인 GUI 및 예외 처리

## 실행 방법
### 1. 필수 라이브러리 설치
```bash
pip install -r requirements.txt
```
> `requirements.txt`가 없는 경우, 다음 라이브러리를 설치하세요:
```bash
pip install tk
```

### 2. 실행
```bash
python ent_extractor.py
```

## 사용 방법
1. **저장 경로 지정**: 빈 폴더만 선택 가능
2. **ENT 파일 추가**: `.ent` 파일을 10개까지 추가 가능
3. **압축 해제**: 개별 파일의 압축을 해제하고 `project.json`을 병합
4. **압축**: 모든 파일이 해제된 후, 병합된 데이터를 새 `.ent` 파일로 저장

## 개선 가능 사항
- 멀티 스레딩 적용 (현재는 UI가 멈출 가능성 있음)
- ZIP 압축 지원 추가
- 더 많은 파일을 처리할 수 있도록 제한 확장

## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

