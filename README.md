# EntryMerge-python

>합작할 때 작품을 하나씩 합치는 게 번거롭지 않으신가요?

>클릭 한 번으로 여러 개의 ENT 파일을 손쉽게 하나로 합쳐보세요!

## 소개

**ENT File Extractor**는 엔트리 작품 파일(`.ent`)을 압축 해제하고, 여러 개의 파일을 병합한 후 새로운 `.ent` 파일로 다시 압축할 수 있는 GUI 애플리케이션입니다. Python의 `Tkinter`로 개발되었습니다.

이 프로젝트는 **100% 생성형 AI**를 활용하여 개발되었습니다.

## 주요 기능

- `.ent` 파일 선택 및 추가 (최대 10개)
- `project.json` 파일 병합 및 중복 데이터 처리
- 압축 해제 후 다시 `.ent` 파일로 압축
- 직관적인 GUI 제공 및 예외 처리 포함

## 지원 OS

- **Windows**: EXE 실행 파일 제공
- **macOS 및 Linux**: Python 코드 실행 필요

## 실행 방법

### 1. EXE 파일 실행 (Windows 전용)

Python 환경 설정 없이 실행할 수 있는 **Windows 실행 파일**을 제공합니다.

1. [`EntryMerge.exe`](https://github.com/205sla/EntryMerge-python/tree/main/dist) 다운로드
2. `EntryMerge.exe` 실행
3. GUI에서 `.ent` 파일을 추가하고 병합 진행

> 실행 시 보안 경고가 발생하면 아래 방법을 사용하세요.

### 2. Python 코드 실행 (모든 OS)

#### 필수 라이브러리 설치

```bash
pip install -r requirements.txt
```

> `requirements.txt`가 없는 경우 다음 라이브러리를 직접 설치하세요.

```bash
pip install tk
```

#### 실행 방법

```bash
python app.py
```

## 사용 방법

[유튜브 영상](https://youtu.be/zwtdWe110rs) 참고

1. **저장 경로 지정**: 빈 폴더만 선택 가능
2. **ENT 파일 추가**: `.ent` 파일을 최대 10개까지 추가 가능
3. **압축 해제**: 개별 `.ent` 파일 압축 해제
4. **압축**: 병합된 데이터를 새 `.ent` 파일로 저장

## `.ent` 파일 포맷 설명

`.ent` 파일은 엔트리 작품 데이터를 저장하는 압축 파일로, 프로젝트의 JSON 데이터와 필요한 에셋 파일을 하나로 묶어 보관합니다.

### **파일 구조**

```
project.ent
└── temp
    ├── project.json
    ├── 0a
    └── fd
```

- **`temp` 폴더**: 프로젝트에 사용된 모든 에셋 파일이 포함된 디렉터리
- **`project.json` 파일**: 프로젝트의 전체 데이터를 포함하는 JSON 파일
- **에셋 폴더**: `project.json`에 명시된 경로에 따라 에셋 파일 저장

### **에셋 파일 경로**

에셋 파일은 고유한 파일 ID를 기반으로 폴더 구조를 형성합니다.
예를 들어, 파일 ID가 `e49448cdlyy4s42e0013f820158i7nqj`인 경우 해당 파일은 `/e4/94/` 경로에 저장됩니다.

### **압축 및 해제 방식**

- `.ent` 파일은 `tar` 형식으로 압축되며, `memLevel=6` 설정이 적용됩니다.
- 압축 시 `temp` 폴더 내 `project.json` 및 에셋 파일을 포함합니다.
- 압축 해제 시 원래 파일 구조로 복원됩니다.

## 라이선스

이 프로젝트는 **MIT 라이선스** 하에 배포됩니다.

