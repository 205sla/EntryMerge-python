import os
import tarfile
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import random
import string
import shutil

class ENTFileExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("ENT 파일 선택 및 압축 해제")
        
        self.file_list = []
        self.extract_buttons = []  # 각 파일의 압축 해제 버튼들을 저장
        self.save_path = None      # 사용자가 지정한 저장 경로
        self.merged_project_json = {}  # 모든 project.json 내용을 병합해서 저장할 딕셔너리
        
        # 저장 경로 지정 UI
        self.save_path_label = tk.Label(root, text="저장 경로가 지정되지 않았습니다.")
        self.save_path_label.pack(pady=5)
        
        self.save_path_button = tk.Button(root, text="저장 경로 지정", command=self.choose_save_path)
        self.save_path_button.pack(pady=5)

        # 작품 추가 버튼
        self.add_button = tk.Button(root, text="작품 추가하기", command=self.add_files)
        self.add_button.pack(pady=5)
        
        # "압축 하기" 버튼 (초기 상태: 비활성화)
        self.compress_button = tk.Button(root, text="압축 하기", command=self.compress_files, state=tk.DISABLED)
        self.compress_button.pack(pady=5)
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=5)
    
    def choose_save_path(self):
        path = filedialog.askdirectory()
        if path:
            # 경로 선택 시 빈 폴더만 선택 가능하도록 체크
            if os.listdir(path):
                messagebox.showerror("오류", "빈 폴더만 선택 가능합니다.")
                return
            self.save_path = path
            self.save_path_label.config(text=f"저장 경로: {self.save_path}")
            # 저장 경로 지정 후, 이미 추가된 파일들의 압축 해제 버튼 활성화
            for button in self.extract_buttons:
                button.config(state=tk.NORMAL)
    
    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("ENT files", "*.ent"), ("All files", "*.*")])
        
        for file in files:
            if file not in self.file_list and len(self.file_list) < 10:
                self.file_list.append(file)
                self.display_file(file)
        # 파일 추가 후 압축 하기 버튼의 활성화 조건을 재확인
        self.check_compress_button_condition()
    
    def display_file(self, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # KB 단위 변환
        
        file_frame = tk.Frame(self.frame)
        file_frame.pack(fill=tk.X, pady=2)
        
        label = tk.Label(file_frame, text=f"{file_name} ({file_size:.2f} KB)", width=40, anchor="w")
        label.pack(side=tk.LEFT, padx=5)
        
        # 저장 경로가 지정되어 있어야 압축 해제 버튼 활성화
        button_state = tk.NORMAL if self.save_path else tk.DISABLED
        button = tk.Button(file_frame, text="압축 해제", command=lambda: self.extract_file(file_path, button), state=button_state)
        button.pack(side=tk.RIGHT, padx=5)
        self.extract_buttons.append(button)
    
    @staticmethod
    def merge_dicts(dict1, dict2):
        """
        두 딕셔너리를 재귀적으로 병합합니다.
        - 동일 키가 있고 값이 딕셔너리인 경우 재귀 병합
        - 동일 키가 있고 값이 리스트인 경우 중복 없이 합침
        - 그 외에는 값이 다르면 리스트로 묶어 저장
        """
        for key, value in dict2.items():
            if key in dict1:
                if isinstance(dict1[key], dict) and isinstance(value, dict):
                    dict1[key] = ENTFileExtractor.merge_dicts(dict1[key], value)
                elif isinstance(dict1[key], list) and isinstance(value, list):
                    for item in value:
                        if item not in dict1[key]:
                            dict1[key].append(item)
                else:
                    if dict1[key] != value:
                        if not isinstance(dict1[key], list):
                            dict1[key] = [dict1[key]]
                        if value not in dict1[key]:
                            dict1[key].append(value)
            else:
                dict1[key] = value
        return dict1

    def post_process_json(self):
        """
        병합된 JSON 데이터에서
        1. "scenes" 항목의 각 id를 4자리 랜덤 문자열로 변경 (중복되지 않도록)
        2. "objects" 항목 내의 "scene" 값과 "script" 문자열 내의 해당 scene id도 변경
        """
        if "scenes" in self.merged_project_json and isinstance(self.merged_project_json["scenes"], list):
            scene_mapping = {}  # 기존 id -> 새 id 매핑
            used_ids = set()
            for scene in self.merged_project_json["scenes"]:
                try:
                    old_id = scene["id"]
                    new_id = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
                    while new_id in used_ids:
                        new_id = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
                    used_ids.add(new_id)
                    scene_mapping[old_id] = new_id
                    scene["id"] = new_id
                except Exception as e:
                    messagebox.showerror("오류", f"scenes 처리 중 오류 발생: {e}")
            
            if "objects" in self.merged_project_json:
                objects = self.merged_project_json["objects"]
                
                def process_obj(obj):
                    # 기존 "scene" 키 처리
                    if "scene" in obj and obj["scene"] in scene_mapping:
                        obj["scene"] = scene_mapping[obj["scene"]]
                    # "script" 문자열 내에서 scene id 치환 처리
                    if "script" in obj and isinstance(obj["script"], str):
                        for old_id, new_id in scene_mapping.items():
                            obj["script"] = obj["script"].replace(old_id, new_id)
                
                if isinstance(objects, list):
                    for obj in objects:
                        try:
                            process_obj(obj)
                        except Exception as e:
                            messagebox.showerror("오류", f"objects 처리 중 오류 발생: {e}")
                elif isinstance(objects, dict):
                    for key, obj in objects.items():
                        try:
                            if isinstance(obj, dict):
                                process_obj(obj)
                        except Exception as e:
                            messagebox.showerror("오류", f"objects 처리 중 오류 발생: {e}")
    
    def extract_file(self, file_path, button):
        if not self.save_path:
            messagebox.showerror("오류", "저장 경로가 지정되지 않았습니다.")
            return
        
        button.config(state=tk.DISABLED, text="해제 중...")
        self.root.update_idletasks()  # UI 업데이트 강제 실행
        
        merge_folder = os.path.join(self.save_path, "ENTmerge")
        os.makedirs(merge_folder, exist_ok=True)
        
        try:
            if tarfile.is_tarfile(file_path):
                with tarfile.open(file_path, 'r') as tar_ref:
                    for member in tar_ref.getmembers():
                        if os.path.basename(member.name) == "project.json" and member.name.startswith("temp/"):
                            f = tar_ref.extractfile(member)
                            if f:
                                new_data = json.load(f)
                                self.merged_project_json = ENTFileExtractor.merge_dicts(self.merged_project_json, new_data)
                        else:
                            tar_ref.extract(member, merge_folder)
                if self.merged_project_json:
                    self.post_process_json()
                    temp_folder = os.path.join(merge_folder, "temp")
                    os.makedirs(temp_folder, exist_ok=True)
                    merged_file_path = os.path.join(temp_folder, "project.json")
                    with open(merged_file_path, "w", encoding="utf-8") as f_out:
                        json.dump(self.merged_project_json, f_out, ensure_ascii=False, indent=4)
                button.config(text="해제 완료")
                # 하나라도 압축 해제했다면 경로 수정 버튼 비활성화
                self.save_path_button.config(state=tk.DISABLED)
                # 해제 완료 후 "압축 하기" 버튼 활성화 조건 확인
                self.check_compress_button_condition()
            else:
                messagebox.showerror("오류", "지원되지 않는 압축 형식이거나 압축 파일이 아닙니다.")
                button.config(state=tk.NORMAL, text="압축 해제")
        except Exception as e:
            messagebox.showerror("오류", f"압축 해제 중 오류 발생: {e}")
            button.config(state=tk.NORMAL, text="압축 해제")

    def check_compress_button_condition(self):
        """
        추가된 파일이 2개 이상이며 모든 압축 해제 버튼의 텍스트가 "해제 완료"일 경우
        "압축 하기" 버튼을 활성화합니다.
        """
        if len(self.file_list) >= 2 and all(button.cget("text") == "해제 완료" for button in self.extract_buttons):
            self.compress_button.config(state=tk.NORMAL)
        else:
            self.compress_button.config(state=tk.DISABLED)

    def compress_files(self):
        if not self.save_path:
            messagebox.showerror("오류", "저장 경로가 지정되지 않았습니다.")
            return

        merge_folder = os.path.join(self.save_path, "ENTmerge")
        if not os.path.exists(merge_folder):
            messagebox.showerror("오류", "압축할 대상 폴더가 존재하지 않습니다.")
            return

        # 압축 직전, ENTmerge/temp 폴더 내의 project.json 파일 수정
        project_json_path = os.path.join(merge_folder, "temp", "project.json")
        if os.path.exists(project_json_path):
            try:
                with open(project_json_path, "r", encoding="utf-8") as f:
                    project_data = json.load(f)
                # 지정된 값으로 수정
                project_data["name"] = "머지"
                project_data["parent"] = "678b8711133715065e4548c7"
                project_data["origin"] = "678b8711133715065e4548c7"
                project_data["user"] = "56136825dadc91e1235b460d"
                with open(project_json_path, "w", encoding="utf-8") as f:
                    json.dump(project_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("오류", f"project.json 수정 중 오류 발생: {e}")
                return

        # 저장할 .ent 파일의 경로 선택 기능 제거, 저장 경로에 "머지.ent"로 저장
        save_file = os.path.join(self.save_path, "머지.ent")

        temp_folder = os.path.join(merge_folder, "temp")
        if not os.path.exists(temp_folder):
            messagebox.showerror("오류", "압축할 대상 폴더가 존재하지 않습니다.")
            return

        # 모든 버튼 비활성화 및 "압축 하는 중.." 표시
        for widget in [self.save_path_button, self.add_button, self.compress_button] + self.extract_buttons:
            widget.config(state=tk.DISABLED)
        self.compress_button.config(text="압축 하는 중..")

        # tar.add()에서 사용할 필터 함수 정의 (심볼릭 링크 제거 및 포터블 옵션 적용)
        def tar_filter(tarinfo):
            try:
                if tarinfo.issym():
                    return None
                tarinfo.uid = 0
                tarinfo.gid = 0
                tarinfo.uname = ""
                tarinfo.gname = ""
                return tarinfo
            except Exception:
                return None

        try:
            # temp 폴더를 기준으로 압축하며, arcname을 "temp"로 지정하여 동일한 디렉토리 구조를 생성합니다.
            with tarfile.open(save_file, "w:gz", compresslevel=6) as tar:
                tar.add(temp_folder, arcname="temp", filter=tar_filter)
            messagebox.showinfo("성공", f"파일이 성공적으로 압축되었습니다: {save_file}")
        except Exception as e:
            messagebox.showerror("오류", f"압축하는 동안 오류 발생: {e}")
        finally:
            """
            # 압축 끝난 후 생성한 임시 파일 모두 삭제
            if os.path.exists(merge_folder):
                try:
                    shutil.rmtree(merge_folder)
                except Exception as e:
                    messagebox.showerror("오류", f"임시 파일 삭제 중 오류 발생: {e}")
            """
        self.compress_button.config(text="압축 완료")

if __name__ == "__main__":
    root = tk.Tk()
    app = ENTFileExtractor(root)
    root.mainloop()
