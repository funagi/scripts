import os
import shutil

base_path=os.path.abspath('.')

for dir_path, dir_names, file_names in os.walk(base_path):
    for i in dir_names:
        parent_path=os.path.join(dir_path,i)
        print('current folder:',parent_path)

        level=0
        useless_folder=''
        for dir_path2, dir_names2, file_names2 in os.walk(parent_path):
            while len(dir_names2)==1 and len(file_names2)==0:
                level=1
                if not useless_folder:
                    useless_folder=os.path.join(dir_path2,dir_names2[0])
                cur_path=os.path.join(dir_path2,dir_names2[0])
                for dir_path2, dir_names2, file_names2 in os.walk(cur_path):
                    break

            if level:
                for dir in dir_names2:
                    print('source:',os.path.join(dir_path2,dir),',destination:',parent_path)
                    shutil.move(os.path.join(dir_path2,dir),parent_path)
                for file in file_names2:
                    print('source:',os.path.join(dir_path2,file),',destination:',parent_path)
                    shutil.move(os.path.join(dir_path2,file),parent_path)

            if useless_folder:
                print('delete:',useless_folder)
                shutil.rmtree(useless_folder)
            break
    break
