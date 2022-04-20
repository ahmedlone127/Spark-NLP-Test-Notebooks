import argparse
import os
import requests
import re
# getting arguments 
parser = argparse.ArgumentParser(description = "pass file")
parser.add_argument("-f","--file",type = str,help = "directory")
args=parser.parse_args()
path = args.file
list_of_names = []

def get_last_path(directory,extension,keyword= ""):
    """Finds all specific type of files in given directory with a specific keyword in their name .
        
    Keyword arguments:
    direcotry  -- directory to search file for 
    extension -- what kind of file to search for
    keyword  -- what keyword should the file name contain 
    """
    list_of_path = []
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(extension) and keyword in file   :
                list_of_path.append(os.path.join(root,file))# join root and file to form a complete path
    return list_of_path
def make_Files(paths):
    """Conerts notebooks to python scripts.
        
    Keyword arguments:
    paths   -- path of files to convert 
    """
    for path in paths :
        os.system(f"jupyter nbconvert --to script '{path}' ")
def edit_files(paths):
    """Removes some parts of the file to make it runnable
        
    Keyword arguments:
    paths   -- path of files to convert 
    """
    for name in paths:
            fin = open(name, "r+", encoding = "utf-8")
            fout = open(name.replace(".py","done.txt"), "w+",encoding= "utf-8")
            fout.write(f"import os\n")
            lines = fin.readlines()
            for line in lines : 
                if (line.startswith("!") and "http://setup.johnsnowlabs.com/colab.sh" not in line):#downloads data frame from url                             
                    fout.write(f"os.system('''{line.replace('!','')}''')\n")
                elif ( "os.environ" not in line and   line.startswith("%")==False  and   line.startswith("!")==False):
                    fout.write(line)
            fout.close()
            fin.close()
def run_Files(paths):
    """Runs file and saves output to a file 
        
    Keyword arguments:
    paths   -- path of files to run
    """

    for path in paths:
        print("Currently testing ",path,flush = True)
        result_name =path.replace("done.txt","result.txt")
        try :
            os.system(f"python3.7 '{path}'  >'{result_name}' 2>&1")
        except Exception as e:# if it fails write error to file 
            fout = open("errors.txt", "a+",encoding= "utf-8")    
            fout.write(f"name : {path}\n")
            fout.write(f"{e}\n")
            fout.write("----------------------------------------------------------------------------------------------------------\n")
            fout.close()
def check_For_Errors(paths):
    """Checks whether the output contains any errors and saves errors to a file 
        
    Keyword arguments:
    paths   -- path of files to check errors for 
    """
    fout = open("errors.txt", "a+",encoding= "utf-8")
    for path in paths :
        fin = open(path, "r+", encoding = "utf-8")
        lines = fin.readlines()
        for line in lines:
            if ("Error" in line or "Exception" in line)and "UnicodeEncode" not in line and "NoSuchMethod" not in line : 
                fout.write(f"name: {path} \n")
                list_of_names.append(path)
                fout.write(f"error: ")
                for line in lines :
                    fout.write(f"{line}")
                fout.write("-------------------------------------------------------------------------------------------------- \n")
                break
                
        fin.close()
                        
    fout.close()
    fout=open("errors.txt","r+",encoding = "utf-8")
    lines = fout.readlines()
    for line in lines:
        print(line,flush = True)
    fout.close()

data = str(requests.get("http://setup.johnsnowlabs.com/colab.sh").content)
os.system(f"""python3.7 -m pip install spark-nlp=={re.findall(r'"(.*?)"',data)[0]}""")
os.system(f"""python3.7 -m pip install pyspark=={re.findall(r'"(.*?)"',data)[1]}""")
paths_For_ipynb = get_last_path(path,".ipynb")   
make_Files(paths_For_ipynb)
paths_For_txt = get_last_path(path,".txt")
paths_For_py = get_last_path(path,".py")
paths_For_txt.extend(paths_For_py)
edit_files(paths_For_txt)   
paths_of_Files_to_run = get_last_path(path,".txt","done")
run_Files(paths_of_Files_to_run)
result_files = get_last_path(path,".txt","result")
check_For_Errors(result_files)
print(list_of_names,flush = True)
